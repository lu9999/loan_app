from src.covenant import Covenant
from src.loan import Loan


class Facility:
    def __init__(self, id, amount, interest_rate, bank_id, covenant):
        self.id = id
        self.amount = float(amount)
        self.interest_rate = float(interest_rate)
        self.bank_id = bank_id
        self.covenant = None
        self.set_covenant(covenant)
        self.expected_yield = 0

    def set_covenant(self, covenant):
        if isinstance(covenant, Covenant):
            self.covenant = covenant

    # strategy 1
    def check_expect_yield_for_new_loan(self, loan):
        expected_yield = (1 - loan.default_likelihood) * loan.interest_rate * loan.amount \
                         - loan.default_likelihood * loan.amount \
                         - self.interest_rate * loan.amount
        return expected_yield

    def strategy_2(self, loan):
        expected_yield = (1 - loan.default_likelihood) * loan.interest_rate * loan.amount \
                         - loan.default_likelihood * loan.amount \
                         - self.interest_rate * loan.amount
        return expected_yield / loan.amount

    def strategy_3(self, loan, ratio=1.0):
        expected_yield = (1 - loan.default_likelihood) * loan.interest_rate * loan.amount \
                         - loan.default_likelihood * loan.amount \
                         - self.interest_rate * loan.amount

        amount_ratio = loan.amount / self.amount * ratio
        return expected_yield / loan.amount + amount_ratio

    def check_new_loan(self, loan):
        if isinstance(loan, Loan) and loan.amount <= self.amount:
            if self.covenant.covenant_requirements_met(loan):
                return True
        return False

    def add_new_loan(self, loan):
        if self.check_new_loan(loan):
            expected_yield = self.check_expect_yield_for_new_loan(loan)
            self.expected_yield += expected_yield
            self.amount -= loan.amount
            return True
        return False
