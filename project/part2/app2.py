
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

st.title("Developer Trends: 2024 Stack Overflow Survey Observatory")
st.markdown("**Group Members:** Add your group member names here")
st.markdown("This dashboard explores trends in developer tools, AI adoption, compensation, and language preferences using the 2024 Stack Overflow Developer Survey (sample).")

df = pd.read_csv("survey_results_sample.csv")

# 1. Simulated AI Task Adoption (mocked bar chart)
st.header("1. AI Task Adoption by Developers")
st.markdown("This chart simulates how developers use AI for various coding tasks (sample values shown).")

ai_data = pd.DataFrame({
    "Task": ["Writing code", "Debugging", "Testing", "Documentation", "Deployment"],
    "Currently Using": [4000, 3000, 2000, 1500, 1000],
    "Interested": [3500, 3200, 2800, 2000, 1800],
    "Not Interested": [800, 1200, 1500, 1800, 2200]
}).melt(id_vars="Task", var_name="Status", value_name="Count")

ai_chart = alt.Chart(ai_data).mark_bar().encode(
    x="Count:Q",
    y=alt.Y("Task:N", sort="-x"),
    color="Status:N",
    tooltip=["Task", "Status", "Count"]
).properties(width=700, height=400)

st.altair_chart(ai_chart)

# 2. Simulated Compensation by Role (mocked chart)
st.header("2. Developer Compensation by Role (Simulated)")
st.markdown("Average compensation by developer role in USD (sample data).")

comp_data = pd.DataFrame({
    "Role": ["Front-end Dev", "Back-end Dev", "Full Stack", "Mobile Dev", "Data Scientist"],
    "AvgSalary": [90000, 105000, 110000, 95000, 120000]
})

comp_chart = alt.Chart(comp_data).mark_bar().encode(
    x=alt.X("AvgSalary:Q", title="Average Salary (USD)"),
    y=alt.Y("Role:N", sort="-x"),
    tooltip=["Role", "AvgSalary"]
).properties(width=700, height=400)

st.altair_chart(comp_chart)

# 3. Coding Experience Histogram
st.header("3. Distribution of Professional Coding Experience")
st.markdown("This histogram shows how many years of professional coding experience respondents have.")

exp_chart = alt.Chart(df).transform_filter(
    alt.datum.YearsCodePro != "NA"
).mark_bar().encode(
    alt.X("YearsCodePro:Q", bin=alt.Bin(maxbins=30), title="Years of Experience"),
    y='count():Q',
    tooltip=['count()']
).properties(width=700, height=400)

st.altair_chart(exp_chart)

# 4. Language Explorer with Bubble Chart
st.header("4. Programming Language Popularity by Country")
st.markdown("Click a language on the left to view where it's most used globally (top 15 countries).")

lang_df = df[['Country', 'LanguageHaveWorkedWith']].dropna()
lang_df = lang_df.assign(Language=lang_df['LanguageHaveWorkedWith'].str.split(';')).explode('Language')
lang_df['Language'] = lang_df['Language'].str.strip()

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

st.altair_chart((left_chart | bubble_chart).configure_view(stroke=None).resolve_scale(size="independent"))
