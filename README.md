This is a comprehensive, visually attractive, and highly detailed README.md for your project. It includes technology badges, a clear roadmap of how the agent works, and the specific troubleshooting steps we solved.

📝 Quiz Generator Agent
<div align="center">


![alt text](https://img.shields.io/badge/python-3.12.4-blue?style=for-the-badge&logo=python&logoColor=white)


![alt text](https://img.shields.io/badge/Framework-Agno-orange?style=for-the-badge)


![alt text](https://img.shields.io/badge/Server-Bindu-red?style=for-the-badge)


![alt text](https://img.shields.io/badge/LLM-OpenRouter-black?style=for-the-badge)


![alt text](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

"Transforming static text into high-quality pedagogical assessments through the power of AI."

</div>

📖 Overview

The Quiz Generator Agent is a professional-grade AI microservice designed to bridge the gap between long-form text and active learning. Built on top of the Agno framework and served via the Bindu protocol, it allows developers to submit documents and receive exactly 10 Multiple Choice Questions (MCQs), complete with balanced distractors and detailed explanations.

This agent operates asynchronously, meaning it can handle massive text inputs by creating a background task, allowing the client to poll for the results without connection timeouts.

✨ Features

🧠 Smart Context Extraction: Identifies the 10 most critical learning points from any text.

🎯 Pedagogical Precision: Generates 4 options (A, B, C, D) per question with only one logically sound answer.

📝 Detailed Explanations: Every answer includes a 1-sentence explanation to reinforce learning.

⚡ Task-Based Architecture: Implements a Submit -> Poll -> Complete workflow for high reliability.

🛡️ X402 Protocol Compliance: Uses the professional JSON-RPC 2.0 standard for agent communication.

🛠️ Technology Stack
Component	Technology	Logo
Language	Python 3.12.4	
![alt text](https://img.shields.io/badge/-Python-blue?logo=python&logoColor=white)

Agent Framework	Agno	
![alt text](https://img.shields.io/badge/-Agno-orange)

Server Engine	Bindu (Uvicorn/Starlette)	
![alt text](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white)

LLM Gateway	OpenRouter (Gemini/GPT)	
![alt text](https://img.shields.io/badge/-OpenRouter-black)

Messaging	X402 / JSON-RPC 2.0	
![alt text](https://img.shields.io/badge/-JSON--RPC-gray)
🚀 Installation & Setup
1. Clone the Project
code
Powershell
download
content_copy
expand_less
cd quiz-generator-agent
2. Configure Virtual Environment

Ensure you are using Python 3.12.4 to avoid C++ build errors.

code
Powershell
download
content_copy
expand_less
python -m venv .venv
.venv\Scripts\activate
3. Install Dependencies
code
Powershell
download
content_copy
expand_less
pip install agno openai python-dotenv bindu x402 requests pytest pytest-asyncio
4. Setup API Credentials

Rename .env.example to .env and fill in your keys:

code
Text
download
content_copy
expand_less
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
MODEL_NAME=google/gemini-2.0-flash-lite-preview-02-05:free
🖥️ Running the Agent

You will need two separate terminals open to interact with the system.

Terminal 1: Start the Server

This launches the AI Agent and starts the Bindu server on port 3773.

code
Powershell
download
content_copy
expand_less
python quiz_generator_agent/main.py
Terminal 2: Run the Quiz Task

This script sends a detailed sample text to the agent, monitors the background task, and prints the final quiz.

code
Powershell
download
content_copy
expand_less
python tests/test_main.py
📂 Project Structure
code
Text
download
content_copy
expand_less
quiz-generator-agent/
├── .github/             # GitHub Actions for CI/CD
├── .venv/               # Isolated Python environment
├── .env                 # Secret API Keys (Git ignored)
├── .env.example         # Template for new users
├── agent_config.json    # Agent metadata & storage settings
├── pyproject.toml       # Project metadata & dependencies
├── README.md            # You are here
├── quiz_generator_agent/
│   └── main.py          # Server logic & Agent Persona
└── tests/
    └── test_main.py     # Protocol tests & Task polling logic
🔧 Troubleshooting & Common Issues
🔴 X402 / C++ Build Errors

Error: ModuleNotFoundError: No module named 'x402.common' or Microsoft Visual C++ 14.0 is required.

Cause: Python 3.13+ requires manual compilation for X402.

Fix: Use Python 3.12.4. If you must use 3.13+, install C++ Build Tools and restart your PC.

🔴 PostgreSQL Connection Refused

Error: ValueError: invalid literal for int() with base 10: '<port>'.

Cause: The agent is looking for a production database.

Fix: Open agent_config.json and ensure "storage": {"type": "memory"} and "scheduler": {"type": "memory"} are set.

🔴 JSON-RPC 400 Bad Request

Error: Unable to extract tag using discriminator 'method'.

Fix: The Bindu framework requires a specific envelope. Your test request must use method: "message/send" and include a uuid for the id field. Refer to tests/test_main.py.

🔴 No Quiz Content in Response

Cause: The agent is asynchronous.

Fix: The initial response only contains a task_id. Your script must loop (poll) the tasks/get endpoint until the state reaches "completed".

⚖️ License

Distributed under the MIT License. See LICENSE for more information.

<div align="center">
<sub>Developed  by Rajat Chauhan. Built using the Agno & Bindu Ecosystem.</sub>
</div>
