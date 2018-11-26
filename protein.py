#!/usr/bin/env python3

class Protein:    # Initializer / Instance Attjaccard.py    ributes
  def __init__(self, domains):
      self.domains = domains
  def jaccard_calc(self, other):
      intersection = set(self.domains).intersection(other.domains)
      union = set(self.domains).union(other.domains)
      print("-- {} {} --".format(len(intersection),len(union)))
      return len(intersection)/len(union)
# Instantiate the Dog object
p1 = Protein(["IPR012345", "IPR123456"])
p2 = Protein(["IPR012345", "IPR123455"])
print("{} jaccard".format(p1.jaccard_calc(p2)))