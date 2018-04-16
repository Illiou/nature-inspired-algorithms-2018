import abc


class AbstractInitializer(abc.ABC):
    """Abstract interface for an Initializer yielding a method to create a random assignment"""
    def __init__(self, assignment_size, domain):
        """Initialize the Initializer

        Args:
            assignment_size(int): length of the initialized assignments
            domain(list): a list of all allowed gene-values
        """
        self.assignment_size = assignment_size
        self.domain = domain

    @abc.abstractmethod
    def initialized_assignment(self):
        """Creates an assignment according to the parameters given in __init__

        Returns:
            list: The assignment as a list of gene-values
        """
        ...


class AbstractSelector(abc.ABC):
    """Abstract interface for a Selector yielding a method to select n chromosomes from the population"""
    def __init__(self, selection_size):
        """
        Initialize the Selector

        Args:
            selection_size(int): the number of selected chromosomes
        """
        self.selection_size = selection_size

    @abc.abstractmethod
    def select_chromosomes(self, population):
        """
        Select chromosomes from population according to self.selection_size

        Args:
            population(list): a list of all chromosomes in the population
        Returns:
            a list of the selected chromosomes
        """
        ...


class AbstractRecombiner(abc.ABC):
    """Abstract interface for a Recombiner yielding a method to recombine parent-chromosomes to new chromosomes"""
    @abc.abstractmethod
    def recombine(self, parents):
        """
        Recombine the parent-chromosomes to get new offspring

        Args:
            parents(list): the parents used to recombine
        Returns:
            list: a list of offspring-chromosomes
        """
        ...


class AbstractMutator(abc.ABC):
    """Abstract interface for a Mutator yielding a method to mutate a single chromosome"""
    def __init__(self, mutation_probability):
        """
        Initialize the Mutator

        Args:
            mutation_probability(float): probability for mutation
        """
        self.mutation_probability = mutation_probability

    @abc.abstractmethod
    def mutate(self, assignment):
        """
        Mutate a chromosome

        Args:
            assignment(list): the assignment to mutate as list of gene-values
        Returns:
            list: the mutated chromosome
        """
        ...


class AbstractReplacer(abc.ABC):
    """
    Abstract interface for a Replacer yielding a method to replace the current population with the offspring-chromosomes
    """
    @abc.abstractmethod
    def replace(self, current_population, offspring):
        """

        Args:
            current_population(list): the current population
            offspring(list): list of offspring-chromosomes
        Returns:
            list: the new population
        """
        ...
