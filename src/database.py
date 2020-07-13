from influxdb import InfluxDBClient, DataFrameClient


class Database:
    def __init__(self, dbname):
        self.dbname = dbname

    def use(self):
        client = InfluxDBClient(host='localhost', port=8086)
        if client.switch_database(self.dbname):
            print(f"Using: {self.dbname}")
        else:
            print(f"DB inexistent, creating: {self.dbname}")
            client.create_database(self.dbname)


    def panda_write(self, dataframe, stock):
        client = DataFrameClient(host='127.0.0.1', port=8086, database=self.dbname)
        client.write_points(dataframe,stock)