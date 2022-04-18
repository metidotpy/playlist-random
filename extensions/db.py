from sqlalchemy import create_engine, MetaData

class ReadData:
    def connection(self, file):
        self.engine = create_engine("sqlite:///{}".format(file))
        self.meta = MetaData
        return self.engine, self.meta
    
    def read_data(self):
        data = {}
        with self.engine.connect() as con:
            result = con.execute("SELECT * FROM iframes")
            for row in result:
                url = row[1]
                name = row[2]
                creator = row[3]
                creator_link = row[4]
                iframe = row[5]
                data[url] = [name, creator, creator_link, iframe]
        return data

read_data = ReadData()