# 🎲 Escape Room Recommendation Chatbot

**AI-powered chatbot for recommending escape room themes based on user preferences**

This project understands natural language input from users and recommends matching escape room themes by parsing key preferences like genre, location, number of players, and fear tolerance.

------------------------------------------------------------
## 📌 Key Features

- 🧠 **Natural Language Understanding with OpenAI GPT**  
  Extracts structured preferences (e.g. `location`, `genre`, `people`, `fear_ok`) from conversational input using GPT-3.5.

- 🗂️ **Dynamic Filtering of Real Data**  
  Filters real-world escape room data stored in CSV format and returns the best-matched themes.

- 💬 **Extendable Chat UI**  
  Built to support future web-based chatbot UI (React/Streamlit), enabling real-time chat interaction.

------------------------------------------------------------

## 🧩 Tech Stack

| Area         | Technology               |
|--------------|---------------------------|
| Language     | Python                    |
| NLP/LLM      | OpenAI GPT-3.5 Turbo      |
| Data Handling| Pandas, CSV               |
| Backend (planned) | FastAPI             |
| Frontend (planned) | HTML / JS / Streamlit |

------------------------------------------------------------

## 🧪 How to Run

1. Activate virtual environment:
   ```bash
   source venv/bin/activate
   
------------------------------------------------------------

## 📁 Project Structure (with explanation)
escape_chatvot/
├── main.py                  # 메인 실행 파일
├── gpt_api.py              # OpenAI API 연동
├── recommend.py            # 데이터 로딩 및 필터링 로직
├── Room_escape_data.csv    # 테마 데이터셋
├── openai_config.py        # API 키 설정
└── web_ui.html (선택)      # 웹 챗봇 UI 샘플
