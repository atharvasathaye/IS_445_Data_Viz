
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

st.title("Developer Trends: 2024 Stack Overflow Survey Observatory")
st.markdown("**Group Members:** Add your group member names here")
st.markdown("This dashboard explores trends in developer tools, AI adoption, compensation, and language preferences using the 2024 Stack Overflow Developer Survey (sample).")

# Load the trimmed dataset
df = pd.read_csv("survey_results_sample.csv")
lang_df = df[['Country', 'LanguageHaveWorkedWith']].dropna()
lang_df = lang_df.assign(Language=lang_df['LanguageHaveWorkedWith'].str.split(';')).explode('Language')
lang_df['Language'] = lang_df['Language'].str.strip()

# ---------------- Chart 1: AI Task Adoption (simulated with image or placeholder) ----------------
st.header("1. AI Task Adoption by Developers")
st.markdown("This visualization shows how developers are currently using AI tools and where they are most interested in adopting them.")
st.image("chart_ai_task_adoption.png")

# ---------------- Chart 2: Compensation by Job Role (simulated) ----------------
st.header("2. Developer Compensation by Role")
st.markdown("Explore how compensation varies across roles and countries based on developer-reported salaries.")
st.image("chart_compensation.png")

# ---------------- Chart 3: Coding Experience Distribution (simulated) ----------------
st.header("3. Professional Coding Experience Distribution")
st.markdown("This histogram and density plot shows the spread of years of professional coding experience.")
st.image("chart_experience.png")

# ---------------- Chart 4: Interactive Language Explorer ----------------
st.header("4. Programming Language Popularity by Country")
st.markdown("Click a language on the left to view where it's most used globally.")

lang_counts = lang_df['Language'].value_counts().head(15).reset_index()
lang_counts.columns = ['Language', 'Count']

click = alt.selection_point(fields=['Language'])

left_chart = alt.Chart(lang_counts).mark_bar().encode(
    x='Count:Q',
    y=alt.Y('Language:N', sort='-x'),
    tooltip=['Language:N', 'Count:Q'],
    color=alt.condition(click, alt.value('#1f77b4'), alt.value('#d3d3d3'))
).add_params(click).properties(width=300, height=400)

right_data = lang_df.groupby(['Language', 'Country']).size().reset_index(name='Count')
right_data['row'] = 'All'

bubble_chart = alt.Chart(right_data).transform_filter(click).transform_window(
    rank='rank(Count)',
    sort=[alt.SortField('Count', order='descending')],
    groupby=['Language']
).transform_filter(
    alt.datum.rank <= 15
).mark_circle().encode(
    x=alt.X('Country:N', sort='-y', title='Country'),
    y=alt.Y('row:N', axis=None),
    size=alt.Size('Count:Q', scale=alt.Scale(range=[100, 2000]), legend=alt.Legend(title="Usage Count")),
    color=alt.Color('Country:N', legend=None),
    tooltip=['Country:N', 'Count:Q']
).properties(width=500, height=400)

chart = (left_chart | bubble_chart).configure_view(stroke=None)
chart.spacing = 50
st.altair_chart(chart)
