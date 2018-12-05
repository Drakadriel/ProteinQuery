import parser
import process
import sys


if __name__ == '__main__':
    db = parser.open_database(sys.argv[1])
    prots = {prot[0]: prot[1] for prot in parser.parse(db)}
    domains = process.extract_domains(prots)
