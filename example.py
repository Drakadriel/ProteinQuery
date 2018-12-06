#!/usr/bin/env python
import json

from settings import DATABASE_FILE

import dbparser
import process
from itertools import islice

from bottle import get, run, request, response, static_file

from neo4j import GraphDatabase
from settings import DATABASE_FILE


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

def match_prot_all(tx):
    results = tx.run(
    "MATCH (n:Protein) RETURN n LIMIT 100"
    )
        #return json.dumps([{"protein" : row.n} for row in results])
    return results

def correct_autoRel(tx):
    tx.run("MATCH (n)-[rel:SIMILAR]-(r) WHERE n.name=r.name DELETE rel")
    return ["ok"]

def match_domain(tx):
        results = tx.run(
        "MATCH (n:Domain) RETURN n LIMIT 100"
        )
        #return json.dumps([{"protein" : row.n} for row in results])
        return results

def show_similar(tx):
    results = tx.run("MATCH p=()-[r:SIMILAR]->() RETURN p LIMIT 100")
    return results

def show_solo_prot(tx):
    results = tx.run("MATCH (p:Protein) WHERE NOT (p)-[:OWN]-(:Domain) RETURN p LIMIT 100")
    return results

def show_similar_induce(tx):
    results = tx.run("MATCH (p1:Protein)-[:OWN]->(d:Domain)<-[:OWN]-(p2:Protein) return p1.name, p2.name, d.name LIMIT 100")
    return results



#with driver.session() as session:
    #session.write_transaction(add_prot_graph)
    #session.write_transaction(add_friend, "Arthur", "Guinevere")
    #session.write_transaction(add_friend, "Arthur", "Lancelot")
    #session.write_transaction(add_friend, "Arthur", "Merlin")
    #session.read_transaction(print_friends, "Arthur")

@get("/")
def get_index():
    return static_file("index.html", root="static")


@get("/graph")
def get_graph():
    return {}
#ne pas reuse après avoir fait car prend une plombe
@get("/construct")
def construct():
    db = dbparser.open_database(DATABASE_FILE)
    for prot in islice(dbparser.parse(db), 200000):
        session.write_transaction(add_prot_graph,prot.name, prot.domains)

#ne pas reuse car prend une plombe
@get("/similar")
def do_similar():
    parser = dbparser.open_proximities("proximities")
    with driver.session() as session:
        for prot1,prot2,quot in parser:
            session.write_transaction(rel_prot,prot1,prot2, quot)
        session.write_transaction(correct_autoRel)

@get("/show_similar_induce")
def show_similar_induce():
    with driver.session() as session:
        session.read_transaction(show_similar_induce)

@get("/show_similar")
def show_similar():
    with driver.session() as session:
        session.read_transaction(show_similar)

@get("/protein")
def get_protein():
    with driver.session() as session:
        session.read_transaction(match_prot_all)

@get("/domain")
def get_domain():
    with driver.session() as session:
        session.read_transaction(match_domain)

@get("/soloProt")
def getSolo():
    with driver.session() as session:
        session.read_transaction(show_solo_prot)


##################################"
##################################""



if __name__ == "__main__":
    run(port=8080)
