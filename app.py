import pandas as pd
import streamlit as st
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/dhirajpawar-dev/job-market-dashboard/main/gsearch_jobs.csv"
    try:
        df = pd.read_csv("gsearch_jobs_small.csv")
    except:
        st.error("Could not load data. Please check the data source.")
        st.stop()
    return df

df = load_data()

st.title("AI-Powered Job Market Intelligence Dashboard")
st.markdown("Analyzing **61,953** real job postings for Data Analyst roles")

st.sidebar.header("Filters")
location_filter = st.sidebar.multiselect(
    "Filter by Location",
    options=df["location"].dropna().unique(),
    default=[]
)

if location_filter:
    filtered_df = df[df["location"].isin(location_filter)]
else:
    filtered_df = df

col1, col2, col3 = st.columns(3)
col1.metric("Total Job Postings", len(filtered_df))
col2.metric("Unique Companies", filtered_df["company_name"].nunique())
col3.metric("Remote Jobs", int(filtered_df["work_from_home"].sum()))

st.divider()

st.subheader("Top 10 Job Titles")
top_titles = filtered_df["title"].value_counts().head(10).reset_index()
top_titles.columns = ["Job Title", "Count"]
fig1 = px.bar(top_titles, x="Count", y="Job Title", orientation="h",
              color="Count", color_continuous_scale="teal")
st.plotly_chart(fig1, use_container_width=True)

st.divider()

st.subheader("Top 10 Locations Hiring")
top_locations = filtered_df["location"].value_counts().head(10).reset_index()
top_locations.columns = ["Location", "Count"]
fig2 = px.bar(top_locations, x="Location", y="Count",
              color="Count", color_continuous_scale="blues")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Salary Distribution (Yearly)")
salary_df = filtered_df[filtered_df["salary_yearly"].notna()]
if len(salary_df) > 0:
    fig3 = px.histogram(salary_df, x="salary_yearly", nbins=50,
                        color_discrete_sequence=["#1D9E75"])
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No salary data available for selected filters.")

st.divider()

st.subheader("Ask AI About the Job Market")
st.markdown("Ask anything about Data Analyst jobs, skills, salaries, or trends.")

user_question = st.text_input("Your question:", 
    placeholder="e.g. What skills should I learn for a data analyst job in 2026?")

if user_question:
    with st.spinner("AI is thinking..."):
        top_skills = df["description_tokens"].dropna().head(100).tolist()
        top_jobs = df["title"].value_counts().head(5).to_dict()
        top_locs = df["location"].value_counts().head(5).to_dict()
        avg_salary = df["salary_yearly"].mean()

        context = f"""
        You are a job market expert. Here is real data from 61,953 Data Analyst job postings:
        - Top job titles: {top_jobs}
        - Top hiring locations: {top_locs}
        - Average yearly salary: ${avg_salary:,.0f}
        - Sample skills from job descriptions: {top_skills[:20]}
        Answer the user's question based on this data in a helpful, clear way.
        """

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_question}
            ]
        )
        answer = response.choices[0].message.content
        st.success("AI Answer:")
        st.write(answer)

st.divider()

st.subheader("Raw Data Explorer")
st.dataframe(filtered_df[["title", "company_name", "location",
                            "salary_yearly", "work_from_home"]].head(50))