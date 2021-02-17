
def is_unique_recipes(recipes_orders, portion_orders ):
    is_unique =[]

    #filter the recipe numbers

    for k,v in recipes_orders.items():
        recipes =[ [i for (i, j) in zip(s, t) if j >0 ] for s,t in zip(v, portion_orders[k])]
    #check if each one order has unique recipues
        uniq = [len(set(s)) == len(s) for s in recipes]
        is_unique.append(uniq)

    return all(is_unique)



def is_within_stock(recipes_orders, portion_orders, all_stocks):
    all_stocks = {s[0]:s[1] for s in all_stocks}
    sum_stocks = {k:0 for k in all_stocks.keys()}

    for s,t in zip(recipes_orders, portion_orders):
        for (i,j) in zip(s,t):
            sum_stocks[i]+=j

    is_within_stock= [sum_stocks[k] <= v for (k,v) in all_stocks.items()]

    return(all(is_within_stock))