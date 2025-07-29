# 🤖 Rule-Based Profile Chatbot with Chain-of-Thought Reasoning

A simple, rule-based chatbot built in Python that simulates a natural conversation using **hardcoded profile information** and **chain-of-thought responses**. Ideal for showcasing your portfolio, introducing yourself in an interactive way, or deploying a chatbot on your personal website or terminal.

---

## 📌 Features

- 🧠 **Chain-of-thought** logic simulation (step-by-step reasoning before answers)
- 🎯 Personal information-based answers (like education, skills, experience)
- 🗣️ Interactive Q&A flow (console-based)
- 🧩 Easily extendable rule-based system
- 🧍‍♂️ Chatbot speaks in first-person like it's "you"

---

## 🚀 How It Works

The bot uses your **profile data** stored in a Python dictionary and matches user queries using rule-based `if-else` conditions. For each match, it simulates a thought process (chain-of-thought) before replying.

---

## 🧑‍💻 Example Profile (customize this)

```python
profile = {
    "name": "Anand Dubey",
    "education": {
        "degree": "B.Tech in Computer Science",
        "university": "Bennett University",
        "specialization": "AI & ML",
        "semester": 6
    },
    "experience": [
        "Research Intern at Bennett University (1+ year)",
        "Freelance Data Analyst (8 months)"
    ],
    "skills": ["Python", "SQL", "Excel", "Tableau", "Power BI"],
    "projects": [
        "Bias Detection Tool for Hiring",
        "Real-Time Object Detection using ViT",
        "Credit Risk Prediction using PySpark"
    ],
    "interests": ["Data Analysis", "Web3", "AI Innovation"],
    "current_goal": "Shifting to Data Analyst/Engineer role",
    "personality": "Hardworking, Learner, Adaptive"
}


#Sample Conversation

> Who are you?

[Thinking] User asked about identity.
[Thinking] Referring to profile data...
[Thinking] Returning name.
My name is Anand Dubey, a B.Tech AI/ML student at Bennett University.

> What projects have you done?

[Thinking] User is curious about projects.
[Thinking] Accessing project list from profile...
[Thinking] Responding with all major projects.
Here’s a list of my projects:
- Bias Detection Tool for Hiring
- Real-Time Object Detection using ViT
- Credit Risk Prediction using PySpark
