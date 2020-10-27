'''Database abstraction module'''
from influxdb import InfluxDBClient, DataFrameClient

import config

class Database:
    '''
    Initialize DB
    '''
    def __init__(self):
        '''
        Read configurations defined on config.py
        Later to be transported to another source
        '''
        self.host = config.DB_HOST
        self.port = config.DB_PORT
        self.dbname = config.DB_NAME

    def use(self, dbname):
        '''
        Select database to be used
        :param dbname: ( str ) in the case taurus
        :return:
        '''
        client = InfluxDBClient(host=self.host, port=self.port)
        client.create_database(dbname)
        client.switch_database(dbname)


    def panda_write(self, dbname, dataframe, stock):
        '''
        To write panda formaed data_points
        :param dbname: ( str ) in the case taurus
        :param dataframe:  received data_points models from predictions
        :param stock: ( str ) Stock ticker
        :return:
        '''
        client = DataFrameClient(host=self.host, port=self.port, database=dbname)
        client.write_points(dataframe, stock)
