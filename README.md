# FinalPythonProject
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

⚙️ Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/your-username/penguins-analysis.git](https://github.com/your-username/penguins-analysis.git)
cd penguins-analysis

Virtual environment (optional but recommended):
Bash:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:
Bash
pip install -r requirements.txt
Run the application:

Bash
uvicorn main:app --reload
Access the app:
Open your browser and go to http://127.0.0.1:8000.

