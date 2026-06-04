from flask import Flask, jsonify, render_template, request

from assistant import BGTAssistant


app = Flask(__name__)
assistant = BGTAssistant()


@app.route("/")
def home():
    """Show the chatbot page."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Receive a user message and return the assistant response."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    language = data.get("language", "en")

    result = assistant.answer(message, language)
    return jsonify(result)


@app.route("/api/quick-questions")
def quick_questions():
    """Send common questions to the front end for quick cards."""
    language = request.args.get("language", "en")
    return jsonify(assistant.get_quick_questions(language))


@app.route("/api/stats")
def stats():
    """Show simple statistics about the most asked questions."""
    return jsonify(assistant.get_statistics())


if __name__ == "__main__":
    app.run(debug=True)
