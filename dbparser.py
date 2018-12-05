#!/usr/bin/env python3

import gzip
import collections

Protein = collections.namedtuple("Protein", ["name", "description", "domains"])


def open_database(filename):
    strip_newline = lambda l: l.rstrip("\n")
    f = gzip.open(filename, 'rt')
    return map(strip_newline, f)



def parse(db):
    current_prot_id = None
    current_prot_domains = None

    line = None
    while True:
        try:
            line = next(db)
        except StopIteration:
            return

        type = None
        if line == '//':
            yield Protein(current_prot_id, "", current_prot_domains)
            continue

        if not line.startswith(" "):
            type, line = line.split("   ", maxsplit=1)

        if type == 'ID':
            current_prot_id = None
            current_prot_domains = set()
        elif type == 'AC':
            current_prot_id = line.split(';')[0]
        elif type == 'DR':
            if line.startswith("InterPro;"):
                domain = line.split('; ')[1]
                current_prot_domains.add(domain)

def save_proximities(proximities, filename):
    with gzip.open(filename, 'wt') as file:
        for prot1, prot1_prox in proximities.items():
            for prot2, proximity in prot1_prox.items():
                file.write("{}\t{}\t{}\n".format(prot1, prot2, proximity))


def open_proximities(filename):
    strip_newline = lambda l: l.rstrip("\n")
    f = gzip.open(filename, 'rt')
    def extract_from_line(line):
        data = line.split("\t")
        data[2] = float(data[2])
        return data

    return map(extract_from_line, map(strip_newline,f))
