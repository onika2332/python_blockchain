
import json
from neo4j import GraphDatabase
class MyGraph:

    @classmethod
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri=uri, auth=(username,password))
        self.session = self.driver.session()
    
    @classmethod
    def close(self):
        self.driver.close()
        
    
    @classmethod
    def add_one_node(self, node_type="Wallet", **kwargs):

        msg = "create (n:{}".format(node_type) + "{"
 
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

        self.session.run(msg)
        
    @classmethod
    def add_nft_node_from_json(self, filename='nft.json'):
        f = open("own.json")
        data = json.load(f)

        for d in data:
            self.add_one_node(node_type="NFT", address=d['address'], latest_price=d['latest_price'])

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
    def search_by_fico_index(self, fico):
        msg = "MATCH (n:{}) WHERE n.fico >= {} RETURN(n)".format("Wallet",fico)

        results = self.session.run(msg)

        list_accounts = [acc for acc in results.data()]

        if len(list_accounts) != 0:
            return list_accounts
        
        print("No wallets reach this fico {}".format(fico))
    
    @classmethod
    def delete_node(self, *args):
        #delete one or multiple node
        assert args is not None, "No address specified for deletion"

        for address in args:
            msg = 'MATCH(n) WHERE n.address = "{}" DETACH DELETE(n)'.format(hex(address))
            self.session.run(msg)
    
    @classmethod
    def add_guarantee_relationship(self, father_address, son_address):
        msg = '''MATCH (w1:Wallet), (w2:Wallet)
                WHERE w.address = "{}" AND w2.address = "{}"
                CREATE (w)-[rel:GUARANTEE]->(w2)'''.format(hex(father_address),hex(son_address))
        self.session.run(msg)

    @classmethod
    def add_own_relstionship(self, owner, nft_address):
        msg = 'MATCH (w1:Wallet), (w2:NFT) WHERE w1.address = "'+ owner + '"' + ' AND w2.address = "' + nft_address + '" CREATE (w1)-[rel:OWN]->(w2)'
        self.session.run(msg)

    @classmethod
    def add_transfer_relationship(self, sender, receiver, **rel_properties):
        msg = 'MATCH (w1:Wallet), (w2:Wallet) WHERE w1.address = "{}" AND w2.address = "{}"'.format(sender,receiver)
        
        if(rel_properties is not None):
            rel_msg = ""
            count = 1
            for prop,value in rel_properties.items():
                if(count == len(rel_properties)):
                    rel_msg += "{}: {}".format(prop,value)
                else:
                    rel_msg += "{}: {},".format(prop,value)
            
            all_rel_msg = 'create (w1)-[rel:TRANSFER {' + rel_msg + '}]->(w2)'
            
            msg += all_rel_msg
            self.session.run(msg)
        else:
            rel_msg = 'create (w1)-[rel:TRANSFER]->(w2)'
            
            msg+= rel_msg
            self.session.run(msg)

    def add_relationship_from_json(self, filename1="relationship.json", filename2="own.json"):
        f1 = open(filename1)
        f2 = open(filename2)

        data1 = json.load(f1)
        data2 = json.load(f2)

        for d1 in data1:
            self.add_transfer_relationship(d1['from'], d1['to'], amount=d1['amount'])
        for d2 in data2:
            self.add_own_relstionship(d2['owner'], d2['address'])

    @classmethod
    def search_30_latest_transfer_transaction(self,address):
        msg = '''match (sender:Wallet)-[rel:TRANSFER]->(receiver:Wallet)
        WHERE sender.address = "{}"
        RETURN rel LIMIT 30
        ORDER BY rel.timestamp'''.format(hex(address))

        results = self.session.run(msg)

        list_tx = [tx for tx in results.data()]

        if len(list_tx) == 0:
            return "No transaction"
        
        return list_tx
    
    def search_30_latest_arrival_transaction(self,address):
        msg = '''match (sender:Wallet)-[rel:TRANSFER]->(receiver:Wallet)
        WHERE receiver.address = "{}"
        RETURN rel LIMIT 30
        ORDER BY rel.timestamp'''.format(hex(address))

        results = self.session.run(msg)

        list_tx = [tx for tx in results.data()]

        if len(list_tx) == 0:
            return "No transaction arrival"
        
        return list_tx
        
if __name__ == '__main__':
    new_graph = MyGraph("bolt://localhost:7687","neo4j","3.14159265")
    #new_graph.add_wallet_node_from_json()
    new_graph.add_relationship_from_json()
    #new_graph.add_nft_node_from_json()
    
    #print(new_graph.search_by_address(0x788cabe9236ce061e5a892e1a59395a81fc8d62c))
    #print(new_graph.search_by_balance(250))
    #print(new_graph.search_by_fico_index(215))

    """
    new_graph.add_one_node(node_type="NFT",
                            address="0x12345",
                            created_at="",
                            owner="0x13562"
                            old_owner="0x56789",
                            latest_price="")
    """
    
    new_graph.close()
    

