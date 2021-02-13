
def init_orders(orders):
    #per_order = [[allocated recipes],[fixed portions]]
    #TODO test sum is equal
    all_orders = []
    recipe2_portion2 = [[['recipe_1','recipe_1','recipe_1','recipe_1'],[2,2,0,0]]]
    recipe2_portion4 = [[['recipe_1','recipe_1','recipe_1','recipe_1'],[4,4,0,0]]]

    recipe3_portion2 = [[['recipe_1','recipe_1','recipe_1','recipe_1'],[2,2,2,0]]]
    recipe3_portion4 = [[['recipe_1','recipe_1','recipe_1','recipe_1'],[4,4,4,0]]]

    recipe4_portion2 = [[['recipe_1','recipe_1','recipe_1','recipe_1'],[2,2,2,0]]]
    recipe4_portion4 = [[['recipe_1','recipe_1','recipe_1','recipe_1'],[4,4,4,0]]]

    all_orders.extend(recipe2_portion2*orders['two_recipes']['two_portions'])
    all_orders.extend(recipe2_portion4*orders['two_recipes']['four_portions'])
    all_orders.extend(recipe3_portion2*orders['three_recipes']['two_portions'])
    all_orders.extend(recipe3_portion4*orders['three_recipes']['four_portions'])
    all_orders.extend(recipe4_portion2*orders['four_recipes']['two_portions'])
    all_orders.extend(recipe4_portion4*orders['four_recipes']['four_portions'])

    recipes_orders = [['recipe_1','recipe_1','recipe_1','recipe_1']]*len(all_orders)
    portion_orders = [s[1] for s in all_orders]
    return(recipes_orders,portion_orders )

def init_stock(stocks):
    all_stocks = []
    for (k,v) in stocks.items():
        all_stocks.append([k,v['stock_count']])

    return all_stocks