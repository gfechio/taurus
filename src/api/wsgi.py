import requests
import socket
import yaml

from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields

import bone.core.status
import bone.core.user
import bone.core.zone

import bone.lib.logger
import bone.lib.util

import bone.database.user

import bone.webservice.util as util

if bone.lib.util.is_prod_server():
    log_type = 'SYSLOG'
else:
    log_type = 'STDOUT'

logger = bone.lib.logger.Logger('bone.webservice', log_type=log_type, log_ident='bone')

app = Flask(bone.__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

util.initialize_authenticator(app)
socket.setdefaulttimeout(5)

from bone.webservice.routes.dqs import api as dqs
from bone.webservice.routes.rundeck import api as rundeck
from bone.webservice.routes.instance import api as instance
from bone.webservice.routes.puppet import api as puppet
from bone.webservice.routes.vault import api as vault
from bone.webservice.routes.role import api as role
from bone.webservice.routes.image import api as image
from bone.webservice.routes.template import api as template
from bone.webservice.routes.host import api as host
from bone.webservice.routes.user import api as user
from bone.webservice.routes.frontend import api as frontend
from bone.webservice.routes.onegate import api as onegate
from bone.webservice.routes.contextualization import api as contextualization
from bone.webservice.routes.datastore import api as datastore
from bone.webservice.routes.network import api as network

from bone.webservice.routes.V2.dqs import api as dqsV2
from bone.webservice.routes.V2.role import api as roleV2
from bone.webservice.routes.V2.execution import api as executionV2
from bone.webservice.routes.V2.jobs import api as jobsV2
from bone.webservice.routes.V2.instance import api as instanceV2
from bone.webservice.routes.V2.puppet import api as puppetV2
from bone.webservice.routes.V2.vault import api as vaultV2
from bone.webservice.routes.V2.frontend import api as frontendV2
from bone.webservice.routes.V2.onegate import api as onegateV2
from bone.webservice.routes.V2.contextualization import api as contextualizationV2

api = Api(
    app,
    base_url='/api/v3/',
    base_path='/api/v3/',
    doc='/api/',
    version=bone.__version__,
    title='{} API'.format(bone.__name__.upper()),
    description='Booking.com OpenNebula API to integrate Virtual Machines.'
)

ns = api.namespace('', description='Basic Operations')
static = api.namespace('api/static', description='Static and/or cached files.')
api.add_namespace(instance)
api.add_namespace(puppet)
api.add_namespace(vault)
api.add_namespace(role)
api.add_namespace(image)
api.add_namespace(template)
api.add_namespace(host)
api.add_namespace(user)
api.add_namespace(dqs)
api.add_namespace(rundeck)
api.add_namespace(frontend)
api.add_namespace(onegate)
api.add_namespace(contextualization)
api.add_namespace(datastore)
api.add_namespace(network)

api.add_namespace(instanceV2)
api.add_namespace(puppetV2)
api.add_namespace(vaultV2)
api.add_namespace(dqsV2)
api.add_namespace(executionV2)
api.add_namespace(jobsV2)
api.add_namespace(roleV2)
api.add_namespace(frontendV2)
api.add_namespace(onegateV2)
api.add_namespace(contextualizationV2)


@app.before_request
def require_login():
    if 'zone' in request.headers:
        request.zone = request.headers['zone']
    else:
        request.zone = bone.core.zone.Zone().name

    #if 'x-api-key' not in request.headers:
    #    return 'x-api-key request header is required for authenticated requests', 401

    #NOTE: Right now we are just checking the token on user attributes ( this is not an authentication token )
    if 'x-api-key' in request.headers:
        user = bone.database.user.User()
        valid_token = user.validate_token(request.headers['x-api-key'])
    #if not valid_token:
    #    return 'x-api-key not recognized in the system', 401

@static.route('/nodes.json')
@static.doc('Static cached file for all hosts. This file is updated every 30 minutes. Do not rely on it for atomic changes!')

@ns.route('/api/healthcheck')
class Status(Resource):
    @ns.doc('status')
    @ns.response(200, 'status: OK')
    def get(self):
        with open('/etc/bone/config.yaml', 'r') as stream:
            try:
                logger.info("HEALTH_CHECK_TEST: Loading configuration file...")
                data = yaml.safe_load(stream)
                logger.info("HEALTH_CHECK_SUCCESS: Loading configuration file: Succeeded!")
            except yaml.YAMLError as exc:
                logger.warning("HEALTH_CHECK_FAILURE: Loading configuration file: Failed!")
                return jsonify({
                    'status': bone.core.status.Status.WARNING.value,
                    'message': 'Could not load the configuration file, something is weird here! {}'.format(exc)
                })

        if 'zone' in data:
            logger.info('HEALTH_CHECK_TEST: Testing OpenNebula connectivity...')

            api = bone.lib.opennebula.Opennebula(data['zone']['name'])
            r = requests.get("https://{}/".format(api.one_endpoint))
            if not r.ok:
                logger.error('HEALTH_CHECK_FAILURE: Testing OpenNebula connectivity: Failed!')

                # No need to score, this is a major issue anyway.
                return jsonify({
                    'status': bone.core.status.Status.FAIL.value,
                    'message': 'Could not talk to OpenNebula, consider me dead! {} {}'.format(r.status_code, r.reason)
                })

            if r.status_code > 399:
                logger.error('HEALTH_CHECK_FAILURE: Testing OpenNebula connectivity: Failed!')

                # No need to score, this is a major issue anyway.
                return jsonify({
                    'status': bone.core.status.Status.FAIL.value,
                    'message': 'Could not talk to OpenNebula, consider me dead! Status code was {}.'.format(r.status_code)
                })

            logger.info('HEALTH_CHECK_SUCCESS: Testing OpenNebula connectivity: Succeeded!')

        if 'serverdb' in data:
            logger.info("HEALTH_CHECK_TEST: Testing ServerDB...")
            r = requests.get('https://serverdb.booking.com/lb_check')
            if r.status_code == requests.codes.ok:
                logger.info("HEALTH_CHECK_SUCCESS: Testing ServerDB: Succeeded!")
            else:
                logger.error("HEALTH_CHECK_FAILURE: Testing ServerDB: Failed!")
                msg = 'Could not talk to ServerDB, expect a few nuances... HTTP status code was {}.'.format(r.status_code)

                # No need to score, this is a major issue anyway.
                return jsonify({
                    'status': bone.core.status.Status.FAIL.value,
                    'message': msg
                })

        # We score minor dependencies, and only alert above a certain threshold.
        message = ''
        score = 0

        if 'puppetdb' in data:
            try:
                logger.info("HEALTH_CHECK_TEST: Testing PuppetDB host existence...")
                socket.gethostbyname(data['puppetdb']['host'])
                logger.info("HEALTH_CHECK_SUCCESS: Testing PuppetDB host existence: Succeeded!")
            except socket.error:
                msg = "HEALTH_CHECK_FAILURE: Testing PuppetDB host existence: Failed!"
                logger.warning(msg)

                score += 1
                message += msg + "\n"

        if 'rundeck' in data:
            logger.info("HEALTH_CHECK_TEST: Testing RunDeck connectivity...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if s.connect_ex((data['rundeck']['host'], data['rundeck']['port'])) == 0:
                logger.info("HEALTH_CHECK_SUCCESS: Testing RunDeck connectivity: Succeeded!")
            else:
                msg = "HEALTH_CHECK_FAILURE: Testing RunDeck connectivity: Failed!"
                logger.warning(msg)

                score += 2
                message += msg + "\n"

        # We alert if all minors are going wrong:
        if score >= 3:
            return jsonify({
                'status': bone.core.status.Status.FAIL.value,
                'message': message
            })
        elif score == 0:
            return jsonify({
                'status': bone.core.status.Status.OK.value,
                'message': 'Health check completed, wij zijn helemaal gezond!'
            })
        else:
            return jsonify({
                'status': bone.core.status.Status.WARNING.value,
                'message': message
            })


@ns.route('/api/test')
class Test(Resource):
    @ns.doc('test')
    @ns.response(200, 'message: "yes this works"')
    def test(self):
        return jsonify({'message': 'yes this works'})

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201



# Start at the port 500{bone_major_version}
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
