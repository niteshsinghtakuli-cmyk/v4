class TrendAI:
    def __init__(self):
        self.history = []

    def classify(self, n):
        return "BIG" if int(n) >= 5 else "SMALL"

    def update(self, results):
        self.history = results[:20]

    def predict(self):
        seq = [self.classify(x) for x in self.history]
        return "BIG" if seq.count("BIG") > seq.count("SMALL") else "SMALL"