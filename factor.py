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
    values = [domains[var] for var in vars]
    combinations = itertools.product(*values)
    return [dict(zip(vars, combo)) for combo in combinations]
    

def marginalize(factor, variable):
    newVars = []
    for var in factor.variables:
        if var != variable:
            newVars.append(var)
    
    newValues = {}
    possibleValues = {}

    for index, varName in enumerate(factor.variables):
        seenValues = set()
        for keyTuple in factor.values.keys():
            seenValues.add(keyTuple[index])
        possibleValues[varName] = list(seenValues)

    valueLists = []
    for varName in newVars:
        valueLists.append(possibleValues[varName])
    
    for combo in itertools.product(*valueLists):
        newEvent = {}
        
        for i in range (len(newVars)):
            varName = newVars[i]
            varValue = combo[i]
            newEvent[varName] = varValue
        
        sumVal = 0;
        for val in possibleValues[variable]:
            fullEvent = {}
            for k, v in newEvent.items():
                fullEvent[k] = v
            
            fullEvent[variable] = val
            value = factor[fullEvent]
            sumVal += value
        
        newValues[tuple(combo)] = sumVal


    return Factor(newVars, newValues)
    


def multiply_factors(factors, domains):
    allVars = []

    for factor in factors:
        for var in factor.variables:
            if var not in allVars:
                allVars.append(var)
    
    newValues = {}

    values = []
    for var in allVars:
        values.append(domains[var])

    for combo in itertools.product(*values):
        newEvent = {}
        for i in range(len(allVars)):
             newEvent[allVars[i]] = combo[i]
        
        
        prodVal = 1
        for factor in factors:
            partialEvent = {}
            for var in factor.variables:
                partialEvent[var] = newEvent[var]
            val = factor[partialEvent]
            prodVal *= val
        
        newValues[tuple(combo)] = prodVal

    return Factor(allVars, newValues)