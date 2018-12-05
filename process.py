#!/usr/bin/env python3

import sys
import time


def extract_domains(prots):
    domains = dict()
    for prot, prot_domains in prots.items():
        for prot_domain in prot_domains:
            domain_prots = domains.get(prot_domain, None)
            if domain_prots is None:
                domains[prot_domain] = {prot}
            else:
                domain_prots.add(prot)

    return domains


def compute_proximity(prots, prot1, prot2):
    domains1 = prots[prot1]
    domains2 = prots[prot2]
    return len(domains1.intersection(domains2)) / len(domains1.union(domains2))


def compute_proximities(prots, domains):
    prot_relations = {}

    def get_relation(prot1, prot2):
        def get(prot1, prot2):
            return prot_relations.get(prot1, dict()).get(prot2, 0)

        relation = get(prot1, prot2)
        return relation if relation != 0 else get(prot2, prot1)

    def add_relation(prot1, prot2):
        exists = get_relation(prot1, prot2) != 0
        if exists:
            return

        relation = prot_relations.get(prot1, None)
        if relation is None:
            relation = dict()
            prot_relations[prot1] = relation

        relation[prot2] = compute_proximity(prots, prot, related_prot)

    i = 1
    n = len(prots)
    start_time = time.time()
    for prot, prot_domains in prots.items():
        duration = time.time() - start_time
        speed = i / duration
        sys.stdout.write("{}: {} ({:0.1f}/s, Time: {:0.1f}m ETA: {}m)     \r".format(
            i, prot, speed, duration/60, ((n - i) / speed) // 60))
        sys.stdout.flush()
        i += 1

        for prot_domain in prot_domains:
            related_prots = domains[prot_domain]

            for related_prot in related_prots:
                add_relation(
                    prot,
                    related_prot,
                )

    return prot_relations
