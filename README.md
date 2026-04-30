# AI-Powered Job Market Intelligence Dashboard

A professional data analytics web application that analyzes 61,953 real Data Analyst job postings and provides AI-powered career insights, business intelligence, and resume analysis.

## Live Demo
🚀 [View Live App](https://job-market-dashboard-hxcvepmuehm7jq3l76kgrs.streamlit.app)

## Screenshots
### Dashboard
![Dashboard](dashboard.png)

### Resume Analyzer
![Resume Analyzer](resume.png)

## Features
- 🔐 **User Authentication** — Secure login and signup system
- 📊 **Interactive Dashboard** — Charts for top job titles, locations, salaries and in-demand skills
- 💡 **Business Insights** — Auto-calculated insights like salary comparisons, remote vs onsite pay, skill demand percentages
- 🎯 **Job Match Score** — Enter your skills and see how well you match the job market with real data-backed recommendations
- 📈 **Skill Gap Impact** — Shows exactly how much each missing skill increases your salary potential
- 📄 **Resume Analyzer** — Upload your resume (PDF) and get AI-powered feedback with match percentage and skill gap analysis
- 🤖 **Ask AI** — Ask any question about the job market and get answers based on real data
- 📋 **Data Explorer** — Search and browse all job postings with filters

## Business Insights Generated
- Python + SQL roles pay significantly above average salary
- Remote vs onsite salary comparison from real data
- Top 5 most in-demand skills with exact percentages
- Average salary breakdown by individual skill
- Top hiring companies and locations

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

## Architecture
User uploads resume / enters skills
↓
Python (Pandas) analyzes against 61,953 job postings
↓
Real data insights calculated (salary, skill demand %)
↓
Groq AI generates personalized recommendations
↓
Streamlit displays interactive dashboard

## Key Data Insights
- SQL is the most in-demand skill across all postings
- Python + SQL combination commands premium salaries
- Remote roles show competitive salary vs onsite
- Top hiring locations concentrated in major US cities

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

## Use Cases
- **Job Seekers** — Understand what skills to learn, analyze salary expectations, get resume feedback
- **HR Teams** — Understand market skill demands and salary benchmarks
- **Career Counselors** — Data-driven career guidance backed by real job market data
- **Students** — Plan which skills to learn based on real market demand

## Author
**Dhiraj Pawar**
- GitHub: [@dhirajpawar-dev](https://github.com/dhirajpawar-dev)
- Live App: [Job Market Dashboard](https://job-market-dashboard-hxcvepmuehm7jq3l76kgrs.streamlit.app)