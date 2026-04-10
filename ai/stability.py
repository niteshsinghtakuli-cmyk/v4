import random

class StabilityAI:
    def __init__(self):
        self.last = None

    def update(self, results):
        pass

    def predict(self):
        pred = random.choice(["BIG","SMALL"])

        if pred == self.last:
            pred = "SMALL" if pred == "BIG" else "BIG"

        self.last = pred
        return pred