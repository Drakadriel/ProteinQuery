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
    #tx.run("MERGE (p:Protein {name: $protein_name)",
        #    protein_name=protein_name)

    if not(match_prot(tx,protein_name)):
        tx.run("MERGE ($protein_name:Protein {name: $protein_name)",protein_name=protein_name)
    for domain in list_domain:
        #tx.run("MERGE (d:Domain {name: $domain})", domain=domain)
        if not(match_domain(tx,domain)):
            tx.run("MERGE ($domain_name:Domain {name: $domain_name)",domain_name=domain)

        tx.run("MATCH (p:Protein{name:$protein_name}),(d:Domain {name:$domain}) MERGE (p)-[:OWN]->(d)",
                protein_name=protein_name, domain=domain)

#predicat : les deux proteines sont similaires
def rel_prot(tx,protein_name_1, protein_name_2):
        if not(match_prot(tx,protein_name_1)):
            tx.run("MERGE ($protein_name:Protein {name: $protein_name)",protein_name=protein_name_1)
        if not(match_prot(tx,protein_name_2)):
            tx.run("MERGE ($protein_name:Protein {name: $protein_name)",protein_name=protein_name_2)
        tx.run("MERGE (p:Protein {name: $protein_name_1})-[:SIMILAR]-(p:Protein {name: $protein_name_2})",protein_name_1=protein_name_1, protein_name_2=protein_name_2)

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

def exec_add(prot_name,domains):
    with driver.session() as session:
        session.write_transaction(add_prot_graph, prot_name,domains)

#with driver.session() as session:
    #session.write_transaction(add_prot_graph)
    #session.write_transaction(add_friend, "Arthur", "Guinevere")
    #session.write_transaction(add_friend, "Arthur", "Lancelot")
    #session.write_transaction(add_friend, "Arthur", "Merlin")
    #session.read_transaction(print_friends, "Arthur")
