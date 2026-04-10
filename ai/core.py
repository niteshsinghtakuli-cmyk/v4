from ai.markov import MarkovAI
from ai.trend import TrendAI
from ai.pattern import PatternAI
from ai.stability import StabilityAI

class AICore:
    def __init__(self):
        self.markov = MarkovAI()
        self.trend = TrendAI()
        self.pattern = PatternAI()
        self.stability = StabilityAI()

    def update(self, results):
        self.markov.update(results)
        self.trend.update(results)
        self.pattern.update(results)
        self.stability.update(results)

    def predict(self):
        m_pred, m_conf = self.markov.predict()
        t_pred = self.trend.predict()
        p_pred = self.pattern.predict()
        s_pred = self.stability.predict()

        votes = [m_pred, t_pred, p_pred, s_pred]

        big = votes.count("BIG")
        small = votes.count("SMALL")

        final = "BIG" if big > small else "SMALL"
        confidence = int((max(big, small) / 4) * 100)

        return {
            "final": final,
            "confidence": confidence,
            "bots": {
                "markov": f"{m_pred} ({m_conf}%)",
                "trend": t_pred,
                "pattern": p_pred,
                "stability": s_pred
            }
        }