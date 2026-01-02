"""
Streamlit Frontend - Modern Job Application Assistant UI
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import List, Dict
import json

# Page configuration
st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE_URL = "http://localhost:8000"

# Custom CSS for modern design
st.markdown("""
<style>
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-bg: #1e1e2e;
        --card-bg: #2a2a3e;
    }
    
    .stCard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stCard:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        margin: 10px 0;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(102, 126, 234, 0.6);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 8px 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .job-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        transform: translateX(4px);
    }
    
    .progress-bar {
        background: #e5e7eb;
        border-radius: 12px;
        height: 12px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 12px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if 'jobs' not in st.session_state:
        st.session_state.jobs = []
    if 'applications' not in st.session_state:
        st.session_state.applications = []
    if 'profile' not in st.session_state:
        st.session_state.profile = None


def api_request(endpoint: str, method: str = "GET", data: dict = None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            return None
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None


def render_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="gradient-text">💼 Job Application Assistant</h1>', unsafe_allow_html=True)
        st.markdown("**AI-Powered Job Search & Application Automation**")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()


def render_stats():
    st.markdown("### 📊 Dashboard Overview")
    col1, col2, col3, col4 = st.columns(4)
    jobs_count = len(st.session_state.jobs)
    applications_count = len(st.session_state.applications)
    pending_count = sum(1 for app in st.session_state.applications if app.get('status') == 'pending')
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Jobs</div>
            <div class="stat-number">{jobs_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <div class="stat-label">Applications</div>
            <div class="stat-number">{applications_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
            <div class="stat-label">Pending</div>
            <div class="stat-number">{pending_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        success_rate = (applications_count / jobs_count * 100) if jobs_count > 0 else 0
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
            <div class="stat-label">Success Rate</div>
            <div class="stat-number">{success_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)


def render_job_search():
    st.markdown("### 🔍 Search Jobs")
    with st.form("job_search_form"):
        col1, col2 = st.columns(2)
        with col1:
            keywords = st.text_input("Keywords", placeholder="e.g., Software Engineer, Data Scientist")
            platforms = st.multiselect(
                "Platforms",
                ["linkedin", "indeed"],
                default=["linkedin", "indeed"]
            )
        with col2:
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
            max_results = st.slider("Max Results per Platform", 10, 100, 50)
        submitted = st.form_submit_button("🚀 Search Jobs", use_container_width=True)
        if submitted and keywords:
            with st.spinner("Searching for jobs..."):
                result = api_request(
                    "/api/jobs/search",
                    method="POST",
                    data={
                        "keywords": keywords,
                        "location": location,
                        "platforms": platforms,
                        "max_results_per_platform": max_results
                    }
                )
                if result and result.get('success'):
                    st.session_state.jobs = result.get('jobs', [])
                    st.success(f"✅ Found {result.get('count', 0)} jobs!")
                    st.rerun()


def render_job_list():
    st.markdown("### 📋 Job Listings")
    if not st.session_state.jobs:
        st.info("No jobs found. Start by searching for jobs above!")
        return
    col1, col2, col3 = st.columns(3)
    with col1:
        source_filter = st.selectbox(
            "Filter by Source",
            ["All"] + list(set(job.get('source', 'Unknown') for job in st.session_state.jobs))
        )
    with col2:
        sort_by = st.selectbox("Sort by", ["Recent", "Match Score", "Company"])
    with col3:
        view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)
    filtered_jobs = st.session_state.jobs
    if source_filter != "All":
        filtered_jobs = [j for j in filtered_jobs if j.get('source') == source_filter]
    if sort_by == "Match Score":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x.get('match_score', 0), reverse=True)
    elif sort_by == "Company":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x.get('company', ''))
    if view_mode == "Cards":
        for job in filtered_jobs:
            render_job_card(job)
    else:
        df = pd.DataFrame(filtered_jobs)
        st.dataframe(df[['title', 'company', 'location', 'source', 'match_score']], use_container_width=True)


def render_job_card(job: Dict):
    with st.container():
        st.markdown(f"""
        <div class="job-card">
            <h3>{job.get('title', 'Unknown Title')}</h3>
            <p><strong>🏢 {job.get('company', 'Unknown Company')}</strong></p>
            <p>📍 {job.get('location', 'Remote')}</p>
            <p>🔗 Source: {job.get('source', 'Unknown')}</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Analyze", key=f"analyze_{job.get('job_id')}"):
                analyze_job(job.get('job_id'))
        with col2:
            if st.button("✍️ Cover Letter", key=f"cover_{job.get('job_id')}"):
                generate_cover_letter(job.get('job_id'))
        with col3:
            if st.button("📤 Apply", key=f"apply_{job.get('job_id')}"):
                submit_application(job.get('job_id'))


def analyze_job(job_id: str):
    with st.spinner("Analyzing job..."):
        result = api_request(
            "/api/jobs/analyze",
            method="POST",
            data={"job_id": job_id}
        )
        if result and result.get('success'):
            analysis = result.get('analysis', {})
            st.success(f"Match Score: {analysis.get('match_score', 0):.1f}%")
            with st.expander("View Analysis"):
                st.json(analysis)


def generate_cover_letter(job_id: str):
    with st.spinner("Generating cover letter..."):
        result = api_request(
            "/api/cover-letter/generate",
            method="POST",
            data={"job_id": job_id, "tone": "professional"}
        )
        if result and result.get('success'):
            cover_letter = result.get('cover_letter', '')
            with st.expander("Cover Letter", expanded=True):
                st.text_area("", cover_letter, height=300)
                st.download_button(
                    "📥 Download",
                    cover_letter,
                    file_name=f"cover_letter_{job_id}.txt"
                )


def submit_application(job_id: str):
    with st.spinner("Submitting application..."):
        result = api_request(
            "/api/applications/submit",
            method="POST",
            data={"job_id": job_id, "auto_submit": False}
        )
        if result and result.get('success'):
            st.success("✅ Application submitted!")
            st.balloons()


def render_profile_section():
    st.markdown("### 👤 User Profile")
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
        with col2:
            location = st.text_input("Location")
            experience_years = st.number_input("Years of Experience", min_value=0, max_value=50)
            resume_path = st.text_input("Resume Path")
        skills = st.text_area("Skills (comma-separated)", placeholder="Python, JavaScript, React, etc.")
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)
        if submitted:
            skills_list = [s.strip() for s in skills.split(',') if s.strip()]
            result = api_request(
                "/api/profile",
                method="POST",
                data={
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "skills": skills_list,
                    "experience_years": experience_years,
                    "resume_path": resume_path
                }
            )
            if result and result.get('success'):
                st.success("✅ Profile saved!")


def main():
    init_session_state()
    with st.sidebar:
        st.markdown('<h2 style="color: #667eea;">💼 Job Assistant</h2>', unsafe_allow_html=True)
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "🔍 Search Jobs", "📋 Applications", "👤 Profile"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        theme = st.selectbox("Theme", ["Modern Purple", "Ocean Blue", "Forest Green"])
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
    render_header()
    st.markdown("---")
    if page == "🏠 Dashboard":
        render_stats()
        st.markdown("---")
        render_job_list()
    elif page == "🔍 Search Jobs":
        render_job_search()
        st.markdown("---")
        render_job_list()
    elif page == "📋 Applications":
        st.markdown("### 📋 My Applications")
        result = api_request("/api/applications")
        if result and result.get('success'):
            st.session_state.applications = result.get('applications', [])
            if st.session_state.applications:
                df = pd.DataFrame(st.session_state.applications)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No applications yet!")
    elif page == "👤 Profile":
        render_profile_section()


if __name__ == "__main__":
    main()
