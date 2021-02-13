def calculate_costs(all_orders, total_stock):
    #TODO this can be tweak for variety
    total_orders = [i[1] for i in all_orders]
    total_orders = [i for k in total_orders  for i in k]
    return total_stock - total_orders




def calculate_costs_in_stock(recipes_orders, portion_orders, all_stocks):
    all_stocks = {s[0]:s[1] for s in all_stocks}
    sum_stocks = {k:0 for k in all_stocks.keys()}

    for s,t in zip(recipes_orders, portion_orders):
        for (i,j) in zip(s,t):
            sum_stocks[i]+=j

    is_within_stock = [min(v-sum_stocks[k],0)  for (k, v) in all_stocks.items()]

    return sum(is_within_stock)

def print_best(recipes_orders, portion_orders, all_stocks):
    all_stocks = {s[0]:s[1] for s in all_stocks}
    sum_stocks = {k:0 for k in all_stocks.keys()}

    for s,t in zip(recipes_orders, portion_orders):
        for (i,j) in zip(s,t):
            sum_stocks[i]+=j

    print(sum_stocks)
    print(all_stocks)