def calculate_costs(all_orders, total_stock):
    #TODO this can be tweak for variety
    total_orders = [i[1] for i in all_orders]
    total_orders = [i for k in total_orders  for i in k]
    return total_stock - total_orders




def calculate_costs_in_stock(recipes_orders, portion_orders, all_stocks):
    sum_stocks = cal_current_stock(recipes_orders, portion_orders, all_stocks)
    all_stocks = {vk: vv for _, v in all_stocks.items() for vd in v for vk, vv in vd.items()}
    is_within_stock = [min(v-sum_stocks[k],0)  for (k, v) in all_stocks.items()]

    return sum(is_within_stock)


def cal_current_stock(recipes_orders, portion_orders, all_stocks):
    sum_stocks = {vk: 0  for _, v in all_stocks.items() for vd in v for vk, _ in vd.items()}  #crazy list comprehension to save time otherwise not recommend
    for k, v in recipes_orders.items():
        for s,t in zip(recipes_orders[k], portion_orders[k]):
            for (i,j) in zip(s,t):
                sum_stocks[i]+=j
    return sum_stocks


def print_best(recipes_orders, portion_orders, all_stocks):
    sum_stocks = cal_current_stock(recipes_orders, portion_orders, all_stocks)  #crazy list comprehension to save time otherwise not recommend
    all_stocks = {vk:vv  for _, v in all_stocks.items() for vd in v for vk,vv in vd.items()}

    print(sum_stocks)
    print(all_stocks)