# AI-Chatbot SQLite 

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)]()


Powered by **DeepSeek** and **Gemini API**

---

## 📖 Table of Contents
- [Description](#-description)
- [Working](#-working)
- [Installation](#-installation)
- [Limitation](#-limitation)
- [improvement](#-improvement)
- [Contact](#-contact)

---

## 🚀 Description
**What does this project do?**  
This project accepts Natural Languague prompts from user and convert them into SQLite query and processes it on database giving desired answer!

**Key Features**  
- Uses DeepSeek Model (custom hosted)
- Have dual model selection option between Gemini and Deepseek
- Handle each error gracefull!

**Tech Stack**  
- Language: Python, Javascript, HTML, CSS, SQL
- Frameworks: Flask, FastAPI, pyTorch
- Database: SQLite
- Tools: Docker, Render, HuggingFace, GitHub 


![Demo video](https://github.com/jeet-Suthar/AI-Chatbot/blob/main/root/static/images/Screencast%20from%202025-02-02%2018-19-08(1).gif)
---
## 💼 Working
---
Model is hosted on Render website(free-tier). Here we have Flask App running with all frontend and backend.

User have option to select between two model - Gemini and DeepSeek.(little icon right beside send icon is model selection button) When user selects Gemini, query are given by google Gemini through API protocol. 

And User selects other option - **DeepSeek** then query are resolved by DeepSeek model. I have download this model inside huggingFace Docker Space. There model file and FastAPI is placed. Basicaly huggingFace Docker is serving as **API EndPoint**. 

User query are passed to this **API Endpoint** and it give SQLite query answer. 

**BUT BUT and big BUT**...

As I have free account on HuggingFace and don't have flithy wealth to spend on paid serivces...**damm** this model is slower af. Takes about 2-3 minute to give one response...had to work on it for straight days yet this is what free service can give you. 

Also model is smaller one so it's prompt are hard to control...but I have still managed to get it run.

---

## 💻 Installation
**Prerequisites**  
- [Python 3.10+](https://python.org)
- [Docker](https://docker.com) (optional)
- SQLite

**First, Install Flask.app**

Following step will cover installation of Flask App

**Steps**  
1. Clone the repository:
   ```bash
   git clone https://github.com/jeet-Suthar/AI-Chatbot.git
   git
   cd AI-Chabot/root
   ```

2. Install requirement.txt libraries
    ```bash
        pip install -r requirements.txt
    ```

3. Run app.py
    ```bash
    python3 app.py
    ```
4. All Done with Flast app. Enjoy!

**Now to install DeepSeek, you need to follow this below steps**

1. Find "DeepSeek_files" name directory
2. There will be on **app.py** file, Run it. It will donwload model about 3-4Gb on your local system. 
3. All Done! 

---
## 🚧 Limitation

As this model is totally build on free services it have hell of limitations.

1. DeepSeek Model response time
2. Echo of user prompt by DeepSeek model in answer.
3. DeepSeek can't handle complex query. 
4. Gemini get confused in multiple nested queries...(rest Gemini is working as butter that too on free version)
5. Don't have memory presistence (as for now)
6. Gemini give sql related queries answer in table format...even if answer is in one word. 
7. UI improvement for responsiveness

---
## 📈 Improvement

If I got access to paid services and little bit more time then thing is improved
1. Response time
2. trained custom AI model on large dataset
3. Made UI more better then now
4. with more experience I will make more accurate and fast

---
## Contact
Gmail - Jitendrasutharwork@gmail.com
