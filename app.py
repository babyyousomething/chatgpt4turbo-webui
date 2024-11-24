from flask import Flask, render_template, request, jsonify
import g4f
import logging

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Сообщение не должно быть пустым!"}), 400

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}]
        )

        # Проверка на тип ответа и извлечение текста
        if isinstance(response, dict) and "choices" in response:
            bot_message = response["choices"][0]["message"]["content"]
        elif isinstance(response, str):
            bot_message = response
        else:
            bot_message = "Неизвестный формат ответа от модели."

        return jsonify({"response": bot_message})
    except Exception as e:
        return jsonify({"error": f"Ошибка обработки: {e}"}), 500

if __name__ == "__main__":
    logging.getLogger('werkzeug').disabled = True
    print("Сервер был запущен на: http://localhost:5000")
    app.run()
