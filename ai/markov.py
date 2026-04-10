import random

class MarkovAI:
    def __init__(self):
        self.transitions = {
            "BIG": {"BIG":1, "SMALL":1},
            "SMALL": {"BIG":1, "SMALL":1}
        }
        self.history = []

    def classify(self, n):
        return "BIG" if int(n) >= 5 else "SMALL"

    def update(self, results):
        self.history = results[:50]

        for i in range(len(self.history)-1):
            a = self.classify(self.history[i])
            b = self.classify(self.history[i+1])
            self.transitions[a][b] += 1

    def predict(self):
        if len(self.history) < 2:
            return random.choice(["BIG","SMALL"]), 50

        last = self.classify(self.history[0])

        big = self.transitions[last]["BIG"]
        small = self.transitions[last]["SMALL"]

        total = big + small

        if big > small:
            return "BIG", int(big/total*100)
        else:
            return "SMALL", int(small/total*100)