# BGT Virtual Assistant Chatbot

## Short description

This project is a school assignment chatbot for BGT, British Gymnasium of Technology. The assistant answers common questions from students, parents, and visitors about the school, programs, registration, grades, technology, and contact information.

The project uses a clean dark web interface and a simple Python/Flask backend.

## Technologies used

- Python
- Flask
- HTML
- CSS
- JavaScript
- JSON for chatbot answers
- Text file logging for conversation history

## How to run the project

1. Open PowerShell or Command Prompt.
2. Go to the project folder:

```powershell
cd "C:\Users\TiaraJasiqi\Desktop\detyra AI"
```

3. Create a virtual environment:

```powershell
python -m venv .venv
```

4. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this command first:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

5. Install Flask:

```powershell
pip install -r requirements.txt
```

6. Start the app:

```powershell
python app.py
```

7. Open the chatbot in your browser:

```text
http://127.0.0.1:5000
```

If Windows opens the Microsoft Store or says Python was not found, install Python from python.org or disable the Windows "App execution aliases" for Python. You can also run the app with the full Python path in PowerShell:

```powershell
& "$env:LOCALAPPDATA\Python\bin\python.exe" app.py
```

## Features

- Answers required BGT questions
- Understands different versions of the same question using keyword matching
- English, Albanian, and bilingual response modes
- Dark minimalistic web design
- Welcome message
- Quick question cards
- Polite fallback answer when the question is not understood
- Conversation history saved in `data/chat_history.txt`
- Simple most asked question statistics saved in `data/stats.json`
- Clean OOP structure with a `BGTAssistant` class

## How the chatbot works

The chatbot knowledge is stored in `data/answers.json`. Each question has:

- an ID
- a category
- English and Albanian titles
- English and Albanian answers
- keywords that help the bot understand similar questions

When a user sends a message, the `BGTAssistant` class:

1. Normalizes the message by lowercasing it and removing punctuation.
2. Compares the message with the keywords in `answers.json`.
3. Chooses the best matching answer.
4. Saves the conversation to `data/chat_history.txt`.
5. Updates the statistics in `data/stats.json`.

If no good match is found, the assistant gives a safe fallback answer and suggests contacting school administration for accurate information.

## Example questions

- What is BGT?
- Where is BGT located?
- What programs does BGT offer?
- How does registration work?
- How can I see my grades?
- How can I contact teachers?
- Does BGT have computer labs?
- What technologies are taught?
- Is there professional practice?
- What is the phone number?
- What is the email?
- What is the address?

## Testing section

User: What is BGT?

Bot: BGT stands for British Gymnasium of Technology. It is a technology-focused high school in Pristina, Kosovo. According to the official BGT website, it is the first gymnasium in Kosovo focused entirely on Information Technology, preparing students for higher education and technology-related careers.

User: How can I see my grades?

Bot: Students can usually check their grades through the school's official system, such as EduPage, or by asking their teachers or the school administration. If you cannot access your account, contact the administration for help.

User: How are payments made?

Bot: Payment details are not clearly listed in the public pages used for this project. For the most accurate information about tuition, invoices, deadlines, and payment methods, please contact the BGT administration or finance office directly.

User: Cilat teknologji mësohen?

Bot: Programi i BGT përfshin Sistemet e TI-së, Elementet e AI, Zhvillimin e Ueb Faqeve, Sigurinë Kibernetike, Programimin, Zhvillimin e Aplikacioneve Mobile, Zhvillimin e Lojërave Kompjuterike, Big Data dhe lëndë të tjera të TI-së.

## Notes about BGT information

Information in this project is based on publicly available official BGT pages:

- https://www.bgt.school/
- https://new.bgt.school/

The official pages were used for details such as the school focus, IT program, contact information, address, website, working hours, and application information. When information was not clearly available, the chatbot uses a safe answer such as: "For the most accurate information, please contact the school administration directly."
