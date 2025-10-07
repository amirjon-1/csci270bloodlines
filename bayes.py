from factor import multiply_factors, marginalize
class BayesianNetwork:
    """Represents a Bayesian network by its factors, i.e. the conditional probability tables (CPTs).

    Parameters
    ----------
    factors : list[factor.Factor]
        The factors of the Bayesian network
    domains : dict[str, list[str]]
        A dictionary mapping each variable to its possible values
    """

    def __init__(self, factors, domains):
        self.factors = factors
        self.domains = domains
        self.variables = set()
        for factor in self.factors:
            self.variables = self.variables | set(factor.variables)

    def __str__(self):
        return "\n\n".join([str(factor) for factor in self.factors])


def eliminate(bnet, variable):
    """Eliminates a variable from the Bayesian network.

    By "eliminate", we mean that the factors containing the variable are multiplied,
    and then the variable is marginalized (summed) out of the resulting factor.

    Parameters
    ----------
    variable : str
        the variable to eliminate from the Bayesian network

    Returns
    -------
    BayesianNetwork
        a new BayesianNetwork, equivalent to the current Bayesian network, after
        eliminating the specified variable
    """
    factorsWithVar = []
    factorsWithoutVar = []
    for factor in bnet.factors:
        if variable in factor.variables:
            factorsWithVar.append(factor)
        else:
            factorsWithoutVar.append(factor)
    
    if len(factorsWithVar) == 0:
        return bnet
    
    combinedFactor = multiply_factors(factorsWithVar, bnet.domains)
    marginalizedFactor = marginalize(combinedFactor, variable)

    newFactors = [];

    for factor in factorsWithoutVar:
        newFactors.append(factor)
    
    newFactors.append(marginalizedFactor)

    return BayesianNetwork(newFactors, bnet.domains)


def compute_marginal(bnet, vars):
    """Computes the marginal probability over the specified variables.

    This method uses variable elimination to compute the marginal distribution.

    Parameters
    ----------
    vars : set[str]
        the variables that we want to compute the marginal over
    """
    elim_order, _ = list(bnet.variables), None
    revised_elim_order = [var for var in elim_order if var not in vars]
    for var in revised_elim_order:
        bnet = eliminate(bnet, var)
    return multiply_factors(bnet.factors, bnet.domains)

    
    
def compute_conditional(bnet, event, evidence):
    """Computes the conditional probability of an event given the evidence event."""
    aAndB = {**event, **evidence}
    aAndBFactor = compute_marginal(bnet, aAndB.keys())
    prob = aAndBFactor[aAndB]

    evidenceFactor = compute_marginal(bnet, evidence.keys())
    evidenceProb = evidenceFactor[evidence]

    if evidenceProb == 0:
        return 0

    return prob/evidenceProb;



