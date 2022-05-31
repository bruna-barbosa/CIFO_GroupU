from copy import deepcopy
from charles.search import hill_climb, sim_annealing
from charles.selection import fps, tournament
from charles.mutation import inversion_mutation, binary_mutation, swap_mutation, replace_mutation
from charles.crossover import single_point_co, cycle_co, pmx_co, arithmetic_co
from init_board import valid_init_boards
from classes import Individual, Population
from main import check_box, check_col, check_row
from random import choice

def get_fitness(self):
    """A fitness function for the Sudoku Problem.
        Calculates the fitness of rows, columns and blocks in terms of repetition and sum
    Returns:
        int: the closer to 0 the better
    """

    boxs = [self.get_box(i) for i in range(9)]
    rows = [self.get_row(i) for i in range(9)]
    cols = [self.get_col(i) for i in range(9)]

    result = 0

    '''for box in boxs:
        for index, value in enumerate(box):
            for index_, value_ in enumerate(box):
                if index == index_:
                    pass
                else:
                    if (value == 0) | (value == value_):
                        result += 1'''

    for row in range(len(rows)):
        result += self.get_row_fit(row)

    for col in range(len(cols)):
        result += self.get_col_fit(col)

    return result


def get_neighbours(self):
    """A neighbourhood function for the Sudoku Problem.
    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for _ in range(9)]

    for count, i in enumerate(n):
        if i[count] == 1:
            i[count] = 0
        elif i[count] == 0:
            i[count] = 1
    '''for rep in n:
        for i in rep.mutable_indexes:
            if rep.representation[i] == 0:
                rep.representation[i] = choice(rep.valid_set)'''


    return [Individual(i) for i in n]


# Monkey Patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

first_board = choice(valid_init_boards)

pop = Population(size=50, optim="min", init_repr=first_board[0], mutable_indexes=first_board[1], valid_set=[i for i in range(1, 10)])

pop.evolve(gens=200,
           select=tournament,
           crossover=single_point_co,
           mutate=inversion_mutation,
           co_p=0.9, mu_p=0.1,
           elitism=True)
