from feasibility import RecipeAllocation

if __name__ == '__main__':

    stock_path = '.\\data\\defaults_stocks_feasible.json'
    orders_path = '.\\data\\defaults_orders.json'

    Feas = RecipeAllocation()
    Feas.load(orders_path,stock_path)
    is_feasible = Feas.search_feasibility()

    print('end')