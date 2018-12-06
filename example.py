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
#ne pas reuse après avoir fait car prend une plombe
@get("/construct")
def construct():
    db = dbparser.open_database(DATABASE_FILE)
    for prot in islice(dbparser.parse(db), 200000):
        neo4j_utils.exec_add(prot.name, prot.domains)

#ne pas reuse car prend une plombe
@get("/similar")
def do_similar():
    parser = dbparser.open_proximities("proximities")
    for prot1,prot2,quot in parser:
        neo4j_utils.exec_simil(prot1,prot2,quot)

    neo4j_utils.exec_delete_auto()

@get("/search")
def get_search():
    try:
        q = request.query["q"]
    except KeyError:
        return []
    else:

        return ["search"]

@get("/protein")
def get_protein(name): #replace title with name
    return neo4j_utils.exec_show_prot()



@get("/soloProt")
def getSolo():
    neo4j_utils.exec_show_solo_prot()

if __name__ == "__main__":
    run(port=8080)
