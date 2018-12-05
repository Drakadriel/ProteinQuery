#!/usr/bin/env python
import json

from settings import DATABASE_FILE

import dbparser
import process
from itertools import islice

from bottle import get, run, request, response, static_file
import neo4j_utils
from neo4j_utils import *


@get("/")
def get_index():
    return static_file("index.html", root="static")


@get("/graph")
def get_graph():
    return {}

@get("/construct")
def construct():
    db = dbparser.open_database(DATABASE_FILE)
    for prot in islice(dbparser.parse(db), 200000):
        neo4j_utils.exec_add(prot.name, prot.domains)


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
