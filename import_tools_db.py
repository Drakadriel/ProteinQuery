import neo4j_utils

from settings import DATABASE_FILE

import dbparser
import process
from itertools import islice

if __name__ == "__main__":
    db = dbparser.open_database(DATABASE_FILE)
    for prot in islice(dbparser.parse(db), 200000):
        neo4j_utils.exec_add(prot.name, prot.domains)
