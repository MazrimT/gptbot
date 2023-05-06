from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

class temperatureBot(object):

    def __init__(self):

        self.es = Elasticsearch("http://localhost:9200")
        self.index = "measurement"
        self.city = "Stockholm"


    def get_temperature(self):

        #query = {
        #    "bool": {
        #        "must": [
        #            {
        #                "range": {
        #                    "@timestamp": {
        #                        "gte": datetime.now().date()# - timedelta(days=1)
        #                    }
        #                }
        #            }
        #        ]
        #    }
        #}
        query = {
            "match_all": {}
        }

        
        response = self.es.search(index=self.index, query=query, sort='_soruce,@timestamp:desc')

        measurements = response['hits']['hits']
        inside_temp = None
        outside_temp = None


        #print(datetime.now().date() - timedelta("days=1"))

        measurements= sorted(measurements, key=lambda d: d['_source']['@timestamp'])
        for m in measurements:
            print(m['_source']['@timestamp'])
       # for measurement in sorted(measurements, ):
        #    print(measurement['_source'])

        #data = [
        #    {
        #        "date": d['_source']['date'],
        #        "name": d['_source']['pollen_name'],
        #        "level": d['_source']['pollen_level']
        #    }
        #    for d in response['hits']['hits']        
        #]
#
        #return data

    def get_message(self):
        
        data = self.get_temperature()
        
        

        #return message


if __name__ == '__main__':

    temp = temperatureBot()
    message = temp.get_message()
    
    print(message)

