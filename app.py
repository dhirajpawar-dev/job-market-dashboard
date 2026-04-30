import pandas as pd
import streamlit as st
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv
import os
from auth import init_db, show_auth

load_dotenv()

st.set_page_config(page_title="Job Market Dashboard", layout="wide")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
init_db()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    show_auth()
    st.stop()

user_name = st.session_state["user_name"]

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("gsearch_jobs_small.csv")
    except:
        st.error("Could not load data.")
        st.stop()
    return df

df = load_data()

st.title(f"Welcome, {user_name}! 👋")
st.markdown("Analyzing **61,953** real job postings for Data Analyst roles")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", [
    "📊 Dashboard",
    "💡 Insights",
    "🎯 Career Tools",
    "🤖 Ask AI",
    "📋 Data Explorer"
])

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["user_name"] = ""
    st.rerun()

st.sidebar.divider()
st.sidebar.info("Built with Python + Streamlit + Groq AI")

if page == "📊 Dashboard":
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

    st.subheader("Top Skills in Demand")
    skills_data = []
    skill_list = ['python', 'sql', 'tableau', 'excel', 'power_bi', 'r', 'spark', 'aws']
    for skill in skill_list:
        count = df['description_tokens'].dropna().apply(
            lambda x: skill in str(x).lower()
        ).sum()
        skills_data.append({"Skill": skill.upper(), "Job Postings": int(count)})
    skills_df = pd.DataFrame(skills_data).sort_values("Job Postings", ascending=True)
    fig4 = px.bar(skills_df, x="Job Postings", y="Skill", orientation="h",
                  color="Job Postings", color_continuous_scale="teal",
                  title="Most In-Demand Skills Across All Job Postings")
    st.plotly_chart(fig4, use_container_width=True)

elif page == "💡 Insights":
    st.subheader("💡 Key Business Insights")
    st.markdown("Auto-calculated insights from **61,953** real job postings:")

    # Insight 1 - Python + SQL salary
    py_sql_df = df[
        df['description_tokens'].dropna().apply(
            lambda x: 'python' in str(x).lower() and 'sql' in str(x).lower()
        ) & df['salary_yearly'].notna()
    ]
    py_sql = py_sql_df['salary_yearly'].mean()
    overall_salary = df[df['salary_yearly'].notna()]['salary_yearly'].mean()

    if py_sql and overall_salary:
        diff = int(((py_sql - overall_salary) / overall_salary) * 100)
        col1, col2 = st.columns(2)
        col1.metric("Avg Salary (Python + SQL)", f"${py_sql:,.0f}", f"{diff}% above average")
        col2.metric("Overall Avg Salary", f"${overall_salary:,.0f}")

    st.divider()

    # Insight 2 - Remote vs onsite salary
    remote_salary = df[(df['work_from_home'] == True) & df['salary_yearly'].notna()]['salary_yearly'].mean()
    onsite_salary = df[(df['work_from_home'] == False) & df['salary_yearly'].notna()]['salary_yearly'].mean()

    if remote_salary and onsite_salary:
        col1, col2 = st.columns(2)
        col1.metric("Remote Jobs Avg Salary", f"${remote_salary:,.0f}")
        col2.metric("Onsite Jobs Avg Salary", f"${onsite_salary:,.0f}")
        if remote_salary > onsite_salary:
            st.success(f"💡 Remote roles pay **${remote_salary - onsite_salary:,.0f} more** on average than onsite roles!")
        else:
            st.info(f"💡 Onsite roles pay **${onsite_salary - remote_salary:,.0f} more** on average than remote roles!")

    st.divider()

    # Insight 3 - Top 5 most valuable skills
    st.markdown("**📊 Top 5 Most In-Demand Skills:**")
    skill_list2 = ['python', 'sql', 'tableau', 'excel', 'power_bi', 'r', 'spark', 'aws']
    skill_counts = {}
    for skill in skill_list2:
        count = df['description_tokens'].dropna().apply(
            lambda x: skill in str(x).lower()
        ).sum()
        skill_counts[skill.upper()] = int(count)

    top_skills_sorted = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (skill, count) in enumerate(top_skills_sorted, 1):
        pct = int((count / len(df)) * 100)
        st.markdown(f"**{i}. {skill}** — appears in **{pct}%** of all job postings ({count:,} jobs)")

    st.divider()

    # Insight 4 - Remote job percentage
    remote_count = int(df['work_from_home'].sum())
    remote_pct = int((remote_count / len(df)) * 100)
    st.info(f"💡 **{remote_pct}%** of all Data Analyst jobs ({remote_count:,} roles) offer remote work!")

    # Insight 5 - Top hiring company
    top_company = df['company_name'].value_counts().index[0]
    top_company_count = df['company_name'].value_counts().iloc[0]
    st.info(f"💡 **{top_company}** is the top hiring company with **{top_company_count}** job postings!")

    st.divider()

    # Insight 6 - Skill salary comparison chart
    st.subheader("💰 Average Salary by Skill")
    skill_salary_data = []
    for skill in skill_list2:
        skill_df = df[
            df['description_tokens'].dropna().apply(
                lambda x: skill in str(x).lower()
            ) & df['salary_yearly'].notna()
        ]
        if len(skill_df) > 0:
            skill_salary_data.append({
                "Skill": skill.upper(),
                "Avg Salary": int(skill_df['salary_yearly'].mean()),
                "Job Count": len(skill_df)
            })

    if skill_salary_data:
        salary_skill_df = pd.DataFrame(skill_salary_data).sort_values("Avg Salary", ascending=True)
        fig5 = px.bar(salary_skill_df, x="Avg Salary", y="Skill",
                      orientation="h", color="Avg Salary",
                      color_continuous_scale="teal",
                      title="Average Salary for Each Skill")
        st.plotly_chart(fig5, use_container_width=True)

