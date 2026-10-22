# Metro Bites Kano — Binta AI Customer Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Groq API](https://img.shields.io/badge/LLM-Groq%20Cloud-orange)](https://groq.com/)

A production-grade, context-grounded conversational AI assistant built for **Metro Bites Kano**, a takeout restaurant based in Nassarawa GRA, Kano State, Nigeria. 

Powered by Groq's high-speed inference engine (`openai/gpt-oss-120b`), **Binta** handles customer inquiries regarding menus, operational hours, and takeout logistics, strictly enforcing factual business boundaries and guardrails.

---

## 📌 Features & Operational Guardrails

- **Strict Menu & Price Grounding:** Accurately quotes approved prices in Nigerian Naira (₦) and prevents hallucination of off-menu items.
- **Geographic Boundary Enforcement:** Validates takeout delivery strictly to **Nassarawa**, **Fagge**, and **Tarauni** LGAs; refuses unserviceable delivery locations politely.
- **Safety & Scope Guardrails:** Programmed to refuse dietary or medical advice (e.g., allergies, diabetic management) and redirects customers to restaurant personnel.
- **Uncertainty & Escalation Fallback:** Employs explicit conversational escalation when answering queries outside its knowledge base.
- **Session Telemetry:** Tracks cumulative LLM token consumption in real-time within the Streamlit interface.

---

## 🍽️ Approved Menu Reference

| Dish / Item | Price (NGN) |
| :--- | :--- |
| Jollof rice with chicken | ₦2,800 |
| Fried rice with turkey | ₦3,500 |
| Grilled chicken with chips | ₦3,200 |
| Chicken shawarma | ₦1,800 |
| Beef burger with fries | ₦2,500 |
| Tuwon shinkafa with miyan taushe | ₦2,000 |
| Small chops pack | ₦1,500 |

* **Location:** Nassarawa GRA, Kano State, Nigeria  
* **Operating Hours:** Mon–Sat: 10:00 AM – 10:00 PM | Sun: 12:00 PM – 9:00 PM  
* **Approved Delivery Zones:** Nassarawa, Fagge, Tarauni  

---

## Project Architecture

```text
metro-bites-binta/
├── .env                  # Local secret credentials (ignored by Git)
├── .dockerignore         # Docker build exclusion list
├── .gitignore            # Git exclusion rules
├── Dockerfile            # Container build definition (Python 3.11-slim)
├── docker-compose.yml    # Container orchestration spec
├── requirements.txt      # Python package dependencies
├── app.py                # Streamlit UI & conversational engine
└── README.md             # Project documentation
