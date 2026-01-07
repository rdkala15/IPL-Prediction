from flask import Flask, render_template_string, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load models
bat_model = joblib.load('batting_performance_model.pkl')
bowl_model = joblib.load('bowling_performance_model.pkl')

# ===================== HTML TEMPLATE =====================
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 CSK IPL Performance Predictor 🦁</title>
    <style>
        body {
            background: linear-gradient(135deg, #ffcc00, #0078d7);
            font-family: 'Poppins', sans-serif;
            text-align: center;
            color: #002147;
            padding: 30px;
            overflow-x: hidden;
            position: relative;
        }

        h1 {
            color: #002147;
            text-shadow: 1px 1px 2px #fff;
        }

        .container {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 20px;
            padding: 40px;
            margin: auto;
            width: 60%;
            box-shadow: 0 0 25px rgba(0,0,0,0.3);
            position: relative;
            z-index: 2;
        }

        select, input {
            padding: 10px;
            width: 80%;
            margin: 10px;
            border: 2px solid #ffcc00;
            border-radius: 10px;
            font-size: 16px;
        }

        button {
            background: #002147;
            color: #ffcc00;
            border: none;
            padding: 12px 25px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #ffcc00;
            color: #002147;
        }

        .result-box {
            background: #ffcc00;
            color: #002147;
            padding: 25px 40px;
            font-size: 24px;
            font-weight: 600;
            border-radius: 20px;
            margin-top: 40px;
            width: fit-content;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 0 25px rgba(0,0,0,0.3);
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: scale(0.9);}
            to {opacity: 1; transform: scale(1);}
        }

        /* Full-screen popup for falling fire */
        .popup {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(circle, rgba(255,153,0,0.95) 0%, rgba(255,50,0,0.9) 100%);
            justify-content: center;
            align-items: center;
            font-size: 45px;
            font-weight: bold;
            color: #fff;
            z-index: 999;
            overflow: hidden;
        }

        .popup.show {
            display: flex;
            animation: fadeInPopup 0.5s ease-in-out;
        }

        @keyframes fadeInPopup {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        .fire {
            position: absolute;
            top: -10vh;
            font-size: 40px;
            animation: fallFire 5s linear infinite;
            opacity: 0.9;
        }

        @keyframes fallFire {
            0% {transform: translateY(-10vh) scale(1);}
            100% {transform: translateY(110vh) scale(0.8);}
        }

        .floating-elements {
            position: fixed;
            top: 0;
            width: 15%;
            height: 100%;
            overflow: hidden;
            pointer-events: none;
            z-index: 1;
        }

        .left-side {
            left: 10%; /* moved slightly away from margin */
        }
        .right-side {
            right: 0;
        }

        .floating {
            position: absolute;
            bottom: -10%;
            font-size: 2.2rem;
            animation: rise 10s linear infinite;
            opacity: 0.8;
        }

        .delay1 { animation-delay: 2s; }
        .delay2 { animation-delay: 4s; }
        .delay3 { animation-delay: 6s; }
        .delay4 { animation-delay: 8s; }

        @keyframes rise {
            0% { transform: translateY(0) scale(1); opacity: 0.8; }
            50% { transform: translateY(-50vh) scale(1.2); opacity: 1; }
            100% { transform: translateY(-100vh) scale(0.8); opacity: 0; }
        }

        /* 🎵 Music Toggle Button */
        .music-toggle {
            position: fixed;
            top: 20px;
            right: 30px;
            background: #002147;
            color: #ffcc00;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 16px;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }

        .music-toggle:hover {
            background: #ffcc00;
            color: #002147;
        }
    </style>
</head>
<body>
    <h1>🦁 IPL Player Performance Predictor 💛</h1>

    <!-- 🎵 Background Music Toggle -->
    <button class="music-toggle" id="musicBtn">🎵 Play Sound</button>
    <audio id="bgMusic" loop>
        <source src=""C:\Users\anant\Downloads\new_ipl_music.mp3"" type="audio/mpeg">
    </audio>

    <!-- Left Floating Elements -->
    <div class="floating-elements left-side">
        <div class="floating">🏏</div>
        <div class="floating delay1">🔥</div>
        <div class="floating delay2">🎯</div>
        <div class="floating delay3">💛</div>
        <div class="floating delay4">🦁</div>
    </div>

    <!-- Right Floating Elements -->
    <div class="floating-elements right-side">
        <div class="floating">💥</div>
        <div class="floating delay1">🏆</div>
        <div class="floating delay2">🌟</div>
        <div class="floating delay3">⚡</div>
        <div class="floating delay4">🔥</div>
    </div>

    <div class="container">
        <form method="POST">
            <select name="mode" required>
                <option value="bat">Predict Runs (Batting)</option>
                <option value="bowl">Predict Wickets (Bowling)</option>
            </select>
            <div id="inputFields">
                <input type="text" name="Matches_Batted" placeholder="Matches Batted" required>
                <input type="text" name="Not_Outs" placeholder="Not Outs" required>
                <input type="text" name="Balls_Faced" placeholder="Balls Faced" required>
                <input type="text" name="Batting_Strike_Rate" placeholder="Batting Strike Rate" required>
                <input type="text" name="Centuries" placeholder="Centuries" required>
                <input type="text" name="Half_Centuries" placeholder="Half Centuries" required>
                <input type="text" name="Fours" placeholder="Fours" required>
                <input type="text" name="Sixes" placeholder="Sixes" required>
            </div>
            <button type="submit">🔥 Predict Now</button>
        </form>

        {% if show_result %}
        <div class="popup" id="popupBox">
            <div> Calculating Your IPL Prediction... 🏆</div>
            {% for i in range(20) %}
            <div class="fire" style="left:{{ (i * 5) % 100 }}%; animation-delay:{{ i * 0.2 }}s;">🔥</div>
            {% endfor %}
        </div>

        <script>
            const popup = document.getElementById("popupBox");
            popup.classList.add("show");
            const sound = new Audio("/static/new_ipl_music.mp3");
            sound.volume =0.7;
            sound.play();
            setTimeout(() => {
                popup.classList.remove("show");
            }, 5000);
        </script>

        <div class="result-box">
            {{ prediction }}
        </div>
        {% endif %}
    </div>

    <script>
        const selectMode = document.querySelector("select[name='mode']");
        const inputFields = document.getElementById("inputFields");
        const bgMusic = document.getElementById("bgMusic");
        const musicBtn = document.getElementById("musicBtn");
        let isPlaying = false;

        selectMode.addEventListener("change", () => {
            if (selectMode.value === "bowl") {
                inputFields.innerHTML = `
                    <input type="text" name="Matches_Bowled" placeholder="Matches Bowled" required>
                    <input type="text" name="Balls_Bowled" placeholder="Balls Bowled" required>
                    <input type="text" name="Runs_Conceded" placeholder="Runs Conceded" required>
                    <input type="text" name="Bowling_Average" placeholder="Bowling Average" required>
                    <input type="text" name="Economy_Rate" placeholder="Economy Rate" required>
                    <input type="text" name="Bowling_Strike_Rate" placeholder="Bowling Strike Rate" required>
                    <input type="text" name="Four_Wicket_Hauls" placeholder="Four Wicket Hauls" required>
                    <input type="text" name="Five_Wicket_Hauls" placeholder="Five Wicket Hauls" required>
                `;
            } else {
                inputFields.innerHTML = `
                    <input type="text" name="Matches_Batted" placeholder="Matches Batted" required>
                    <input type="text" name="Not_Outs" placeholder="Not Outs" required>
                    <input type="text" name="Balls_Faced" placeholder="Balls Faced" required>
                    <input type="text" name="Batting_Strike_Rate" placeholder="Batting Strike Rate" required>
                    <input type="text" name="Centuries" placeholder="Centuries" required>
                    <input type="text" name="Half_Centuries" placeholder="Half Centuries" required>
                    <input type="text" name="Fours" placeholder="Fours" required>
                    <input type="text" name="Sixes" placeholder="Sixes" required>
                `;
            }
        });

        musicBtn.addEventListener("click", () => {
            if (!isPlaying) {
                bgMusic.play();
                musicBtn.textContent = "🔇 Pause Sound";
                isPlaying = true;
            } else {
                bgMusic.pause();
                musicBtn.textContent = "🎵 Play Sound";
                isPlaying = false;
            }
        });
    </script>
</body>
</html>
"""

# ===================== FLASK ROUTE =====================
@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    show_result = False

    if request.method == "POST":
        mode = request.form.get("mode")
        show_result = True

        try:
            if mode == "bat":
                data = pd.DataFrame([{
                    'Matches_Batted': float(request.form['Matches_Batted']),
                    'Not_Outs': float(request.form['Not_Outs']),
                    'Balls_Faced': float(request.form['Balls_Faced']),
                    'Batting_Strike_Rate': float(request.form['Batting_Strike_Rate']),
                    'Centuries': float(request.form['Centuries']),
                    'Half_Centuries': float(request.form['Half_Centuries']),
                    'Fours': float(request.form['Fours']),
                    'Sixes': float(request.form['Sixes']),
                }])
                pred = bat_model.predict(data)[0]
                prediction = f"🏏 Predicted Runs: {pred:.2f}"
            else:
                data = pd.DataFrame([{
                    'Matches_Bowled': float(request.form['Matches_Bowled']),
                    'Balls_Bowled': float(request.form['Balls_Bowled']),
                    'Runs_Conceded': float(request.form['Runs_Conceded']),
                    'Bowling_Average': float(request.form['Bowling_Average']),
                    'Economy_Rate': float(request.form['Economy_Rate']),
                    'Bowling_Strike_Rate': float(request.form['Bowling_Strike_Rate']),
                    'Four_Wicket_Hauls': float(request.form['Four_Wicket_Hauls']),
                    'Five_Wicket_Hauls': float(request.form['Five_Wicket_Hauls']),
                }])
                pred = bowl_model.predict(data)[0]
                prediction = f"🎯 Predicted Wickets: {pred:.2f}"

        except Exception as e:
            prediction = f"⚠️ Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, prediction=prediction, show_result=show_result)

if __name__ == "__main__":
    print("✅ Models loaded successfully")
    app.run(debug=True)
