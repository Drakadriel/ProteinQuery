#!/usr/bin/env python
import json

from bottle import get, run, request, response, static_file
from neo4j import GraphDatabase


driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo"))
tx = graph.cypher.begin()
def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
         print(record["friend.name"])

##############################################
##############################################"
##############################################"
##############################################"
# list_domain must be a python list, create a protein with its relatives domains
def add_prot_graph(tx, protein_name,list_domain):
    #tx.run("MERGE (p:Protein {name: $protein_name)",
        #    protein_name=protein_name)
    if !(match_prot(protein_name)):
        graph.cyber.execute("MERGE ($protein_name:Protein {name: $protein_name)",protein_name=protein_name)
    for domain in list_domain:
        #tx.run("MERGE (d:Domain {name: $domain})", domain=domain)
        if !(match_domain(domain)):
                graph.cyber.execute("MERGE ($domain_name:Domain {name: $domain_name)",domain_name=domain)
        graph.cypher.execute("MATCH ($protein_name:Protein({name:$protein_name})),($domain:Domain {name:$domain}) MERGE ($protein_name)-[:OWN]->($domain)",
                protein_name=protein_name, domain=domain)

#predicat : les deux proteines sont similaires
def rel_prot(tx,protein_name_1, protein_name_2):
        graph.cypher.execute("MERGE (p:Protein {name: $protein_name_1})-[:SIMILAR]->(p:Protein {name: $protein_name_2})",
        protein_name_1=protein_name_1, protein_name_2=protein_name_2)

def match_prot(protein_name):
        results = graph.cypher.execute(
        "MATCH (n:Protein) WHERE n.name=$name RETURN n", name=protein_name
        )
        #return json.dumps([{"protein" : row.n} for row in results])
        return results

def match_domain(domain_name):
        results = graph.cypher.execute(
        "MATCH (n:Domain) WHERE n.name=$name RETURN n", name=domain_name
        )
        #return json.dumps([{"protein" : row.n} for row in results])
        return results
with driver.session() as session:
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

@get("/search")
def get_search():
    try:
        q = request.query["q"]
    except KeyError:
        return []
    else:
        #results = graph.cypher.execute(
        #    "MATCH (movie:Movie) "
        #    "WHERE movie.title =~ {title} "
        #    "RETURN movie", {"title": "(?i).*" + q + ".*"})
        #response.content_type = "application/json"
        #return json.dumps([{"movie": row.movie.properties} for row in results])
        #{"protein":{
        #    "name":"PROUT",
        #    "domain": ["d1","d2"]
        #}}
        return ["search"]

@get("/protein/<name>")
def get_movie(name): #replace title with name
    #results = graph.cypher.execute(
    #    "MATCH (movie:Movie {title:{title}}) "
    #    "OPTIONAL MATCH (movie)<-[r]-(person:Person) "
    #    "RETURN movie.title as title,"
    #    "collect([person.name, head(split(lower(type(r)),'_')), r.roles]) as cast "
    #    "LIMIT 1", {"title": title})
    #row = results[0]
    #return {"title": row.title,
    #        "cast": [dict(zip(("name", "job", "role"), member)) for member in row.cast]}
    return []

if __name__ == "__main__":
    run(port=8080)
