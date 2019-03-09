import abc


class AbstractProblem(abc.ABC):
    """Abstract interface for a problem"""
    @abc.abstractmethod
    def chromosome_size(self):
        """ The chromosome size of the problem

        Returns:
            int: the chromosome size
        """
        ...

    @abc.abstractmethod
    def allele_count(self):
        """ The number of alleles

        Returns:
            int: the allele count
        """
        ...

    @abc.abstractmethod
    def create_individual(self, chromosome, fitness=None):
        """
        Creates an object of a subclass of AbstractIndividual
        Args:
            chromosome(array(list)): the chromosome of the individual
            fitness(float): already calculated fitness
        Returns:
            AbstractIndividual: the new individual
        """
        ...


class AbstractIndividual(abc.ABC):
    """Abstract interface for an Individual"""
    def __init__(self, problem, chromosome, fitness=None):
        """
        An individual of the population

        Args:
            problem(AbstractProblem): The according problem
            chromosome(list): the chromosome of the individual
            fitness(float): a already computed fitness value, which will be newly computed if None
        """
        self.problem = problem
        self.chromosome = chromosome
        if fitness is None:
            self.fitness = self._calculate_fitness()
        else:
            self.fitness = fitness

    @abc.abstractmethod
    def _calculate_fitness(self):
        """
        Calculate the fitness of the given chromosome

        Returns:
            int: the fitness
        """
        ...

    def mutate(self, mutator):
        """
        Mutates the individuals`s chromosome by using the given mutator
        Args:
            mutator: the mutator used for mutation
        """
        self.chromosome = mutator.mutate(self.chromosome)
        self.fitness = self._calculate_fitness()

    def __copy__(self):
        # to improve performance by not recalculating fitness each time a deepcopy gets made
        return self.problem.create_individual(self.chromosome.copy(), self.fitness)


class AbstractInitializer(abc.ABC):
    """Abstract interface for an Initializer yielding a method to create an initialized population"""
    def __init__(self, problem, population_size):
        """Initialize the Initializer

        Args:
            problem(AbstractProblem): the according problem
            population_size(int): the population size
        """
        self.problem = problem
        self.population_size = population_size

    @abc.abstractmethod
    def initialized_population(self):
        """Creates a population according to the parameters given in __init__

        Returns:
            list: a population as list of individuals
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
    def __init__(self, parent_count, crossover_probability):
        """
        Initialize the Recombiner
        Args:
            parent_count(int): the number of parents used in a recombination
            crossover_probability(float): the probability to really recombine
        """
        self.parent_count = parent_count
        self.crossover_probability = crossover_probability

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
    def __init__(self, mutation_probability, allele_count):
        """
        Initialize the Mutator

        Args:
            mutation_probability(float): probability for mutation
            allele_count(int): number of machines
        """
        self.mutation_probability = mutation_probability
        self.allele_count = allele_count

    @abc.abstractmethod
    def mutate(self, chromosome):
        """
        Mutate a chromosome

        Args:
            chromosome(list): the chromosome to mutate as list of gene-values
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
