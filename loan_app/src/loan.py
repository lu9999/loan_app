
class Loan:
    def __init__(self, id, interest_rate, amount, default_likelihood, state):
        self.id = id
        self.interest_rate = float(interest_rate)
        self.amount = float(amount)
        self.default_likelihood = float(default_likelihood)
        self.state = state
        self.facility_id = None

    def set_facility_id(self, id):
        self.facility_id = id
