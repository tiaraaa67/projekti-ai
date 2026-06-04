import json
import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from threading import Lock


BASE_DIR = Path(__file__).resolve().parent


class BGTAssistant:
    """Simple OOP chatbot for British Gymnasium of Technology."""

    def __init__(
        self,
        answers_path=BASE_DIR / "data" / "answers.json",
        history_path=BASE_DIR / "data" / "chat_history.txt",
        stats_path=BASE_DIR / "data" / "stats.json",
    ):
        self.answers_path = Path(answers_path)
        self.history_path = Path(history_path)
        self.stats_path = Path(stats_path)
        self.lock = Lock()

        self.answers_path.parent.mkdir(parents=True, exist_ok=True)
        self.history_path.touch(exist_ok=True)
        self.stats_path.touch(exist_ok=True)

        self.knowledge = self._load_json(self.answers_path, default={})
        self.stats = self._load_json(self.stats_path, default={})
        self.intents = self.knowledge.get("intents", [])

    def _load_json(self, path, default):
        """Load a JSON file safely, returning a default value if it is empty."""
        if not path.exists() or path.stat().st_size == 0:
            return default

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_stats(self):
        with self.stats_path.open("w", encoding="utf-8") as file:
            json.dump(self.stats, file, indent=2, ensure_ascii=False)

    def _normalize(self, text):
        """Make matching easier by lowercasing and removing accents/punctuation."""
        text = text.lower().strip()
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def _match_intent(self, message):
        """Find the best intent using keyword and token overlap scoring."""
        normalized_message = self._normalize(message)
        message_tokens = set(normalized_message.split())

        best_intent = None
        best_score = 0

        for intent in self.intents:
            score = 0

            for keyword in intent.get("keywords", []):
                normalized_keyword = self._normalize(keyword)
                keyword_tokens = set(normalized_keyword.split())

                if not normalized_keyword:
                    continue

                if normalized_keyword in normalized_message:
                    # Longer phrase matches are usually more specific.
                    score += 8 + len(keyword_tokens)
                elif keyword_tokens:
                    overlap = len(message_tokens.intersection(keyword_tokens))
                    if overlap:
                        score += overlap

            if score > best_score:
                best_score = score
                best_intent = intent

        # A low score usually means only one generic word matched.
        if best_score < 3:
            return None, best_score

        return best_intent, best_score

    def _format_answer(self, intent, language):
        if language == "sq":
            return intent.get("answer_sq", intent.get("answer_en", ""))

        if language == "both":
            english = intent.get("answer_en", "")
            albanian = intent.get("answer_sq", "")
            return f"English:\n{english}\n\nShqip:\n{albanian}"

        return intent.get("answer_en", "")

    def _fallback(self, language):
        fallback = self.knowledge.get("fallback", {})

        if language == "sq":
            return fallback.get("sq", fallback.get("en", ""))

        if language == "both":
            return f"English:\n{fallback.get('en', '')}\n\nShqip:\n{fallback.get('sq', '')}"

        return fallback.get("en", "")

    def _record_history(self, message, answer, language, intent_id):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"[{timestamp}] Language: {language}\n"
            f"User: {message}\n"
            f"Intent: {intent_id or 'unknown'}\n"
            f"Bot: {answer}\n"
            f"{'-' * 70}\n"
        )

        with self.history_path.open("a", encoding="utf-8") as file:
            file.write(entry)

    def _update_stats(self, intent_id):
        if not intent_id:
            intent_id = "unknown"

        self.stats[intent_id] = self.stats.get(intent_id, 0) + 1
        self._save_stats()

    def answer(self, message, language="en"):
        """Return a chatbot response and save the conversation."""
        language = language if language in {"en", "sq", "both"} else "en"
        message = (message or "").strip()

        if not message:
            response = self._fallback(language)
            return {
                "answer": response,
                "intent": None,
                "matched_title": "Unknown",
                "confidence": 0,
            }

        intent, score = self._match_intent(message)

        if intent:
            response = self._format_answer(intent, language)
            intent_id = intent.get("id")
            matched_title = intent.get("title_en", "Matched question")
        else:
            response = self._fallback(language)
            intent_id = None
            matched_title = "Unknown"

        with self.lock:
            self._record_history(message, response, language, intent_id)
            self._update_stats(intent_id)

        return {
            "answer": response,
            "intent": intent_id,
            "matched_title": matched_title,
            "confidence": score,
        }

    def get_quick_questions(self, language="en"):
        """Return popular questions for clickable cards in the interface."""
        quick_ids = self.knowledge.get("quick_questions", [])
        quick_questions = []

        for intent_id in quick_ids:
            intent = next((item for item in self.intents if item.get("id") == intent_id), None)
            if not intent:
                continue

            title_key = "title_sq" if language == "sq" else "title_en"
            quick_questions.append(
                {
                    "id": intent_id,
                    "text": intent.get(title_key, intent.get("title_en")),
                    "category": intent.get("category", "BGT"),
                }
            )

        return quick_questions

    def get_statistics(self, limit=5):
        """Return the most asked recognized questions."""
        titles = {intent["id"]: intent["title_en"] for intent in self.intents}
        counter = Counter(self.stats)
        stats = []

        for intent_id, count in counter.most_common(limit):
            stats.append(
                {
                    "intent": intent_id,
                    "question": titles.get(intent_id, "Unknown or fallback question"),
                    "count": count,
                }
            )

        return stats
