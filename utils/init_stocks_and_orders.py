
def init_orders(orders):
    #per_order = [[allocated recipes],[fixed portions]]
    #TODO test sum is equal
    r_hold = ['recipe_1', 'recipe_1', 'recipe_1', 'recipe_1']

    p_placehold = {
        'two_recipes': {'two_portions': [2, 2, 0, 0], 'four_portions': [4, 4, 0, 0]},
        'three_recipes': {'two_portions': [2, 2, 2, 0], 'four_portions': [4, 4, 4, 0]},
        'four_recipes': {'two_portions': [2, 2, 2, 2], 'four_portions': [4, 4, 4, 4]}
    }

    recipes_orders = {}
    portion_orders = {}

    for k_type, v_type in orders.items():
        portion_orders[k_type] = []
        recipes_orders[k_type] = []

        for k_recipes, v_recipes in v_type.items():
            for k_portion, v_portion in v_recipes.items():
                p_hold = p_placehold[k_recipes][k_portion]

                portion_orders[k_type].extend([p_hold] * v_portion)
                recipes_orders[k_type].extend([r_hold] * v_portion)

    return(recipes_orders,portion_orders )

def init_stock(stocks):
    all_stocks = {}
    for (k,v) in stocks.items():
        if all_stocks.get(v['box_type']):
            all_stocks[v['box_type']].append({k: v['stock_count']})
        else:
            all_stocks[v['box_type']] = [{k: v['stock_count']}]

    return all_stocks