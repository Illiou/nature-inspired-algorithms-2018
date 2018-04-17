from Week_2.AbstractModules import AbstractReplacer


class PseudoReplacer(AbstractReplacer):
    def replace(self, current_population, offspring):
        return offspring[:len(current_population)]