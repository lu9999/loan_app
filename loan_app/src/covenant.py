
class Covenant:
    def __init__(self):
        self.max_default_likelihood = 1.0
        self.banned_state_set = set()

    def add_banned_state(self, state):
        self.banned_state_set.add(state)

    def add_max_default_likelihood(self, max_default_likelihood):
        if max_default_likelihood and max_default_likelihood != "" \
                and self.max_default_likelihood > float(max_default_likelihood):
            self.max_default_likelihood = max_default_likelihood

    def is_valid_state(self, state):
        return state not in self.banned_state_set

    def is_under_max_default_likelihood(self, default_likelihood):
        if default_likelihood and default_likelihood != "":
            return float(default_likelihood) < self.max_default_likelihood
        else:
            return False

    def covenant_requirements_met(self, loan):
        if self.is_valid_state(loan.state) and self.is_under_max_default_likelihood(loan.default_likelihood):
            return True
        else:
            return False
