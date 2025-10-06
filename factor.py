import itertools
from itertools import product

class Factor:
    def __init__(self, variables, values):
        self.variables = variables
        self.values = values

    def __getitem__(self, event):
        key = []
        for var in self.variables:
            if var not in event:
                raise KeyError(f"Variable {var} not found in given event.")
            key.append(event[var])
        if tuple(key) in self.values:
            return self.values[tuple(key)]
        else:
            raise KeyError(f"No value assigned to event {event}.")

    def __str__(self):
        result = f"{self.variables}:"
        for event, value in self.values.items():
            result += f"\n  {event}: {value}"
        return result

    __repr__ = __str__


def events(vars, domains):
    thing = list(itertools.product(list(zip(vars,element)) for element in domains))
 
    return thing
    

def marginalize(factor, variable):
    """TODO: Implement this for Question Two."""

def multiply_factors(factors, domains):
    """TODO: Implement this for Question Three."""
