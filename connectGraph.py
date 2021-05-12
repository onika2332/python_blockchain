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
    def add_one_node(self, node_type="Wallet", **kwargs):
        # CREATE statement
        msg = "create (n:{}".format(node_type) + "{"

        # if import data is none   
        assert kwargs is not None, "no data to import"
        
        count = 0 
        for key,value in kwargs.items():
            if count < len(kwargs) - 1:
                if(0 == count):
                    msg+= '{}:"{}",'.format(key,value)
                else:
                    msg += "{}:{},".format(key,value)
                count += 1 
            else:
                msg += ("{}:{}".format(key,value) + "})")
        #print(msg)
        self.session.run(msg)
        
    @classmethod
    def add_wallet_node_from_json(self, filename1='acc.json',filename12='fico1.json'):
        f1 = open('acc.json')
        f2 = open('fico1.json')

        data1 = json.load(f1)  # from acc.json, we have id, 
        data2 = json.load(f2)  # from fico1.json, we have avarage, balance, history, fico

        info = {}
        info["id"] = []
        info["address"] = []
        info["average"] = []
        info["balance"] = []
        info["history"] = []
        info["fico"] = []
        
        for key, value in data1.items():    
            info["id"].append(key)
            info["address"].append(value)

        for obj in data2:
            info["average"].append(obj["average_transaction"])
            info["balance"].append(obj["balance"])
            info["history"].append(obj["history"])
            info["fico"].append(obj["fico"])
        
        for i in range(0,len(info["id"])):
            if i < len(info["fico"]):
                self.add_one_node(
                                address = info["address"][i],
                                id = info["id"][i],
                                average = info["average"][i],
                                balance = info["balance"][i],
                                history = info["history"][i],
                                fico = info["fico"][i])
            else:
                self.add_one_node(label = info["address"][i],
                                    id = info["id"][i])
    
    @classmethod
    def search_by_address(self, address):
        msg = 'MATCH (n) WHERE n.address = "{}" RETURN (n)'.format(hex(address))

        data = self.session.run(msg).data()
        
        if data is not None:
            return data
        else:
            print("This address isn't available")

    @classmethod
    def search_by_balance(self, balance_value):
        count_msg = "MATCH (n:{}) WHERE n.balance >= {} RETURN(n)".format("Wallet",balance_value)
        
        accounts = self.session.run(count_msg)
        
        list_wallets = [acc for acc in accounts.data()]
        
        print(len(list_wallets))
        if len(list_wallets) != 0 :
            return list_wallets
        
        print("No wallets reach this balance value {}".format(balance_value))

    @classmethod
    def seacrh_by_fico(self, fico):
        count_msg = "MATCH (n:{}) WHERE n.fico >= {} RETURN(n)".format("Wallet",fico)
        
        accounts = self.session.run(count_msg)
        
        list_wallets = [acc for acc in accounts.data()]
        
        if len(list_wallets) != 0:
            return list_wallets
        
        print("No wallets reach this fico {}".format(fico))
    
    @classmethod
    def delete_node(self, *args):
        #delete one or multiple node
        assert args is not None, "No address specified for deletion"

        for address in args:
            msg = 'MATCH(n) WHERE n.address = "{}" DETACH DELETE(n)'.format(hex(address))
            self.session.run(msg)
    
    # @classmethod
    # def add_relationship(type)

    # @classmethod
    # def search_30_latest_transactions(address):
        
if __name__ == '__main__':
    new_graph = MyGraph("bolt://localhost:7687","neo4j","3.14159265")
    #new_graph.add_wallet_node_from_json()
    
    #print(new_graph.search_by_address(0x788cabe9236ce061e5a892e1a59395a81fc8d62c))
    #print(new_graph.search_by_balance(250))
    print(new_graph.search_by_fico(100))
    new_graph.close()

