from bayes import BayesianNetwork


class FamilyMember:
    """A single member of a family tree."""

    def __init__(self, name, sex, mother, father):
        """
        Parameters
        ----------
        name : str
            The name of the family member.
        sex : str
            The sex of the family member ("male" or "female")
        mother : FamilyMember
            The mother of the family member (or None if unknown)
        father : FamilyMember
            The father of the family member (or None if unknown)
        """

        self.name = name
        self.sex = sex
        self.mother = mother
        self.father = father

    def get_name(self):
        """Returns the name of the family member."""
        return self.name

    def get_sex(self):
        """Returns the sex of the family member."""
        return self.sex


class Male(FamilyMember):
    """A male family member."""

    def __init__(self, name, mother=None, father=None):
        super().__init__(name, "male", mother, father)


class Female(FamilyMember):
    """A female family member."""

    def __init__(self, name, mother=None, father=None):
        super().__init__(name, "female", mother, father)


def romanoffs():
    """A simple example of a family, using four members of the Russian royal family (the Romanoffs)."""
    alexandra = Female("alexandra")
    nicholas = Male("nicholas")
    alexey = Male("alexey", mother=alexandra, father=nicholas)
    anastasia = Female("anastasia", mother=alexandra, father=nicholas)
    return alexandra, nicholas, alexey, anastasia


def create_variable_domains(family):
    """Creates a dictionary mapping each variable to its domain, for the hemophilia network.

    For each family member, we create either 3 or 4 variables (3 if they’re male, 4 if they’re female).
    If N is the name of the family member, then we create the following variables:
        M_N: N’s maternally inherited gene
        P_N: N’s paternally inherited gene (if N is female)
        G_N: the genotype of N
        H_N: whether N has hemophilia

    The variables should be mapped to the following domains:
        - M_N: ['x', 'X']
        - P_N: ['x', 'X']
        - G_N: ['xx', 'xX', 'XX']
        - H_N: ['-', '+']

    Parameters
    ----------
    family : list[FamilyMember]
        the list of family members

    Returns
    -------
    dict[str, list[str]]
        a dictionary mapping each variable to its domain (i.e. its possible values)
    """
    domains = {}
    
    for person in family:
        name = person.get_name()
        sex = person.get_sex()
        
        # M_N: maternally inherited gene - always present
        domains[f'M_{name}'] = ['x', 'X']
        
        # P_N: paternally inherited gene - only for females
        if sex == "female":
            domains[f'P_{name}'] = ['x', 'X']
        
        # G_N: genotype - depends on sex
        if sex == "female":
            domains[f'G_{name}'] = ['xx', 'xX', 'XX']
        else:  # male
            domains[f'G_{name}'] = ['xy', 'Xy']
        
        # H_N: hemophilia status - always present
        domains[f'H_{name}'] = ['-', '+']
    
    return domains



