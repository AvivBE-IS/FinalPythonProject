# 🐧 Palmer Penguins Analysis Web App

A data analysis and exploration web application built with **FastAPI**. This project was developed as a Capstone Project for the **CyberProAI** course. It provides an interactive interface to explore the Palmer Penguins dataset, filter data, and generate dynamic visualizations.

## 🚀 Features

* **Interactive Data Exploration:** View and filter the penguins dataset based on various criteria.
* **Dynamic Visualizations:** Generate real-time plots (histograms, scatter plots) using **Seaborn** and **Matplotlib**.
* **Predefined Analysis:** Access specific analytical questions via dedicated endpoints.
* **Clean Architecture:** Built using a layered architecture separating business logic (`DataService`, `AnalysisService`) from the web layer.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Web Framework:** FastAPI
* **Templating:** Jinja2
* **Data Manipulation:** Pandas
* **Visualization:** Matplotlib, Seaborn
* **Server:** Uvicorn

## 📂 Project Structure

```text
├── main.py              # Application entry point
├── services/
│   ├── data_service.py      # Logic for data loading and filtering
│   └── analysis_service.py  # Logic for generating plots
├── static/              # CSS, Images, and generated plots
├── templates/           # Jinja2 HTML templates
├── data/
│   └── penguins.csv     # The dataset
└── requirements.txt     # Python dependencies
```

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone [https://github.com/AvivBE-IS/penguins-analysis.git](https://github.com/AvivBE-IS/penguins-analysis.git)
cd penguins-analysis
```

### 2. Create a virtual environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## ▶️ How to Run

**1. Start the server:**
Run the following command to start the application with live reload:
```bash
uvicorn main:app --reload
```

**2. Access the application:**
Open your web browser and navigate to:
http://127.0.0.1:8000
