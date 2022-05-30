from charles.charles import Population, Individual
from copy import deepcopy
from data.sudoku_data import values
from charles.selection import fps, tournament, ranking
from charles.mutation import replace_mutation, swap_mutation
from charles.crossover import single_point_co, cycle_co
from numpy import std


def get_fitness(self):
    """A fitness function for the Sudoku Problem.
    Calculates the fitness of rows, columns and blocks in terms of repetition and sum

    Returns:
        int: the closer to 0 the better
    """

    rows = 0
    columns = 0
    blocks = 0

    for i in range(9):
        sum = 0
        for j in range(9):
            sum = sum + self.representation[i * 9 + j]
        rows = rows + abs(sum - 45)

    for i in range(9):
        sum = 0
        for j in range(9):
            sum = sum + self.representation[i + j * 9]
        columns = columns + abs(sum - 45)

    for box_num in range(9):
        row = 3 * int(box_num / 3)
        col = 3 * (box_num % 3)
        sum = 0
        for i in range(row, row + 3):
            for j in range(col, col + 3):
                sum = sum + self.representation[i * 9 + j]
        blocks = blocks + abs(sum - 45)

    return rows + columns + blocks


def get_neighbours(self):
    """A neighbourhood function for the Sudoku Problem.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation))]

    for count, i in enumerate(n):
        if i[count] == 1:
            i[count] = 0
        elif i[count] == 0:
            i[count] = 1

    n = [Individual(i) for i in n]
    return n


# Monkey Patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours


def check_setting(
        size,
        gens,
        select,
        crossover,
        mutate,
        co_p,
        mu_p,
        elitism
):
    total_runs = 10
    pop = Population(
        size=size, optim="min", init_repr=deepcopy(values), valid_set=[1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    fitness = []
    for _ in range(total_runs):
        fitness.append(
            pop.evolve(
                gens=gens,
                select=select,
                crossover=crossover,
                mutate=mutate,
                co_p=co_p,
                mu_p=mu_p,
                elitism=elitism
            )
        )
    print(f"Select: {select.__name__}")
    print(f"Crossover: {crossover.__name__}")
    print(f"Mutation: {mutate.__name__}")
    print(f"Elitism: {elitism}")
#    print(f"Solutions: {fitness}")
    print(f"Best solution: {min(fitness)}")
    print(f"Average solution: {sum(fitness) / total_runs}")
    print(f"Std: {std(fitness)}")


def total_check():
    selections = [fps, tournament, ranking]
    crossovers = [single_point_co, cycle_co]
    mutations = [swap_mutation, replace_mutation]

    for s, c, m in [
        (s, c, m)
        for s in selections
        for c in crossovers
        for m in mutations
    ]:
        check_setting(
            size=50,
            gens=1000,
            select=s,
            crossover=c,
            mutate=m,
            co_p=0.8,
            mu_p=0.2,
            elitism=True
        )
        print()


total_check()
