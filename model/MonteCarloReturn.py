class MonteCarloReturn(object):
    def __init__(self):
        self._symbol = None
        self._days = None
        self._expected_value = None
        self._returns = None
        self._prob_breakeven = None
        self._beta = None
        self._sharpe = None
        self._capm_return = None

    def to_dict(self):
        return {'symbol': self._symbol,
                'days': self._days,
                'expected_value': self._expected_value,
                'returns': self._returns,
                '_prob_breakeven': self._prob_breakeven,
                'beta': self._beta,
                'sharpe': self._sharpe,
                'capm_return': self._capm_return
                }
    @property
    def capm_return(self):
        return self._capm_return

    @capm_return.setter
    def capm_return(self, value):
        self._capm_return = value

    @property
    def sharpe(self):
        return self._sharpe

    @sharpe.setter
    def sharpe(self, value):
        self._sharpe = value

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, value):
        self._beta = value

    @property
    def prob_breakeven(self):
        return self._prob_breakeven

    @prob_breakeven.setter
    def prob_breakeven(self, value):
        self._prob_breakeven = value

    @property
    def returns(self):
        return self._returns

    @returns.setter
    def returns(self, value):
        self._returns = value

    @property
    def expected_value(self):
        return self._expected_value

    @expected_value.setter
    def expected_value(self, value):
        self._expected_value = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, value):
        self._days = value

