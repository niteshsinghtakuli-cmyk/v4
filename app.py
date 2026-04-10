from flask import Flask, render_template, jsonify
import requests, time, os
from ai.core import AICore

app = Flask(__name__)
ai = AICore()

URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

last_period = None
last_prediction = None

history = []

# 🧠 self-learning memory
pattern_memory = {}
last_pattern = None


def get_next(p):
    return str(int(p) + 1)


def get_pattern(results):
    # take last 3 results → convert to BIG/SMALL pattern
    pattern = []
    for r in results[:3]:
        pattern.append(1 if int(r) >= 5 else 0)
    return tuple(pattern)


def adjust_prediction(pred, pattern):
    if pattern not in pattern_memory:
        return pred

    score = pattern_memory[pattern]

    # 🔥 if pattern historically wrong → flip prediction
    if score < -1:
        return "BIG" if pred == "SMALL" else "SMALL"

    return pred


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data")
def data():
    global last_period, last_prediction, history
    global pattern_memory, last_pattern

    try:
        ts = int(time.time()*1000)
        res = requests.get(f"{URL}?ts={ts}")
        data = res.json()

        records = data['data']['list']
        first = records[0]

        current_period = first['issueNumber']
        number = first['number']

        actual = "BIG" if int(number) >= 5 else "SMALL"

        # 🔥 APPLY LEARNING FROM LAST RESULT
        if last_prediction is not None and last_pattern is not None:

            win = (last_prediction == actual)

            # update memory
            if last_pattern not in pattern_memory:
                pattern_memory[last_pattern] = 0

            if win:
                pattern_memory[last_pattern] += 1
            else:
                pattern_memory[last_pattern] -= 1

            # store history
            history.insert(0, {
                "period": current_period,
                "prediction": last_prediction,
                "actual": actual,
                "result": "WIN" if win else "LOSS"
            })

            history = history[:20]

        if current_period == last_period:
            return {}

        last_period = current_period

        # AI update
        results = [x['number'] for x in records]
        ai.update(results)

        result = ai.predict()

        pred = result["final"]
        conf = result["confidence"]

        # 🧠 get pattern
        pattern = get_pattern(results)
        last_pattern = pattern

        # 🔥 APPLY SELF LEARNING
        pred = adjust_prediction(pred, pattern)

        last_prediction = pred

        return jsonify({
            "period": current_period,
            "next": get_next(current_period),
            "final": pred,
            "confidence": conf,
            "bots": result["bots"],
            "history": history
        })

    except Exception as e:
        print("ERROR:", e)
        return {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))