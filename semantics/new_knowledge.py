"""Contains class that build a knowledge base"""
from semantics.new_structures import *

class KnowledgeBase:
    def __init__(self):
        self.facts = []

    def process_semantic_structures(self, semantic_structures):
        response = ''
        for structure in semantic_structures:
            if isinstance(structure, NewAssertion):
                self.assimilate(structure)
            elif isinstance(structure, NewQuery):
                response = self.query(structure)
        return response

    def assimilate(self, assertion):
        self.facts.append(LocationFact(assertion))

    def query(self, query):
        """Reponds to a given query"""
        for fact in self.facts:
            response = fact.query(query)
            if response is not None:
                return response
        if isinstance(query, NewLocationQuery) or isinstance(query, NewYNQuery):
            return "I don't know about %s"% query.theme.readable()
    def readable(self):
        return '\n'.join(f.readable() for f in self.facts)

class Fact:
    def __init__(self):
        pass

    def query(self, query):
        """Returns a reponse if fact answers query, none otherwise"""
        return None

class LocationFact(Fact):
    def __init__(self, assertion):
        self.theme = assertion.theme
        self.location = assertion.location

    def readable(self):
        return '%s @ %s'%(self.theme.readable(), self.location.readable())

    def query(self, query):
        if isinstance(query, NewLocationQuery):
            if query.theme.name == self.theme.name:
                return self.readable()
        elif isinstance(query, NewYNQuery):
            if query.theme.name == self.theme.name:
                if query.location.name == self.theme.name:
                    return 'Yes.', self.readable()
                else:
                    return 'No.', self.readable()
        return None
