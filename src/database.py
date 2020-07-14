import config
from influxdb import InfluxDBClient, DataFrameClient


class Database:
    def __init__(self):
        self.host = config.DB_HOST 
        self.port = config.DB_PORT
        self.dbname = config.DB_NAME

    def use(self, dbname):
        client = InfluxDBClient(host=self.host, port=self.port)
        if client.switch_database(dbname):
            print(f"Using: {dbname}")
        else:
            print(f"DB inexistent, creating: {dbname}")
            client.create_database(dbname)


    def panda_write(self, dbname, dataframe, stock):
        client = DataFrameClient(host=self.host, port=self.port, database=dbname)
        client.write_points(dataframe, stock)