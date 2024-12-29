from flask import Flask, render_template, request, jsonify
from agent import Agent
from src.utils.config_loader import load_config
from src.utils.messenging import connect_to_telegram
from django_report import PDFGenerator
import markdown
import requests
from flask import send_from_directory

config_list = load_config("config/GROQ_CONFIG_LIST")

app = Flask(__name__,static_url_path='/static')

# Telegram Bot Token and URL
BOT_TOKEN = "YOUR_BOT_TOKEN"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    message = ""
    if request.method == "POST":
        message = request.form["keyword"]
        if message.strip():
            agent = Agent(config_list)
            result = agent.start(message)
            print(result)
            # try:
            #     html = markdown.markdown(result)
            # except Exception as e:

            #     if 'error' in result:
            #         html = "Maximum number of requests exceeded. Please try again after a few minutes."
            #     print(e)
            return render_template("index.html", html=result, message=message)
            # generator = PDFGenerator(f"reports", "templates", "report.html")
            # result = generator.generate_pdf_file({"result": html})
    else:
        result = None
    return render_template("index.html", result=result or "", message=message)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    chat_id = update["message"]["chat"]["id"]
    message_text = update["message"]["text"]
    print(f"Received message: {message_text}")
    send_message(chat_id, f"You said: {message_text}")
    return "OK", 200


def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


if __name__ == "__main__":
    connect_to_telegram()
    app.run(debug=True)