elif page == "🎯 Career Tools":
    st.subheader("Job Match Score")
    st.markdown("Enter your skills and see how well you match the job market.")
    user_skills = st.text_input("Enter your skills (comma separated):",
        placeholder="e.g. python, sql, tableau, excel")

    if user_skills:
        user_skill_list = [s.strip().lower() for s in user_skills.split(",")]
        market_skills = ['python', 'sql', 'tableau', 'excel', 'power_bi', 'r', 'spark', 'aws']
        matched = [s for s in user_skill_list if s in market_skills]
        score = int((len(matched) / len(market_skills)) * 100)

        st.metric("Your Match Score", f"{score}%")

        # Progress bar
        st.progress(score / 100)

        if score >= 70:
            st.success(f"Great match! You have: {', '.join(matched)}")
        elif score >= 40:
            st.warning(f"Good start! You have: {', '.join(matched)}")
        else:
            st.error(f"Keep learning! You matched: {', '.join(matched) if matched else 'none yet'}")

        # Smart recommendations tied to real data
        missing = [s for s in market_skills if s not in user_skill_list]
        if missing:
            st.divider()
            st.subheader("📈 Skill Gap Impact")
            for skill in missing[:3]:
                skill_count = df['description_tokens'].dropna().apply(
                    lambda x: skill in str(x).lower()
                ).sum()
                pct = int((skill_count / len(df)) * 100)
                skill_salary = df[
                    df['description_tokens'].dropna().apply(
                        lambda x: skill in str(x).lower()
                    ) & df['salary_yearly'].notna()
                ]['salary_yearly'].mean()
                if skill_salary:
                    st.info(f"➕ Adding **{skill.upper()}** → appears in **{pct}%** of jobs | Avg salary: **${skill_salary:,.0f}**")
                else:
                    st.info(f"➕ Adding **{skill.upper()}** → appears in **{pct}%** of all job postings")

    st.divider()

    st.subheader("Resume Analyzer")
    st.markdown("Upload your resume and get AI-powered feedback based on the job market.")

    upload_option = st.radio("Choose input method:",
        ["Upload File", "Paste Text"], horizontal=True)

    resume_text = ""

    if upload_option == "Upload File":
        uploaded_file = st.file_uploader("Upload your resume", type=["txt", "pdf"])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                resume_text = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                import PyPDF2
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                for page in pdf_reader.pages:
                    resume_text += page.extract_text()
    else:
        resume_text = st.text_area("Paste your resume text here:",
            placeholder="Paste your resume content here...",
            height=200)

    if resume_text:
        with st.spinner("Analyzing your resume..."):

            # Calculate real match from dataset
            resume_lower = resume_text.lower()
            market_skills = ['python', 'sql', 'tableau', 'excel', 'power_bi', 'r', 'spark', 'aws']
            matched_skills = [s for s in market_skills if s in resume_lower]
            missing_skills = [s for s in market_skills if s not in resume_lower]
            match_pct = int((len(matched_skills) / len(market_skills)) * 100)

            # Show match percentage
            col1, col2 = st.columns(2)
            col1.metric("Resume Match Score", f"{match_pct}%")
            col2.metric("Skills Matched", f"{len(matched_skills)}/{len(market_skills)}")
            st.progress(match_pct / 100)

            if matched_skills:
                st.success(f"✅ Skills found: {', '.join([s.upper() for s in matched_skills])}")
            if missing_skills:
                st.error(f"❌ Missing skills: {', '.join([s.upper() for s in missing_skills])}")

            st.divider()

            resume_context = f"""
            You are a career expert. Analyze this resume against the current Data Analyst job market.
            Job market data:
            - Most in demand skills: SQL, Python, Tableau, Excel, Power BI
            - Average salary: $85,000/year
            - Top hiring locations: Anywhere, United States, New York
            - Resume already matched these skills: {matched_skills}
            - Resume is missing these skills: {missing_skills}
            Resume:
            {resume_text}
            Provide:
            1. Skills found in the resume that match job market demand
            2. Missing skills the person should learn
            3. Overall resume score out of 10
            4. Top 3 specific recommendations to improve
            Keep it concise and actionable.
            """
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": resume_context},
                    {"role": "user", "content": "Analyze my resume"}
                ]
            )
            analysis = response.choices[0].message.content
            st.success("AI Analysis:")
            st.write(analysis)

elif page == "🤖 Ask AI":
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

elif page == "📋 Data Explorer":
    st.subheader("Raw Data Explorer")
    st.markdown("Browse through all job postings in the dataset.")

    location_filter = st.sidebar.multiselect(
        "Filter by Location",
        options=df["location"].dropna().unique(),
        default=[]
    )
    if location_filter:
        filtered_df = df[df["location"].isin(location_filter)]
    else:
        filtered_df = df

    search = st.text_input("Search by job title or company:",
        placeholder="e.g. Data Analyst, Google, Microsoft")

    if search:
        searched_df = filtered_df[
            filtered_df["title"].str.contains(search, case=False, na=False) |
            filtered_df["company_name"].str.contains(search, case=False, na=False)
        ]
    else:
        searched_df = filtered_df

    st.dataframe(searched_df[["title", "company_name", "location",
                                "salary_yearly", "work_from_home"]])
    st.markdown(f"Showing **{len(searched_df)}** job postings")