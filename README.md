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

├── main.py                  # Main script to run the chatbot

├── gpt_api.py               # Handles communication with OpenAI API for extracting preferences

├── recommend.py             # Loads and filters the escape room data based on extracted preferences

├── Room_escape_data.csv     # Dataset containing escape room theme information

├── openai_config.py         # Stores OpenAI API key and related settings

├── web_ui.html              # (Planned to expand) Web-based UI for chatbot interaction

├── venv/                    # Python virtual environment (excluded from Git)

└── .env / .gitignore        # Environment variables & ignored files configuration

