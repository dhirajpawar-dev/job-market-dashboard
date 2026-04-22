# AI-Powered Job Market Intelligence Dashboard

A data analytics web application that analyzes 61,953 real Data Analyst job postings and provides AI-powered career insights.

## Live Demo
🚀 [View Live App](https://job-market-dashboard-hxcvepmuehm7jq3l76kgrs.streamlit.app)

## Features
- 📊 **Interactive Dashboard** — Charts for top job titles, locations, salaries and in-demand skills
- 🎯 **Job Match Score** — Enter your skills and see how well you match the job market
- 📄 **Resume Analyzer** — Upload your resume (PDF) and get AI-powered feedback and score
- 🤖 **Ask AI** — Ask any question about the job market and get answers based on real data
- 📋 **Data Explorer** — Search and browse all 61,953 job postings
- 🔐 **User Authentication** — Secure login and signup system

## Tech Stack
- **Python** — Core programming language
- **Pandas** — Data loading, cleaning and analysis
- **Streamlit** — Web application framework
- **Plotly** — Interactive data visualizations
- **Groq AI (LLaMA 3.3)** — AI-powered insights and resume analysis
- **SQLite** — User authentication database
- **bcrypt** — Password hashing and security
- **PyPDF2** — PDF resume parsing
- **Git & GitHub** — Version control

## Dataset
- Source: [Kaggle — Data Analyst Job Postings](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search)
- 61,953 real job postings from Google Search
- 27 columns including title, company, location, salary, skills

## How to Run Locally
1. Clone the repository
git clone https://github.com/dhirajpawar-dev/job-market-dashboard.git
2. Install dependencies
pip install -r requirements.txt
3. Add your Groq API key in a `.env` file
GROQ_API_KEY=your_key_here
4. Download the dataset from Kaggle and save as `gsearch_jobs_small.csv`
5. Run the app
streamlit run app.py

## Screenshots
> Dashboard showing top job titles, locations and salary distribution
![alt text](image.png)

> Resume Analyzer giving AI feedback on uploaded PDF resume
![alt text](image-1.png)

## Author
**Dhiraj Pawar**
- GitHub: [@dhirajpawar-dev](https://github.com/dhirajpawar-dev)