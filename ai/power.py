from elasticsearch import Elasticsearch
from datetime import datetime
from matplotlib import pyplot as plt 
from pathlib import Path
import pytz

class powerBot(object):

    def __init__(self):

        self.es = Elasticsearch("http://localhost:9200")
        self.index = "power_cost"


    def get_power(self):
        query = {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": datetime.now().date()
                            }
                        }
                    }
                ]
            }
        }
        

        response = self.es.search(index=self.index, query=query, size=1000)
        
        if response['hits']['total']['value'] > 0:
            
            x = [d['_source']['@timestamp'][:13].replace('T', ' - ') for d in response['hits']['hits']]
            y = [d['_source']['total'] for d in response['hits']['hits']]
            
            x_now = datetime.now(pytz.timezone('Europe/Stockholm')).strftime('%Y-%m-%d - %H')
            print(x_now)
            plt.figure(figsize=(10,3))
            plt.plot(x, y) 
            plt.grid('both')
            plt.xticks(rotation=45, fontsize=7, ha="right")   
     #       plt.xlabel('Hour')
            plt.ylabel('SEK/kWh')
            plt.axvline(x = x_now, color = 'r', linestyle='dotted')
            for a,b in zip(x, y): 
                plt.text(a, b, f"    {b}", rotation=90)

            try:
                file_path = f"{Path(__file__).parent.parent.joinpath('images/power')}/power.png"
                print(file_path)
                plt.savefig(f"{file_path}", bbox_inches='tight') 
            except:
                raise



if __name__ == '__main__':

    power = powerBot()

    power.get_power()
    

