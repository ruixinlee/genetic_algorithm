import json
from utils.init_stocks_and_orders import init_orders, init_stock
from utils.costs import calculate_costs, calculate_costs_in_stock, print_best
from utils.constrains import is_unique_recipes
import random

#TODO: distributed GE
#TODO: mutation rate and number that decrease with improvement in costs
#TODO: edge cases - how long until we decide there is no solition?
#TODO: sampling too equal - sampling can change according to split of stock
#TODO: edge cases - sum_orders > sum_ stock

def gen_parents(all_stocks, parents_num):
    max_recipe = 4
    recipes_lists = {k:[list(i.keys())[0] for i in v] for k,v in all_stocks.items()}
    recipes_lists['gourmet'] = recipes_lists['vegetarian'] + recipes_lists['gourmet']
    parent_lists = []


    for n in range(parents_num):
        parent = {}
        for k,v in recipes_orders.items():
            if k == 'vegetarian':
                n_orders = len(recipes_orders[k])
                parent[k] = [random.sample(recipes_lists[k],max_recipe) for i in range(n_orders)]
            if k == 'gourmet':
                n_orders = len(recipes_orders[k])
                parent[k] = [random.sample(recipes_lists[k], max_recipe) for i in range(n_orders)]

        parent_lists.append(parent)

    return parent_lists


def cross_gene(parent_lists,n_child):

    mom_list = random.choices(parent_lists,k =n_child)
    dad_list = random.choices(parent_lists,k =n_child)
    binary = [0,1]
    children_list = []
    for ichild in range(n_child):
        dad = dad_list[ichild]
        mom = mom_list[ichild]
        child = {}
        for k,v in dad.items():
            n_orders = len(v)
            dad_gene = random.choices(binary, k = n_orders)
            child[k] = [dad[k][i] if dad_gene[i] ==1 else mom[k][i]  for i in range(n_orders)]
        children_list.append(child)
    return children_list

def mutate_gene(parent_lists, mutation_rate, all_stocks, n_orders,mutation_counts):
    max_recipe = 4
    n_parents = len(parent_lists)

    recipes_lists = {k: [list(i.keys())[0] for i in v] for k, v in all_stocks.items()}
    recipes_lists['gourmet'] = recipes_lists['vegetarian'] + recipes_lists['gourmet']
    binary = [0,1]
    cumulative_w = [1-mutation_rate, 1]
    is_mutate_parent = random.choices(binary,cum_weights=cumulative_w, k=n_parents)

    mutated_parents_lists = []

    for is_mutate, parent in zip(is_mutate_parent,parent_lists):
        if is_mutate:
            for k,v in parent.items():
                n_orders = len(v)
                mutate_locs = random.choices(range(n_orders), k=mutation_counts)
                mutated_gene = random.choices(recipes_lists[k],  k=mutation_counts*max_recipe)
                mutated_gene = [mutated_gene[i:i+max_recipe] for i in range(0,mutation_counts*max_recipe,max_recipe)]

                for ml, mg in zip(mutate_locs, mutated_gene):
                    v[ml] = mg

                parent[k] = v
        mutated_parents_lists.append(parent)
    return mutated_parents_lists

def survive_children(parent_lists, portion_orders):
    #TODO: check if veg only get veg
    parent_lists = [parent for parent in parent_lists if is_unique_recipes(parent, portion_orders)]

    return parent_lists

def strongest_children(parent_lists,n_parents,  portion_orders, all_stocks):

    n_parents = min(n_parents, len(parent_lists))

    parents_lists = sorted(parent_lists, key = lambda i: calculate_costs_in_stock(i,  portion_orders, all_stocks),reverse=True)

    parents_lists =parents_lists[:n_parents]


    print(f'best- {calculate_costs_in_stock(parents_lists[0],portion_orders, all_stocks )}, worst {calculate_costs_in_stock(parents_lists[-1],portion_orders, all_stocks)}')
    return parents_lists


if __name__ == '__main__':

    with open('.\\data\\defaults_stocks.json', 'r') as f:
        stocks = json.load(f)
    with open('.\\data\\defaults_orders.json', 'r') as f:
        orders = json.load(f)

    recipes_orders, portion_orders = init_orders(orders)
    all_stocks = init_stock(stocks) # these are constraints
    n_orders = sum([len(v) for k,v in recipes_orders.items()])


    num_iteration = 1000
    parents_num = 100
    n_child = 1000
    mutation_rate = 0.3
    mutation_counts = int(n_orders*0.3)

    parent_lists = gen_parents(all_stocks, parents_num)
    for i in range(50):
        print('find surviving children')
        # print(set([len(i) for r  in parent_lists for i in r]))
        parent_lists = survive_children(parent_lists,portion_orders)
        print('find strongest_children')
        # print(set([len(i) for r  in parent_lists for i in r]))
        parent_lists = strongest_children(parent_lists, parents_num, portion_orders, all_stocks)
        print('breed')
        # print(set([len(i) for r  in parent_lists for i in r]))
        parent_lists = cross_gene(parent_lists, n_child)
        print('mutate')
        # print(set([len(i) for r  in parent_lists for i in r]))
        parent_lists = mutate_gene(parent_lists, mutation_rate, all_stocks, n_orders,mutation_counts)
        print_best(parent_lists[0], portion_orders, all_stocks)

print('test')