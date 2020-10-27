'''
Module for logging
'''
import os
import sys
import json
import logging
import logging.handlers


class Logger:
    '''Definition of logger class'''
    RootLogger = None
    RootLogType = None
    def __init__(self, name, log_type=None, log_level='DEBUG', log_ident='taurus'):
        '''
        name: application name
        log_type: Syslog, STDOUT
        log_level: DEBUG, INFO, WARNING
        log_ident: service name
        '''
        self.name = name

        # Should be called only once in an application's lifetime.
        if (Logger.RootLogger is None) or log_type is not None:
            Logger.RootLogger = logging.getLogger('taurus')
            Logger.RootLogger.setLevel(getattr(logging, log_level))

            if log_type == 'SYSLOG':
                handler = logging.handlers.SysLogHandler()
                handler.ident = '{} {}: '.format(os.uname().nodename, log_ident)
            elif log_type == 'STDOUT' or log_type is None:
                log_type = 'STDOUT'
                handler = logging.StreamHandler(stream=sys.stdout)

            Logger.RootLogger.handlers = []
            handler.setFormatter(logging.Formatter('%(message)s'))
            Logger.RootLogger.addHandler(handler)
            Logger.RootLogType = log_type

        self.logger = logging.getLogger('taurus')

    def debug(self, message):
        '''Sets loglevet to be DEBUG'''
        self._log('DEBUG', message)

    def info(self, message):
        '''Sets loglevet to be INFO'''
        self._log('INFO', message)

    def warning(self, message):
        '''Sets loglevet to be WARNING'''
        self._log('WARNING', message)

    def error(self, message):
        '''Sets loglevet to be ERROR'''
        self._log('ERROR', message)

    def critical(self, message):
        '''Sets loglevet to be CRITICAL'''
        self._log('CRITICAL', message)

    def _log(self, level, args):
        ''' Internal Function responsible for parsing and sending to syslog.'''
        data = {}
        for name, value in args.items():
            if name == 'self' or name == 'kwargs' or value is None:
                continue
        data['module'] = self.name
        data['severity'] = level

        if Logger.RootLogType == 'STDOUT':
            log_output = data['message']
        else:
            log_output = json.dumps(data)

        exception_exists = sys.exc_info() != (None, None, None)

        self.logger.log(getattr(logging, level), log_output, exc_info=exception_exists)
