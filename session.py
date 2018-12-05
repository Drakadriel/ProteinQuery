# coding: utf-8

from settings import DATABASE_FILE

import dbparser
import process
from itertools import islice
db = dbparser.open_database(DATABASE_FILE)
prots = {prot.name: prot.domains for prot in islice(dbparser.parse(db), 200000)}

domains = process.extract_domains(prots)
