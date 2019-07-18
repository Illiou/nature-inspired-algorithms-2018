import abc


class AbstractVehicleRoutingAlgorithm(abc.ABC):
    @abc.abstractmethod
    def run(self):
        """
        Running the algorithm and returning the solution for the problem
        Returns: (Solution) the solution to the VRP
        """
        pass
