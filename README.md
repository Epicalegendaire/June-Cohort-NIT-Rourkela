# Health Care Managememt System by CLEANCode

# 🧠 Intelligent Prescription Dashboard (LLM-Powered, Django-Based)

An advanced, interactive medical dashboard built with **Django** and styled using **Black Dashboard (Bootstrap 4)**. This project seamlessly integrates a **Large Language Model (LLM)** to generate AI-based prescription suggestions based on user-input symptoms. Designed with a clean, intuitive UI, the system offers a responsive and user-friendly experience for healthcare professionals and researchers alike.

---

## 🚀 Key Features

- 🔬 **AI-Powered Prescription Engine**: Uses a fine-tuned LLM to recommend prescriptions based on symptom inputs.
- ⚙️ **Django Framework**: Secure, scalable, and modular backend with RESTful API integration.
- 🖥️ **Interactive User Interface**: Modern Bootstrap 4 admin dashboard (Black Dashboard) with AJAX-based communication for smooth UX.
- 📊 **Real-Time Feedback**: Instant prescription generation without leaving the dashboard page.
- 🔐 **Authentication System**: User login, registration, and session handling included.
- 📦 **Modular Codebase**: Easily extendable for additional models, data logging, or healthcare modules.

---

## 📥 Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtualenv (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/intelligent-prescription-dashboard.git
cd intelligent-prescription-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Then visit: http://127.0.0.1:8000/

---

## 🧠 How It Works

1. The user enters symptoms in the dashboard.
2. The frontend sends this data to the Django backend via AJAX.
3. The backend loads the appropriate LLM model for the doctor/user.
4. The LLM generates a prescription recommendation.
5. The result is dynamically rendered on the same page using JavaScript.

---

## 📁 Project Structure

```
├── apps/
│   ├── api/                  # API endpoints and LLM logic
│   ├── pages/                # Dashboard views and UI templates
├── templates/
│   └── layouts/              # Reusable base templates
├── static/
│   └── assets/               # JS, CSS, fonts, and dashboard assets
├── manage.py
├── requirements.txt
└── README.md
```

---

## ✨ Live Features Demonstration

- **Dynamic symptom input form**
- **Real-time AJAX-based prescription generation**
- **Custom notifications via Bootstrap Notify**
- **Support for doctor-specific models**

---

## 🔄 Customization Tips

- Update `views.py` in `apps/api/` to swap or extend LLM logic.
- Edit `dashboard.html` to change UI layout and fields.
- Add logging or model storage for audit and compliance.

---

## 📄 License

This project builds on the [Black Dashboard by Creative Tim](https://www.creative-tim.com/product/black-dashboard), used under its respective license.

---

## 🤝 Credits

- [Creative Tim](https://www.creative-tim.com/) – UI Design
- [OpenAI / Hugging Face / Custom LLMs] – Language Model Integration
- [Django](https://www.djangoproject.com/) – Backend Framework

## WEBSITE

stack - python flask or django

### Front End - YAMIN HARIS

### Back End - MITHUN BHARATH

## Text to Speech - RISHAB JOHARY

## AI / CHATBOT - TOM MATHEW
