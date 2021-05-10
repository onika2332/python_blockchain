#write code for connecting graph
#write function to import data, update data, delete data, retrieve data
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
                msg += ("{}:{}".format(key,value) + "})"
        
        #print(msg)
        #self.driver.session().run(msg)
        
    
    # # add multi node to graph
    # def add_multi_node(self, **kwargs):
    #     assert kwargs is not None, "no data to import"


    # # add relation ship between 2 node
    # @classmethod
    # def add_relationship(self, **node1_label, **condition_property, **relationship):
        
    #     assert node1_label is not None and relationship is not None, "invalid data to import relationship"

    #     #MATCH part
    #     msg_part1 = "MATCH "

    # #delete a node, multi node, all node
    # # add multi node to graph
    # # search a node
        
if __name__ == '__main__':
    new_graph = MyGraph("bolt://localhost:7687","neo4j","3.14159265")
    new_graph.add_one_node(label="node1",
                        txn_hash=0x123456,
                      block=7273509,
                       age="",
                      tx_from="def",
                      tx_to="xyz",
                      value=0.00,
                      txn_fee=0.00044548)
    new_graph.close()
