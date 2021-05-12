from neo4j import GraphDatabase as gr


adds = str(0xd80956d9c0b6fa21c9eaa4d4cfd4742d9294356fc1b4f715e6048ef9dc760f14)
print(adds, type(adds))
add = "address:{}".format(adds)
query4 = "create (n:{}".format("player100") + "{" + "{},".format(add) + "team: juventus})"
print(query4)

session = gr.driver(uri="bolt://localhost:7687",auth=("neo4j","3.14159265")).session()
session.run(query4)

