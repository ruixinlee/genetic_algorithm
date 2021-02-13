
def is_unique_recipes(recipes_orders, portion_orders ):

    #filter the recipe numbers
    recipes =[ [i for (i, j) in zip(s, t) if j >0 ] for s,t in zip(recipes_orders, portion_orders)]
    #check if each one order has unique recipues
    is_unique = [len(set(s)) == len(s) for s in recipes]

    return all(is_unique)



def is_within_stock(recipes_orders, portion_orders, all_stocks):
    all_stocks = {s[0]:s[1] for s in all_stocks}
    sum_stocks = {k:0 for k in all_stocks.keys()}

    for s,t in zip(recipes_orders, portion_orders):
        for (i,j) in zip(s,t):
            sum_stocks[i]+=j

    is_within_stock= [sum_stocks[k] <= v for (k,v) in all_stocks.items()]

    return(all(is_within_stock))