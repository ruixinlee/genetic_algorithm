import json
import random
from datetime import datetime
import time

class RecipeAllocation:

    def __init__(self, num_iteration = 1000, parents_num = 100 ,n_child = 1000, mutation_rate = 0.3):
        self.num_iteration  = num_iteration
        self.parents_num    = parents_num
        self.n_child        = n_child
        self.mutation_rate  = mutation_rate
        self.search_stop   = 5

        self.max_recipe = 4
        self.stock = None
        self.orders = None

        self.all_stocks = None
        self.all_stocks_flatten = None
        self.recipes_orders = None  #all orders in recipes
        self.portion_orders = None  #all orders in portions
        self.n_orders = None
        self.is_feasible = None

        self.parent_lists = None
        self.feasible_parent = None
        self.log(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} begin class')

    def load(self, orders_json, stocks_json):
        """
        to load orders and stock_json
        :param orders: path of the json file for orders
        :param stocks:path of the json file for stock
        :return:
        """

        with open(orders_json, 'r') as f:
            self.orders = json.load(f)

        with open(stocks_json, 'r') as f:
            self.stocks = json.load(f)

        ## check if recipes types are compatibles
        try:
            order_types = list(self.orders.keys())
            stock_types = list(set([v['box_type'] for v in self.stocks.values()]))
            is_available = [i not in stock_types for i in order_types]
            if any(is_available):
                raise Exception('Error: incompatible recipes types')
        except Exception as e:
            self.log(str(e))

        self.log('loaded jsons')

        self.init_orders()
        self.init_stocks()  # these are constraints

    def log(self,text):
        print(text)
        with open('./data/log.txt', 'a') as f:
            f.write(text + '\n')

    def init_orders(self):
        # TODO test sum is equal

        r_hold = ['recipe_1', 'recipe_1', 'recipe_1', 'recipe_1']

        p_placehold = {
            'two_recipes': {'two_portions': [2, 2, 0, 0], 'four_portions': [4, 4, 0, 0]},
            'three_recipes': {'two_portions': [2, 2, 2, 0], 'four_portions': [4, 4, 4, 0]},
            'four_recipes': {'two_portions': [2, 2, 2, 2], 'four_portions': [4, 4, 4, 4]}
        }

        recipes_orders = {}
        portion_orders = {}

        for k_type, v_type in self.orders.items():
            portion_orders[k_type] = []
            recipes_orders[k_type] = []

            for k_recipes, v_recipes in v_type.items():
                for k_portion, v_portion in v_recipes.items():
                    p_hold = p_placehold[k_recipes][k_portion]

                    portion_orders[k_type].extend([p_hold] * v_portion)
                    recipes_orders[k_type].extend([r_hold] * v_portion)

        self.recipes_orders = recipes_orders
        self.portion_orders = portion_orders
        self.n_orders = sum([len(v) for k, v in self.recipes_orders.items()])

        self.log('initiated orders and recipes')

    def init_stocks(self):
        all_stocks = {}
        for (k, v) in self.stocks.items():
            if all_stocks.get(v['box_type']):
                all_stocks[v['box_type']].append({k: v['stock_count']})
            else:
                all_stocks[v['box_type']] = [{k: v['stock_count']}]

        self.all_stocks =all_stocks

        recipes_lists = {k: [list(i.keys())[0] for i in v] for k, v in all_stocks.items()}
        recipes_lists['gourmet'] = recipes_lists['vegetarian'] + recipes_lists['gourmet']

        self.recipes_lists = recipes_lists
        self.all_stocks_flatten = {vk: vv for _, v in all_stocks.items() for vd in v for vk, vv in vd.items()}
        self.log('initiate stocks')

    def generate_parents(self):
        all_stocks  = self.all_stocks
        parents_num = self.parents_num
        recipes_orders = self.recipes_orders
        recipes_lists = self.recipes_lists
        parent_lists = []

        for n in range(parents_num):
            parent = {}
            for k, v in recipes_orders.items():
                if k == 'vegetarian':
                    n_orders = len(recipes_orders[k])
                    parent[k] = [random.sample(recipes_lists[k], self.max_recipe) for i in range(n_orders)]
                if k == 'gourmet':
                    n_orders = len(recipes_orders[k])
                    parent[k] = [random.sample(recipes_lists[k], self.max_recipe) for i in range(n_orders)]

            parent_lists.append(parent)

        self.parent_lists = parent_lists

    def cross_gene(self):
        parent_lists = self.parent_lists
        n_child = self.n_child
        mom_list = random.choices(parent_lists, k=n_child)
        dad_list = random.choices(parent_lists, k=n_child)
        binary = [0, 1]
        children_list = []
        for ichild in range(n_child):
            dad = dad_list[ichild]
            mom = mom_list[ichild]
            child = {}
            for k, v in dad.items():
                n_orders = len(v)
                dad_gene = random.choices(binary, k=n_orders)
                child[k] = [dad[k][i] if dad_gene[i] == 1 else mom[k][i] for i in range(n_orders)]
            children_list.append(child)

        self.parent_lists = children_list

    def mutate_gene(self):
        parent_lists = self.parent_lists
        mutation_rate = self.mutation_rate
        max_recipe = self.max_recipe
        parents_num = self.parents_num
        recipes_lists = self.recipes_lists

        mutation_counts = int(self.n_orders * self.mutation_rate)
        binary = [0, 1]
        cumulative_w = [1 - mutation_rate, 1]
        is_mutate_parent = random.choices(binary, cum_weights=cumulative_w, k=parents_num)

        mutated_parents_lists = []

        for is_mutate, parent in zip(is_mutate_parent, parent_lists):
            if is_mutate:
                for k, v in parent.items():
                    n_orders = len(v)
                    mutate_locs = random.choices(range(n_orders), k=mutation_counts)
                    mutated_gene = random.choices(recipes_lists[k],
                                                  k=mutation_counts * max_recipe)
                    mutated_gene = [mutated_gene[i:i + max_recipe] for i in
                                    range(0, mutation_counts * max_recipe, max_recipe)]

                    for ml, mg in zip(mutate_locs, mutated_gene):
                        v[ml] = mg

                    parent[k] = v
            mutated_parents_lists.append(parent)
        self.parent_lists = mutated_parents_lists

    def survive_children(self):
        # TODO: check if veg only get veg
        parent_lists = self.parent_lists
        portion_orders = self.portion_orders
        parent_lists = [p for p in parent_lists if self.__class__.is_unique_recipes(p, portion_orders)]

        self.parent_lists =parent_lists

    def strongest_children(self):

        parent_lists    = self.parent_lists
        parents_num       = self.parents_num
        portion_orders  = self.portion_orders
        all_stocks      = self.all_stocks
        n_parents       = min(parents_num, len(parent_lists))

        parent_lists = sorted(parent_lists, key=lambda i: self.__class__.calculate_costs_in_stock(i, portion_orders, all_stocks),
                               reverse=True)

        parent_lists = parent_lists[:n_parents]

        print(
            f'best profit- { self.__class__.calculate_costs_in_stock(self.parent_lists[0], portion_orders, all_stocks)}, worst { self.__class__.calculate_costs_in_stock(self.parent_lists[-1], portion_orders, all_stocks)}')
        self.parent_lists = parent_lists

    def search_feasibility(self):

        tic = time.time()
        self.generate_parents()
        self.survive_children()
        self.strongest_children()
        generation = 0

        cost_paths = []

        while True:

            self.cross_gene()
            self.strongest_children()
            self.mutate_gene()
            self.strongest_children()
            self.survive_children()
            self.strongest_children()

            best_parent = self.parent_lists[0]
            worst_parent = self.parent_lists[-1]
            best_parent_costs = self.__class__.calculate_costs_in_stock(best_parent, self.portion_orders, self.all_stocks )
            worst_parent_costs = self.__class__.calculate_costs_in_stock(worst_parent, self.portion_orders, self.all_stocks )
            best_stock_level = self.__class__.cal_current_stock(best_parent, self.portion_orders, self.all_stocks)
            generation += 1

            cost_paths.append(best_parent_costs)
            if len(cost_paths)> self.search_stop:
                cost_paths_mov = [j-i for i,j in zip(cost_paths[:-1], cost_paths[1:])]
                which_constant = [1 if i <= 0 else 0 for i in cost_paths_mov]
                self.log(f'is the solution worse off than the present one? : {which_constant}')

                if sum(which_constant[-self.search_stop:]) == self.search_stop:
                    self.log(f'no feasible solution found, costs remain constant for {self.search_stop} steps')
                    self.is_feasible = False
                    return self.is_feasible

            toc = time.time()
            self.log(f'created generation {generation} in {toc - tic} seconds')
            self.log(f'best parent has cost {best_parent_costs}, worst parent has cost {worst_parent_costs}')
            self.log(f'best parent stock level is:   {best_stock_level}')
            self.log(f'current stock level is:       {self.all_stocks_flatten}')
            self.log(' ')





            if best_parent_costs >=0:
                self.feasible_parent = best_parent
                self.log(f'feasible solution found, cost is {best_parent_costs}')
                self.log(f'current stock level is   {self.all_stocks_flatten}')
                self.log(f'feasible stock level is  {best_stock_level}')
                self.is_feasible = True
                return True

    @classmethod
    def is_unique_recipes(cls, recipes_orders, portion_orders):
        is_unique = []

        # filter the recipe numbers

        for k, v in recipes_orders.items():
            recipes = [[i for (i, j) in zip(s, t) if j > 0] for s, t in zip(v, portion_orders[k])]
            # check if each one order has unique recipues
            uniq = [len(set(s)) == len(s) for s in recipes]
            is_unique.append(uniq)

        return all(is_unique)

    @classmethod
    def is_within_stock(cls,recipes_orders, portion_orders, all_stocks):
        all_stocks = {s[0]: s[1] for s in all_stocks}
        sum_stocks = {k: 0 for k in all_stocks.keys()}

        for s, t in zip(recipes_orders, portion_orders):
            for (i, j) in zip(s, t):
                sum_stocks[i] += j

        is_within_stock = [sum_stocks[k] <= v for (k, v) in all_stocks.items()]

        return (all(is_within_stock))

    @classmethod
    def calculate_costs_in_stock(cls,recipes_orders, portion_orders, all_stocks):
        sum_stocks = cls.cal_current_stock(recipes_orders, portion_orders, all_stocks)
        all_stocks = {vk: vv for _, v in all_stocks.items() for vd in v for vk, vv in vd.items()}
        is_within_stock = [min(v - sum_stocks[k], 0) for (k, v) in all_stocks.items()]

        return sum(is_within_stock)

    @classmethod
    def cal_current_stock(cls,recipes_orders, portion_orders,all_stocks):

        sum_stocks = {vk: 0 for _, v in all_stocks.items() for vd in v for vk, _ in
                      vd.items()}  # crazy list comprehension to save time otherwise not recommend
        for k, v in recipes_orders.items():
            for s, t in zip(recipes_orders[k], portion_orders[k]):
                for (i, j) in zip(s, t):
                    sum_stocks[i] += j
        return sum_stocks

if __name__ == '__main__':

    stock_path = '.\\data\\defaults_stocks.json'
    orders_path = '.\\data\\defaults_orders.json'

    Feas = RecipeAllocation()
    Feas.load(orders_path,stock_path)
    is_feasible = Feas.search_feasibility()

    print('test')

