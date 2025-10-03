# 📝 CVF Organizational Culture Survey App

A custom web application built with **Python** and **Streamlit** to evaluate organizational culture based on the **Competing Values Framework (Cameron & Quinn)**.  
- 👉 Use the App [CVF Survey App](https://cvf-survey-app-2k2fihtuimbkqcs7vdzfjv.streamlit.app/)

## 🔑 Key Features
- **Interactive Survey UI** using Streamlit with tailored demographics (Division, Level, Gender, Generation, Tenure).  
- **Forced distribution of 100 points per element** with professional examples and tooltips to guide participants.  
- **Real-time data capture** stored in **Google Sheets** via a secure Google Service Account.  
- **Responsive sidebar** with project information, detailed instructions, and customizable descriptions.  
- **Safety valves**:
  - Validation checks to ensure each group sums to 100 points.  
  - Demographics must be completed before submission.  
  - Secure credential management via `.streamlit/secrets.toml` or environment variables.  
- **Scalable analytics pipeline** for further analysis in Python (pandas, matplotlib, seaborn).  
- **Data visualization** through radar (spider) charts to map organizational culture profiles.  

## 📂 Project Structure
├── app.py # Main Streamlit app
├── requirements.txt # Dependencies
├── .streamlit/
│ └── secrets.toml # Google credentials (not committed to GitHub)
└── README.md # Project documentation


## ⚙️ Deployment
This app can be deployed to:
- **Streamlit Cloud** (quick setup)  
- **Render (Standard plan)** – supports secret files for credentials and scalable hosting  
- **Azure / GCP / AWS** – for enterprise-grade deployment  

### Render Build Command
```bash
mkdir .streamlit; cp /etc/secrets/secrets.toml ./.streamlit/; pip install --upgrade pip && pip install -r requirements.txt
```

🔒 Security

Credentials are never hardcoded in the repo.

Google Sheets access is restricted to a service account.

.streamlit/secrets.toml and credentials.json are excluded via .gitignore.

📊 Analysis

After survey completion, data can be exported from Google Sheets and analyzed in Python to:

Generate descriptive statistics (per division, gender, tenure, etc.)

Visualize organizational culture using radar (spider) charts

Benchmark against reference profiles from Cameron & Quinn

<img width="1116" height="1095" alt="output (3)" src="https://github.com/user-attachments/assets/a328dd4b-3867-4d27-a0c2-6c6ed2b81615" />


<img width="2379" height="1186" alt="output (2)" src="https://github.com/user-attachments/assets/0690c109-8093-4bf9-a557-0944e9a1b9a9" />


🚀 Future Enhancements

Admin dashboard for live monitoring of submissions.

Advanced filtering and comparison between demographic groups.

Automated report generation in PDF or Power BI integration.

