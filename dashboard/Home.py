"""CogDash entry point. Run from dashboard/: streamlit run Home.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
from dashboard import views

st.set_page_config(page_title="CogDash · Cognitive research", page_icon="◉", layout="wide")
st.markdown("""<style>
 .block-container {padding-top:3.5rem; padding-bottom:2rem; max-width:1500px;}
 [data-testid="stVerticalBlock"] {gap:.65rem;}
 h1 {letter-spacing:-.6px; font-size:2rem!important; font-weight:750!important;}
 h2 {font-size:1.45rem!important;} h3 {font-size:1.13rem!important;}
 [data-testid="stMetric"] {background:#f2f6fa;border-radius:9px;padding:10px 13px;border-top:3px solid #007c91;}
 [data-testid="stMetricValue"] {font-size:1.6rem;}
 [data-testid="stSidebar"] {background:#f2f6fa;}
 .eyebrow {color:#007c91;font-size:12px;font-weight:700;letter-spacing:1.5px;margin-bottom:5px;}
 .lead {font-size:17px;line-height:1.5;color:#425670;max-width:1050px;}
 div[data-testid="stAlert"] {border-radius:7px;}
 .cog-table {width:100%;border-collapse:collapse;font-size:13px;margin:8px 0 14px;}
 .cog-table th {text-align:left!important;background:#eaf1f7;padding:9px 12px;position:sticky;top:0;}
 .cog-table td {padding:8px 12px;border-bottom:1px solid #e1e8ee;white-space:nowrap;}
 .cog-table tr:nth-child(even) td {background:#f8fafc;}
 </style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ◉ CogDash")
    st.caption("COGNITIVE RESEARCH / v2.0")

pages = {
    "Findings": [st.Page(views.home, title="Home", default=True, url_path="home"),
                 st.Page(views.research, title="Patient-Level Research", url_path="research")],
    "Explore": [st.Page(views.explorer, title="Cluster Explorer", url_path="clusters"),
                st.Page(views.profiles, title="Cognitive Profiles", url_path="profiles"),
                st.Page(views.lookup, title="Patient Lookup", url_path="lookup"),
                st.Page(views.new_profile, title="New Profile", url_path="new-profile")],
    "Compare": [st.Page(views.imputation, title="Imputation Compare", url_path="imputation"),
                st.Page(views.clinical, title="Clinical Units", url_path="clinical"),
                st.Page(views.hypotheses, title="Hypothesis Summary", url_path="hypotheses"),
                st.Page(views.advanced, title="Advanced Analytics", url_path="advanced"),
                st.Page(views.robustness, title="Robustness", url_path="robustness")],
}
page = st.navigation(pages, expanded=True)
with st.sidebar:
    st.divider()
    st.caption("Research use\n\nClinical phenotypes and treatment utility remain unconfirmed.")

try:
    page.run()
except FileNotFoundError:
    st.error("Required analysis results are missing. Restore the saved results and prepare the dashboard assets using the setup instructions.")