def create_hemophilia_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of hemophilia, given one's genotype.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of hemophilia, given one's genotype
    """
    name = person.get_name()
    sex = person.get_sex()

    g_var = f'G_{name}'
    h_var = f'H_{name}'

    probs = {}
    
    if sex == "female":
        # Female genotypes: xx, xX, XX
        # Only XX results in hemophilia (recessive)
        probs[('xx', '-')] = 1.0
        probs[('xx', '+')] = 0.0
        
        probs[('xX', '-')] = 1.0
        probs[('xX', '+')] = 0.0
        
        probs[('XX', '-')] = 0.0
        probs[('XX', '+')] = 1.0
    else: 
        # Male genotypes: xy, Xy
        # Xy results in hemophilia
        probs[('xy', '-')] = 1.0
        probs[('xy', '+')] = 0.0
        
        probs[('Xy', '-')] = 0.0
        probs[('Xy', '+')] = 1.0
    
    return Factor([g_var, h_var], probs)


def create_genotype_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of a genotype, given one's inherited genes.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of a genotype, given one's inherited genes
    """

    sex = person.get_sex()

    if sex == "male":

        variables = [f"G_{person.get_name()}", f"M_{person.get_name()}"]

        values = {}

        for m in ['x', 'X']:
            if m == 'x':
                values[('xy', m)] = 1.0
                values[('Xy', m)] = 0.0
            else:
                values[('xy', m)] = 0.0
                values[('Xy', m)] = 1.0

        return Factor(variables, values)
    
    else:
        
        variables = [f"G_{person.get_name()}", f"M_{person.get_name()}", f"P_{person.get_name()}"]

        values = {}

        for m in ['x', 'X']:
            for p in ['x', 'X']:
                if m == 'x' and p == 'x':
                    values[('xx', m, p)] = 1.0
                    values[('xX', m, p)] = 0.0
                    values[('XX', m, p)] = 0.0
                elif (m == 'x' and p == 'X') or (m == 'X' and p == 'x'):
                    values[('xx', m, p)] = 0.0
                    values[('xX', m, p)] = 1.0
                    values[('XX', m, p)] = 0.0
                else:
                    values[('xx', m, p)] = 0.0
                    values[('xX', m, p)] = 0.0
                    values[('XX', m, p)] = 1.0

        return Factor(variables, values)


    # TODO: Implement this for Question Eight. Any ideas? I'm trying to figure out what its supposed to return.
    # I think it's supposed to return the thing above (factor) which should just be a float, no?


def create_maternal_inheritance_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of the gene inherited from one's mother.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of the gene inherited from the family member's mother.
    """
    # TODO: Implement this for Question Nine.

    kid = person.get_name()
    mom = person.mother

    if mom is None:
        variables = [f"M_{kid}"]
        values = {('x',): 29999/30000, ('X',): 1/30000}
        return Factor(variables, values)
    
    
    variables = [f"M_{kid}", f"G_{mom.get_name()}"]
    values = {}

    for g in ['xx', 'xX', 'XX']:
        if g == 'xx':
            values[('x', g)] = 1.0
            values[('X', g)] = 0.0
        elif g == 'xX':
            values[('x', g)] = 0.5
            values[('X', g)] = 0.5
        else:
            values[('x', g)] = 0.0
            values[('X', g)] = 1.0

    return Factor(variables, values)


def create_paternal_inheritance_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of the gene inherited from one's father.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of the gene inherited from the family member's father.
    """
    # TODO: Implement this for Question Ten.

    kid = person
    dad = person.father

    if kid.get_sex() == "male":
        variables = [f"M_{kid.get_name()}"]
        values = {('y',): 1.0}
        return Factor(variables, values)
    
    else:
        if dad is None:
            variables = [f"P_{kid.get_name()}"]
            values = {('x',): 29999/30000, ('X',): 1/30000}
            return Factor(variables, values)
        
        variables = [f"P_{kid.get_name()}", f"G_{dad.get_name()}"]
        values = {}

        for g in ['xy', 'Xy']:
            if g == 'xy':
                values[('x', g)] = 1.0
                values[('X', g)] = 0.0
            else:
                values[('x', g)] = 0.0
                values[('X', g)] = 1.0

        return Factor(variables, values)


def create_family_bayes_net(family):
    """Creates a Bayesian network that models the genetic inheritance of hemophilia within a family.

    Parameters
    ----------
    family : list[FamilyMember]
        the members of the family

    Returns
    -------
    BayesianNetwork
        a Bayesian network that models the genetic inheritance of hemophilia within the specified family
    """
    domains = create_variable_domains(family)
    cpts = []
    for person in family:
        if person.get_sex() == "female":
            cpts.append(create_paternal_inheritance_cpt(person))
        cpts.append(create_maternal_inheritance_cpt(person))
        cpts.append(create_genotype_cpt(person))
        cpts.append(create_hemophilia_cpt(person))
    return BayesianNetwork(cpts, domains)
