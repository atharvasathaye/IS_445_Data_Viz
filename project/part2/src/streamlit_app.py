
import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("survey_results_public.csv")
lang_df = df[['Country', 'LanguageHaveWorkedWith']].dropna()
lang_df = lang_df.assign(Language=lang_df['LanguageHaveWorkedWith'].str.split(';')).explode('Language')
lang_df['Language'] = lang_df['Language'].str.strip()

# Sidebar
st.sidebar.title("IS445 Final Project - Group Observatory")
st.sidebar.markdown("**Group Members:** Add your names here")

st.title("Developer Trends: 2024 Stack Overflow Survey Observatory")

# ---------------- Chart 1 ----------------
st.header("1. AI Task Adoption: Current vs. Interested")
st.markdown("This visualization explores how developers are currently using AI tools and where they are most interested in adopting them.")
st.image("chart_ai_task_adoption.png")  # Replace with chart or code

# ---------------- Chart 2 ----------------
st.header("2. Developer Compensation by Role")
st.markdown("We examine how compensation varies across different developer roles and countries.")
st.image("chart_compensation.png")  # Replace with chart or code

# ---------------- Chart 3 ----------------
st.header("3. Coding Experience Distribution")
st.markdown("The histogram and KDE plot below shows the distribution of professional coding experience.")
st.image("chart_experience.png")  # Replace with chart or code

# ---------------- Chart 4 ----------------
st.header("4. Interactive Language Explorer")
st.markdown("Click a language to view its usage across the top countries (bubble chart).")

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
    x=alt.X('Country:N', sort='-y'),
    y=alt.Y('row:N', axis=None),
    size=alt.Size('Count:Q', scale=alt.Scale(range=[100, 2000]), legend=alt.Legend(title="Usage Count")),
    color=alt.Color('Country:N', legend=None),
    tooltip=['Country:N', 'Count:Q']
).properties(width=500, height=400)

chart = (left_chart | bubble_chart).configure_view(stroke=None)
chart.spacing = 50
st.altair_chart(chart)
