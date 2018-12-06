from neo4j import GraphDatabase
from settings import DATABASE_FILE

import dbparser
import process
from itertools import islice

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo"))
'''
#Exemples qui marchent
def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
         print(record["friend.name"])

'''
# list_domain must be a python list, create a protein with its relatives domains
def add_prot_graph(tx, protein_name,list_domain):
    tx.run("MERGE (p:Protein {name: $protein_name})",protein_name=protein_name)
    for domain in list_domain:
        tx.run("MERGE (d:Domain {name: $domain_name})",domain_name=domain)
        tx.run("MATCH (p:Protein{name:$protein_name}),(d:Domain {name:$domain}) MERGE (p)-[:OWN]->(d)",
                protein_name=protein_name, domain=domain)
    return ["ok"]

#predicat : les deux proteines sont similaires
def rel_prot(tx,protein_name_1, protein_name_2, quot):
        tx.run("MERGE (p:Protein {name: $protein_name})",protein_name=protein_name_1)
        tx.run("MERGE (p:Protein {name: $protein_name})",protein_name=protein_name_2)
        tx.run("MATCH (p1:Protein {name: $protein_name_1}),(p2:Protein {name: $protein_name_2}) MERGE (p1)-[:SIMILAR {quotien:$quot}]-(p2)",protein_name_1=protein_name_1, quot=quot, protein_name_2=protein_name_2)
        return ["ok"]

def match_prot(tx,protein_name):
        results = tx.run(
        "MATCH (n:Protein) WHERE n.name=$name RETURN n", name=protein_name
        )
        #return json.dumps([{"protein" : row.n} for row in results])
        return results

def match_domain(tx,domain_name):
        results = tx.run(
        "MATCH (n:Domain) WHERE n.name=$name RETURN n", name=domain_name
        )
        #return json.dumps([{"protein" : row.n} for row in results])
        return results

def show_similar(tx):
    results = tx.run("MATCH p=()-[r:SIMILAR]->() RETURN p LIMIT 25")
    return results

def show_solo_prot(tx):
    results = tx.run("MATCH (p:Protein) WHERE NOT (p)-[:OWN]-(:Domain) RETURN p LIMIT 25")
    return results

def show_similar_induce(tx):
    results = tx.run("MATCH (p1:Protein)-[:OWN]->(d:Domain)<-[:OWN]-(p2:Protein) return p1.name, p2.name, d.name LIMIT 25")
    return results



##################################"
##################################""

def show_similar():
    with driver.session() as session:
        session.read_transaction(show_similar)

def exec_simil(prot_name1, prot_name2, quot):
    with driver.session() as session:
        session.write_transaction(rel_prot,prot_name1,prot_name2, quot)

def exec_add(prot_name,domains):
    with driver.session() as session:
        session.write_transaction(add_prot_graph, prot_name,domains)

#with driver.session() as session:
    #session.write_transaction(add_prot_graph)
    #session.write_transaction(add_friend, "Arthur", "Guinevere")
    #session.write_transaction(add_friend, "Arthur", "Lancelot")
    #session.write_transaction(add_friend, "Arthur", "Merlin")
    #session.read_transaction(print_friends, "Arthur")
