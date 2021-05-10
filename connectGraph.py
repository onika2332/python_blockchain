#write code for connecting graph
#write function to import data, update data, delete data, retrieve data
import json
from neo4j import GraphDatabase
class MyGraph:
    #constructor
    @classmethod
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri=uri, auth=(username,password))
        self.session = self.driver.session()
    
    #close session
    @classmethod
    def close(self):
        self.driver.close()
        
    
    #add one node to graph
    @classmethod
    def add_one_node(self, **kwargs):
        # CREATE statement
        msg = "create "

        # if import data is none   
        assert kwargs is not None, "no data to import"
        
        count = 0 
        for key,value in kwargs.items():
            if count < len(kwargs) - 1:
                if 0 == count:
                    msg += ("(n:{}".format(value) + "{")
                else:
                    msg += "{}:{},".format(key,value)
                count += 1 
            else:
                msg += ("{}:{}".format(key,value) + "})")
        (msg)
        #print(msg)
        self.session.run(msg)
        
    @classmethod
    def add_node_from_json(self, filename1='acc.json',filename12='fico1.json'):
        f1 = open('acc.json')
        f2 = open('fico1.json')

        data1 = json.load(f1)  # from acc.json, we have id, 
        data2 = json.load(f2)  # from fico1.json, we have avarage, balance, history, fico

        info = {}
        info["id"] = []
        info["label"] = []
        info["average"] = []
        info["balance"] = []
        info["history"] = []
        info["fico"] = []
        
        for key, value in data1.items():    
            info["id"].append(key)
            info["label"].append(value)

        for obj in data2:
            info["average"].append(obj["average_transaction"])
            info["balance"].append(obj["balance"])
            info["history"].append(obj["history"])
            info["fico"].append(obj["fico"])
        
        for i in range(0,len(info["id"])):
            if i < len(info["fico"]):
                self.add_one_node(
                                label = "N" + str(info["label"][i]),
                                id = str(info["id"][i]),
                                average = str(info["average"][i]),
                                balance = str(info["balance"][i]),
                                history = str(info["history"][i]),
                                fico = str(info["fico"][i]))
            else:
                self.add_one_node(label = "N" + str(info["label"][i]),
                                    id = str(info["id"][i]))

if __name__ == '__main__':
    new_graph = MyGraph("bolt://localhost:7687","neo4j","3.14159265")
    new_graph.add_node_from_json()
    new_graph.close()
