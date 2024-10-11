
import streamlit as st
import pandas as pd
import plotly.express as px
import re
import warnings

warnings.filterwarnings("ignore")

data = pd.read_csv("ai_ml_jobs_linkedin.csv")

data['sector'] = data['sector'].fillna('NA')
data = data.dropna(subset=['publishedAt'])

data['applicationsCount'] = data['applicationsCount'].apply(lambda x: int(re.findall(r'(\d+)', x)[0]))

data.to_pickle('ai_ml_jobs_data.pkl')
data = pd.read_pickle('ai_ml_jobs_data.pkl')
def get_states(row):
    row_lower = row.lower()
    if ',' in row_lower:
        return row.split(', ')[1]
    elif 'new york' in row_lower:
        return 'NY'
    elif 'seattle' in row_lower:
        return 'WA'
    elif 'houston' in row_lower or 'dallas' in row_lower:
        return 'TX'
    elif 'chicago' in row_lower:
        return 'IL'
    elif 'los angeles' in row_lower or 'san francisco' in row_lower:
        return 'CA'
    elif 'atlanta' in row_lower:
        return 'GA'
    elif 'panama' in row_lower:
        return 'FL'

data['stateAt'] = data['location'].apply(get_states)

st.title("USA Job Market Dashboard")
user_input = st.text_area("Enter your full name")
if user_input:
    st.write(f"Hello, {user_input}!")

job_profile = st.text_input("What job profile are you looking for?")
if job_profile:
    st.write(f"You are looking for a job profile in: {job_profile}")    

experience = st.selectbox(
    "How many years of experience do you have?",
    options=["Select an option","Internship", "0-1 years", "1-3 years", "3-5 years", "5+ years"]
)
if experience != "Select an option":
    st.write(f"You have selected: {experience} of experience.")    

st.title("USA Job Market Dashboard")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    popular_state_for_applicants = data.groupby(['stateAt']).sum(['applicationsCount']).reset_index().sort_values(['applicationsCount'], ascending=False)
    fig_choropleth = px.choropleth(
        popular_state_for_applicants,
        locations='stateAt',
        locationmode='USA-states',
        color='applicationsCount',
        color_continuous_scale=px.colors.sequential.Plasma,
        title='Choropleth Map of Popular States for Applicants in the USA',
        labels={'applicationsCount': 'Number of Applications'},
        scope='usa'
    )
    st.plotly_chart(fig_choropleth, use_container_width=True)

with col2:
    top_10_requirements = data.groupby(['title'])['location'].count().reset_index().sort_values(['location'], ascending=False).head(10)
    fig_top_titles = px.bar(top_10_requirements, x='title', y='location', title='Top 10 Job Titles by Location Count', template='plotly_dark')
    st.plotly_chart(fig_top_titles, use_container_width=True)

with col3:
    level_based_count = data.groupby('experienceLevel')['title'].count().reset_index().sort_values(['title'])
    fig_experience = px.pie(level_based_count, names='experienceLevel', values='title', title='Distribution of Job Titles by Experience Level', color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig_experience, use_container_width=True)

with col4:
    top_10_hiring_companies = data.groupby(['companyName'])['title'].count().reset_index().sort_values(['title'], ascending=False).head(10)
    fig_hiring_companies = px.pie(top_10_hiring_companies, names='companyName', values='title', title='Top 10 Hiring Companies', hole=0.4, color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig_hiring_companies, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    sectorwise_jobs_top_10 = data.groupby(['sector'])['title'].count().reset_index().sort_values(['title'], ascending=False).head(10)
    fig_heatmap = px.imshow(sectorwise_jobs_top_10[['title']].T, 
                             labels=dict(x='Sector', y='Job Count'), 
                             x=sectorwise_jobs_top_10['sector'], 
                             y=['Job Count'], 
                             color_continuous_scale=px.colors.sequential.Viridis, 
                             title='Heatmap of Job Counts by Sector')
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col6:
    count_per_contract_type = data.groupby(['contractType'])['title'].count().reset_index().sort_values(['title'], ascending=False)
    fig_contract_type = px.pie(count_per_contract_type, names='contractType', values='title', title='Distribution of Job Titles by Contract Type', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_contract_type, use_container_width=True)

st.sidebar.header("About")
st.sidebar.text("This dashboard provides insights into the USA job market based on LinkedIn job postings.")
