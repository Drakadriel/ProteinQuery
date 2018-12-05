# coding: utf-8

from settings import DATABASE_FILE

import parser
import process
from itertools import islice
db = parser.open_database(DATABASE_FILE)
prots = {prot.name: prot.domains for prot in islice(parser.parse(db), 200000)}

domains = process.extract_domains(prots)
