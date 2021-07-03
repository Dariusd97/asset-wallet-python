import json
from flask import Flask, request
import montecarlo
from model.MonteCarloReturn import MonteCarloReturn
from portfolio_optimization import portfolio_alloc_and_opt

app = Flask(__name__)

@app.route('/mc-sim')
async def mc_sim():
    start = "2015-1-1"
    days_to_forecast = 252
    simulation_trials = 10000
    monteCarloReturn = MonteCarloReturn()
    stocks = ['GOOG', 'AAPL', 'PATH']
    mc_list = await montecarlo.monte_carlo(stocks, days_to_forecast, simulation_trials,monteCarloReturn, start_date=start, plotten=False)
    for i in range(len(mc_list)):
        mc_list[i].symbol = stocks[i]
    results = [a.to_dict() for a in mc_list]
    json_data = json.dumps({'results': results})
    return json_data

@app.route('/portfolio-sim', methods=['GET'])
async def portfolio_sim():
    stocks = []
    if request.args.get("stock1") is not None:
        stocks.append(request.args.get("stock1"))
    if request.args.get("stock2") is not None :
        stocks.append(request.args.get("stock2"))
    if request.args.get("stock3") is not None:
        stocks.append(request.args.get("stock3"))
    if request.args.get("stock4") is not None:
        stocks.append(request.args.get("stock4"))

    number_of_portfolios = 100

    a,b = await portfolio_alloc_and_opt(stocks, number_of_portfolios)
    json_data = json.dumps({'method_1': a.to_dict(), 'method_2':b.to_dict()})
    return json_data

#app.run(port=5000)