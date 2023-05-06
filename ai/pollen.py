from elasticsearch import Elasticsearch
from datetime import datetime

class pollenBot(object):

    def __init__(self):

        self.es = Elasticsearch("http://localhost:9200")
        self.index = "pollen"
        self.city = "Stockholm"


    def get_pollen(self, city=None):

        query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "city": city if city else self.city
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
        

        response = self.es.search(index=self.index, query=query)

        data = [
            {
                "date": d['_source']['date'],
                "name": d['_source']['pollen_name'],
                "level": d['_source']['pollen_level']
            }
            for d in response['hits']['hits']        
        ]

        return data

    def get_message(self, city=None):
        
        data = self.get_pollen(city=city)
        
        names = set(sorted([d['name'] for d in data]))
        dates = list(set(sorted([d['date'] for d in data])))

        message = f"Pollenkollen: (level out of 6) Today: {dates[0]}\n```\nPollen      "

        for i, date in enumerate(dates):
            #print(date, i)
            if i == 0:
                message += "Today".ljust(8)
            elif i == 1:
                message += "Tomorrow".ljust(8)
            else:
                message += f"Day {i+1}".ljust(8)

        message += '\n'

        for name in sorted(names):
            
            type_data = sorted([d for d in data if d['name'] == name], key=lambda d: d['date'])

            msg = f"{name} ".ljust(13) + " ".join([f"{d['level']}".ljust(8) for d in type_data]) + "\n"





            message += msg


        message += "\n```"

        return message


if __name__ == '__main__':

    pol = pollenBot()
    message = pol.get_message()
    
    print(message)

