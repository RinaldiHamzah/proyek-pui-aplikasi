import os
from datetime import datetime
from pathlib import Path
import requests
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from sentiment_model import ModelPredict

BASE_DIR = Path(__file__).resolve().parent
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "public" / "static"),
    static_url_path="/static",
)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key-before-production")

_model_ml = None


def get_model():
    global _model_ml
    if _model_ml is None:
        _model_ml = ModelPredict()
    return _model_ml


def get_chat_ids():
    raw_chat_ids = os.getenv("TELEGRAM_CHAT_IDS", "")
    return [chat_id.strip() for chat_id in raw_chat_ids.split(",") if chat_id.strip()]


@app.route("/")
def index():
    if "logged_in" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    required_password = os.getenv("LOGIN_PASSWORD")

    if not username:
        return render_template("login.html", error="Username wajib diisi"), 400

    if required_password and password != required_password:
        return render_template("login.html", error="Password tidak sesuai"), 401

    session["logged_in"] = True
    session["username"] = username
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if "logged_in" not in session:
        return redirect(url_for("index"))

    return render_template("dashboard.html", username=session["username"])


class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_sentiment_result(self, review_text, sentiment, model, username):
        message = f"""
<b>Hasil Analisis Sentimen</b>
<b>User:</b> {username}
<b>Ulasan:</b> {review_text[:2000]}{"..." if len(review_text) > 2000 else ""}

<b>Sentimen:</b> {sentiment}
<b>Model:</b> {model}
<b>Waktu:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        """

        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                data={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                },
                timeout=8,
            )
            return response.json()
        except requests.RequestException as error:
            app.logger.warning("Telegram notification failed: %s", error)
            return None


@app.route("/predict", methods=["POST"])
def predict():
    if "logged_in" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    review_text = request.form.get("review_text", "").strip()
    model = request.form.get("model", "svm")

    if not review_text:
        return jsonify({"error": "Text review tidak boleh kosong"}), 400

    model_ml = get_model()
    if model == "naive-bayes":
        sentiment = model_ml.model_predict_nvm(review_text)
    else:
        sentiment = model_ml.model_predict_svm(review_text)

    result = {
        "sentiment": sentiment,
        "model_used": model,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_ids = get_chat_ids()

    if bot_token and chat_ids:
        telegram_sent = False
        for chat_id in chat_ids:
            notifier = TelegramNotifier(bot_token, chat_id)
            telegram_result = notifier.send_sentiment_result(
                review_text=review_text,
                sentiment=sentiment,
                model=model,
                username=session["username"],
            )
            telegram_sent = telegram_sent or bool(telegram_result and telegram_result.get("ok"))

        result["telegram_sent"] = telegram_sent
        result["telegram_message"] = (
            "Hasil berhasil dikirim ke Telegram Bot"
            if telegram_sent
            else "Gagal mengirim ke Telegram Bot"
        )
    else:
        result["telegram_sent"] = False
        result["telegram_message"] = "Telegram Bot belum dikonfigurasi"

    return jsonify(result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
