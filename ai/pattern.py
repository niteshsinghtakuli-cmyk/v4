import random

class PatternAI:
    def __init__(self):
        self.history = []

    def classify(self, n):
        return "BIG" if int(n) >= 5 else "SMALL"

    def update(self, results):
        self.history = results[:6]

    def predict(self):
        if len(self.history) < 6:
            return random.choice(["BIG","SMALL"])

        seq = [self.classify(x) for x in self.history]

        if all(x == "BIG" for x in seq):
            return "SMALL"
        if all(x == "SMALL" for x in seq):
            return "BIG"

        return random.choice(["BIG","SMALL"])