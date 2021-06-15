import json


class PortfolioOptimization(object):
    def __init__(self):
        self._method_name = None
        self._returns = None
        self._risk = None
        self._sharpe_ratio = None
        self._weights = None

    def to_dict(self):
        weights_list = []
        for i in range(len(self._weights)):
            weights_list.append(self._weights[i])
        return {'_method': self._method_name,
                '_returns': self._returns,
                '_risk': self._risk,
                '_sharpe_ratio': self._sharpe_ratio,
                '_weights': json.dumps(weights_list)
                }

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, value):
        self._weights = value

    @property
    def sharpe_ratio(self):
        return self._sharpe_ratio

    @sharpe_ratio.setter
    def sharpe_ratio(self, value):
        self._sharpe_ratio = value

    @property
    def risk(self):
        return self._risk

    @risk.setter
    def risk(self, value):
        self._risk = value

    @property
    def method_name(self):
        return self._method_name

    @method_name.setter
    def method_name(self, value):
        self._method_name = value

    @property
    def returns(self):
        return self._returns

    @returns.setter
    def returns(self, value):
        self._returns = value