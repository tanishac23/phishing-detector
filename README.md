# 🛡️ PhishShield - AI Powered Phishing & Spam Detector

PhishShield is a cybersecurity web application that uses **Machine Learning** to detect:

- 🔗 **Phishing URLs**
- 📧 **Spam/Phishing Emails**

It analyzes 30+ intelligent features for URLs and classifies emails using a trained Naive Bayes model.

---

## 🚀 Features

- Real-time phishing detection using intelligent feature extraction
- Spam email classification
- User-friendly UI with multiple pages (Home, About, Blog, Contact)
- Built using Python, Flask, HTML/CSS, and scikit-learn
- Deployable on platforms like Render

---

## 🧠 Tech Stack

- Frontend: HTML, CSS (Bootstrap)
- Backend: Python (Flask)
- ML: scikit-learn, pandas, joblib
- Dataset: Kaggle phishing URLs + Spam Email dataset

---

## 📁 Project Structure
phishing-detector/
│
├── static/
│ └── images/ # Logo and other assets
│ └── styles.css # Stylesheet
│
├── templates/
│ └── *.html # Pages: index, about, blog, contact, detect
│
├── app_phishing.py # Flask web app
├── url_feature_extractor.py
├── train_phishing_model.py
├── url_model_trainer.py
├── phishing_model.pkl
├── spam_model.pkl
├── requirements.txt
├── README.md # ← You are here!

---

## 📌 How to Run Locally

```bash
git clone https://github.com/tanishac23/phishing-detector.git
cd phishing-detector
pip install -r requirements.txt
python app_phishing.py
Visit: http://localhost:5000

🌐 Live Demo
(Coming soon on Render...)

👩‍💻 Developed By
Tanisha Choudhari
GitHub | LinkedIn
B.Tech in Cyber Security
Shri Ramdeobaba College of Engineering and Management, Nagpur

---
