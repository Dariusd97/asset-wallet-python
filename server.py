import json
from flask import Flask
import montecarlo
from model.MonteCarloReturn import MonteCarloReturn

app = Flask(__name__)

@app.route('/mc-sim')
async def home():
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

app.run(port=5000)