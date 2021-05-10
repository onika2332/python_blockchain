#write code for connecting graph
#write function to import data, update data, delete data, retrieve data
from neo4j import GraphDatabase
class MyGraph:

    @classmethod
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri=uri, auth=(username,password))
        self.session = self.driver.session()
    
    # class _node:
    #     def __init__(self,txn_hash,block,age,tx_from,tx_to,value,txn_fee,*args):
    #         self.txn_hash = txn_hash
    #         self.block = block
    #         self.age = age
    #         self.tx_from = tx_from
    #         self.tx_to = tx_to
    #         self.value = value
    #         self.txn_fee = txn_fee
    #     def return_node(self):
    #         return {
    #             "txn_hash" : self.txn_hash,
    #             "block" : self.block,
    #             "age" : self.age,
    #             "tx_from" : self.tx_from,
    #             "tx_to" : self.tx_to,
    #             "value" : self.value,abc"
    #             "txn_fee" : self.txn_fee
    #         }
    
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
                    msg += (f"(n:{value}"+"{")
                else:
                    msg += f"{key}:{value},"
                count += 1 
            else:
                msg += (f"{key}:{value}"+"})")
        self.session.run(msg)
        print(msg)
    
    # add relation ship between 2 node
    #delete a node, multi node, all node
    # add multi node to graph
    # search a node
        
if __name__ == '__main__':
    new_graph = MyGraph("bolt://localhost:7687","neo4j","3.14159265")
    new_graph.add_one_node(label="node1",
                        txn_hash=0x123456,
                      block=7273509,
                       age="ages",
                      tx_from="def",
                      tx_to="xyz",
                      value=0.00,
                      txn_fee=0.00044548)
    new_graph.close()
