# 🚀 AI Social Media Post Automation

Automate your social media content workflow using AI!  
This project uses **LangGraph** and **Groq LLM** to generate, evaluate, and optimize posts for **Twitter** and **Facebook** automatically.

---

## 🔹 Features

- Generate Twitter and Facebook posts from a topic
- Evaluate posts for engagement, hashtags, and readability
- Automatically improve posts if rejected
- Max 5 attempts per post for optimization
- Final approval and display of ready-to-post content

---

## 🛠 Tech Stack

- **Python**  
- **LangGraph** – orchestrate multi-step AI workflows  
- **LangChain + Groq** – AI LLM for generation & evaluation  
- **dotenv** – manage API keys safely

                ┌─────────────────────────────────────┐
                │           USER INPUT                │
                │         (Topic/Keyword)             │
                └────────────────┬────────────────────┘
                                 ↓
                ┌─────────────────────────────────────┐
                │         GENERATION LAYER            │
                │  ┌──────────────┬──────────────┐   │
                │  │ Twitter      │ Facebook     │   │
                │  │ Generator    │ Generator    │   │
                │  └──────────────┴──────────────┘   │
                └────────────────┬────────────────────┘
                                 ↓
                ┌─────────────────────────────────────┐
                │         EVALUATION LAYER            │
                │  ┌──────────────┬──────────────┐   │
                │  │ Twitter      │ Facebook     │   │
                │  │ Validator    │ Validator    │   │
                │  └──────────────┴──────────────┘   │
                └────────────────┬────────────────────┘
                                 ↓
                ┌─────────────────────────────────────┐
                │         ROUTER LAYER                │
                │  ┌─────────────────────────────┐   │
                │  │  Conditional Decision Engine│   │
                │  └─────────────────────────────┘   │
                └────────────────┬────────────────────┘
                      ┌───────────┴───────────┐
                      ↓                       ↓
          ┌─────────────────┐         ┌─────────────────┐
          │   APPROVAL      │         │  OPTIMIZATION   │
          │    LAYER        │         │     LAYER       │
          └─────────────────┘         └─────────────────┘
                      ↓                       ↓
                ┌─────────────────────────────────────┐
                │           FINAL OUTPUT               │
                │    (Approved Twitter & Facebook      │
                │              Posts)                  │
                └─────────────────────────────────────┘
```bash
git clone https://github.com/your-username/ai-social-post-orchestrator.git
cd ai-social-post-orchestrator
