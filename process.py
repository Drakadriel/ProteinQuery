#!/usr/bin/env python3

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
