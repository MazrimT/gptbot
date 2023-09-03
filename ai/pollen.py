from elasticsearch import Elasticsearch
from datetime import datetime

class pollenBot(object):

    def __init__(self):

        self.es = Elasticsearch("http://localhost:9200")
        self.index = "pollen"


    def get_pollen(self, city=None):
        query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "city": city
                        }
                    },
                    {
                        "range": {
                            "date": {
                                "gte": datetime.now().date()
                            }
                        }
                    },
                    {
                        "range": {
                            "pollen_level": {
                                "gte": 1
                            }
                        }
                    }
                ]
            }
        }
        
        
        response = self.es.search(index=self.index, query=query, size=1000)

        data = [
            {
                "date": d['_source']['date'],
                "name": d['_source']['pollen_name'],
                "level": d['_source']['pollen_level']
            }
            for d in response['hits']['hits']        
        ]

        return data

    def get_message(self, city='Stockholm'):
        
        data = self.get_pollen(city=city)
        
        if data:
        
            names = set(sorted([d['name'] for d in data]))
            dates = list(set(sorted([d['date'] for d in data])))

            message = f"Pollen for {city}: (level out of 6) Today: {dates[0]}\n```\nPollen      "

            for i, date in enumerate(dates):

                if i == 0:
                    message += "Today".ljust(8)
                elif i == 1:
                    message += "Tomorrow".ljust(8)
                else:
                    message += f" Day {i+1}".ljust(8)

            message += '\n'

            for name in sorted(names):
                
                type_data = sorted([d for d in data if d['name'] == name], key=lambda d: d['date'])

                msg = f"{name} ".ljust(13) + " ".join([f"{d['level']}".ljust(8) for d in type_data]) + "\n"

                message += msg

            message += "\n```"

            return message
        else:
            return 'No pollen reports currently.'

    def list_cities(self):
        query = {
            "bool": {
                "must": [
                    {
                        "range": {
                            "date": {
                                "gte": datetime.now().date()
                            }
                        }
                    },
                    {
                        "range": {
                            "pollen_level": {
                                "gte": 1
                            }
                        }
                    }
                ]
            }
        }

        response = self.es.search(index=self.index, query=query, size=1000)
        
        if response["hits"]["total"]['value'] != 0:
            return sorted(list(set([d['_source']['city'] for d in response['hits']['hits']])))
        else:
            return []



if __name__ == '__main__':

    pol = pollenBot()
    cities = pol.list_cities()
    for city in cities:
        message = pol.get_message(city=city)
        print(message)
    

