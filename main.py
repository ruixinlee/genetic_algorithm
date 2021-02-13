import json
from utils.init_stocks_and_orders import init_orders, init_stock
from utils.costs import calculate_costs, calculate_costs_in_stock, print_best
from utils.constrains import is_unique_recipes
import random

def gen_parents(n_orders, recipes_lists, parents_num):
    n = 4
    parent_lists = []
    for c in range(parents_num):
        parent = [random.sample(recipes_lists,n) for i in range(n_orders)]
        parent_lists.append(parent)

    return parent_lists


def cross_gene(parent_lists,n_child,n_orders):

    mom_list = random.choices(parent_lists,k =n_child)
    dad_list = random.choices(parent_lists,k =n_child)
    binary = [0,1]
    children_list = []
    for ichild in range(n_child):
        dad = dad_list[ichild]
        mom = mom_list[ichild]
        dad_gene = random.choices(binary, k = n_orders)
        child = [dad[i] if dad_gene[i] ==1 else mom[i]  for i in range(n_orders)]
        children_list.append(child)
    return children_list

def mutate_gene(parent_lists, mutation_rate, n_orders, recipes_lists, mutation_counts):
    n_parents = len(parent_lists)

    binary = [0,1]
    cumulative_w = [1-mutation_rate, 1]
    if_mutate = random.choices(binary,cum_weights=cumulative_w, k=n_parents)

    total_mutates = sum(if_mutate)*mutation_counts
    mutate_locs = random.choices(range(n_orders), k=total_mutates)
    mutate_locs = [mutate_locs[i:i+mutation_counts] for i in range(0,total_mutates,mutation_counts)]

    new_genes =[]
    for k in range(total_mutates):
        new_genes.append(random.sample(recipes_lists, k=4))

    new_genes = [new_genes[i:i + mutation_counts] for i in range(0, total_mutates, mutation_counts)]

    if_mutate_iter = iter(if_mutate)
    mutate_loc_iter = iter(mutate_locs)
    mutate_gene_iter = iter(new_genes)

    mutated_parents_lists = []
    for p in parent_lists:
        if next(if_mutate_iter) == 1:
            mutate_loc = next(mutate_loc_iter)
            new_gene = next(mutate_gene_iter)
            for mi, mj in enumerate(mutate_loc):
                p[mj]= new_gene[mi]

        mutated_parents_lists.append(p)
    return mutated_parents_lists

def survive_children(parent_lists, portion_orders):
    parent_lists = [p for p in parent_lists if is_unique_recipes(p, portion_orders)]
    return parent_lists

def strongest_children(parent_lists,n_parents,  portion_orders, all_stocks):

    n_parents = min(n_parents, len(parent_lists))
    children_costs = [calculate_costs_in_stock(p,  portion_orders, all_stocks) for p in parent_lists]
    sorted_parents_lists = [i for _,i in sorted(zip(children_costs,parent_lists), reverse=True)]
    sorted_parents_lists =sorted_parents_lists[:n_parents]

    if calculate_costs_in_stock(sorted_parents_lists[0],portion_orders, all_stocks )< calculate_costs_in_stock(sorted_parents_lists[-1],portion_orders, all_stocks ):
        print('test')

    print(f'best- {calculate_costs_in_stock(sorted_parents_lists[0],portion_orders, all_stocks )}, worst {calculate_costs_in_stock(sorted_parents_lists[-1],portion_orders, all_stocks)}')
    return sorted_parents_lists


if __name__ == '__main__':

    with open('.\\data\\defaults_stocks.json', 'r') as f:
        stocks = json.load(f)
    with open('.\\data\\defaults_orders.json', 'r') as f:
        orders = json.load(f)



    orders = orders['vegetarian']
    stocks = {i: k for i, k in stocks.items() if k['box_type'] == 'vegetarian'}

    recipes_orders, portion_orders = init_orders(orders)
    all_stocks = init_stock(stocks) # these are constraints
    recipes_lists = [s[0] for s in all_stocks]
    n_orders = len(recipes_orders)


    num_iteration = 1000
    parents_num = 100
    n_child = 1000
    mutation_rate = 0.3
    mutation_counts = int(n_orders*0.3)

    parent_lists = gen_parents(n_orders, recipes_lists, parents_num)
    for i in range(50):
        print('find surviving children')
        # print(set([len(i) for r  in parent_lists for i in r]))
        # parent_lists = survive_children(parent_lists,portion_orders)
        print('find strongest_children')
        # print(set([len(i) for r  in parent_lists for i in r]))
        parent_lists = strongest_children(parent_lists, parents_num, portion_orders, all_stocks)
        print('breed')
        # print(set([len(i) for r  in parent_lists for i in r]))
        parent_lists = cross_gene(parent_lists, n_child, n_orders)
        print('mutate')
        # print(set([len(i) for r  in parent_lists for i in r]))
        parent_lists = mutate_gene(parent_lists, mutation_rate, n_orders, recipes_lists, mutation_counts)
        # print_best(parent_lists[0], portion_orders, all_stocks)

print('test')