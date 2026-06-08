
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Developer Observatory: 2024 Stack Overflow Survey (Sample)")
st.markdown("**Group Members:** Atharva Sathaye, Poojan Shah, Anupama Singh, Liao Vincent, Kim Alex")

df = pd.read_csv("survey_results_sample.csv")
df['YearsCodePro'] = pd.to_numeric(df['YearsCodePro'], errors='coerce')

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "AI Tool Usage",
    "Compensation by Role",
    "Coding Experience",
    "Learning Methods",
    "Language Usage Explorer"
])

with tab1:
    st.header("AI Tool Usage by Task (Sample Categories)")
    ai_df = pd.DataFrame({
        "Task": ["Writing code", "Search answers", "Debugging", "Documenting", "Testing"],
        "Currently Using": [4000, 3500, 3200, 2900, 2700],
        "Interested": [2000, 2200, 2500, 2600, 2400],
        "Not Interested": [1000, 800, 700, 500, 400]
    }).melt(id_vars="Task", var_name="Status", value_name="Count")

    ai_chart = alt.Chart(ai_df).mark_bar().encode(
        x=alt.X("Count:Q"),
        y=alt.Y("Task:N", sort='-x'),
        color=alt.Color("Status:N"),
        tooltip=["Task", "Status", "Count"]
    ).properties(width=700, height=400)

    st.altair_chart(ai_chart)

with tab2:
    st.header("Average Salary by Developer Type (Simulated Grouping)")
    role_df = pd.DataFrame({
        "Developer Type": [
            "Mobile Dev", "Front-end Dev", "Back-end Dev", "Full Stack Dev", 
            "Cloud Engineer", "Data Scientist", "Product Manager"
        ],
        "Country": ["United States of America"] * 7,
        "Average Compensation": [140000, 115000, 130000, 135000, 145000, 150000, 160000]
    })

    sel_country = st.selectbox("Select Country:", sorted(role_df["Country"].unique()))
    filtered = role_df[role_df["Country"] == sel_country]

    comp_chart = alt.Chart(filtered).mark_bar().encode(
        x=alt.X("Average Compensation:Q"),
        y=alt.Y("Developer Type:N", sort="-x"),
        tooltip=["Developer Type", "Average Compensation"]
    ).properties(width=700, height=400)

    st.altair_chart(comp_chart)

with tab3:
    st.header("Distribution of Professional Coding Experience")
    st.markdown("This histogram and KDE plot show the years of professional coding experience.")

    fig = px.histogram(df, x="YearsCodePro", nbins=30, marginal="box", 
                       title="Years of Professional Coding", opacity=0.7)
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Preferred Learning Methods vs Experience")
    st.markdown("Bubble chart showing correlation between learning method and years of experience.")

    bubble_df = pd.DataFrame({
        "LearningMethod": ["Online Courses", "Books", "Colleagues", "Bootcamps", "University"],
        "YearsCodePro": [3, 6, 9, 4, 8],
        "Count": [1000, 800, 600, 400, 300]
    })

    fig_bubble = px.scatter(bubble_df, x="YearsCodePro", y="LearningMethod", 
                            size="Count", color="LearningMethod", 
                            labels={"YearsCodePro": "Years Coding"},
                            title="Learning Preferences by Experience")

    st.plotly_chart(fig_bubble, use_container_width=True)

with tab5:
    st.header("Interactive Language Usage by Country")
    st.markdown("Click a language to view top 15 countries using it.")

    lang_df = df[['Country', 'LanguageHaveWorkedWith']].dropna()
    lang_df = lang_df.assign(Language=lang_df['LanguageHaveWorkedWith'].str.split(';')).explode('Language')
    lang_df['Language'] = lang_df['Language'].str.strip()

    lang_counts = lang_df['Language'].value_counts().head(15).reset_index()
    lang_counts.columns = ['Language', 'Count']
    click = alt.selection_point(fields=['Language'])

    left = alt.Chart(lang_counts).mark_bar().encode(
        x='Count:Q',
        y=alt.Y('Language:N', sort='-x'),
        tooltip=['Language:N', 'Count:Q'],
        color=alt.condition(click, alt.value('#1f77b4'), alt.value('#d3d3d3'))
    ).add_params(click).properties(width=300, height=400)

    right_data = lang_df.groupby(['Language', 'Country']).size().reset_index(name='Count')
    right_data['row'] = 'All'

    right = alt.Chart(right_data).transform_filter(click).transform_window(
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

    st.altair_chart((left | right).configure_view(stroke=None).resolve_scale(size="independent"))
