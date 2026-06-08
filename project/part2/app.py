
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

st.set_page_config(layout="wide")
st.title("Developer Observatory: 2024 Stack Overflow Survey (Full Dataset)")
st.markdown("**Group Members:** Atharva Sathaye, Poojan Shah, Anupama Singh, Liao Vincent, Kim Alex")

# Load dataset
df = pd.read_csv("survey_results_public.csv", low_memory=False)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Learning Methods vs Experience",
    "Language Usage by Country",
    "Coding Experience Distribution",
    "AI Tool Usage by Task",
    "Compensation by Job Role"
])

with tab1:
    st.header("Learning Methods vs Experience")

    df_learn = df[['YearsCode', 'LearnCode']].dropna()
    df_learn['YearsCode'] = df_learn['YearsCode'].replace({'Less than 1 year': 0, 'More than 50 years': 51}).astype(float)
    df_learn['LearnList'] = df_learn['LearnCode'].str.split(';')
    df_learn = df_learn.explode('LearnList')
    learn_exp = df_learn.groupby('LearnList').agg(avg_exp=('YearsCode', 'mean'), count=('YearsCode', 'count')).reset_index()
    learn_exp = learn_exp[learn_exp['count'] > 50]
    learn_exp['norm_exp'] = (learn_exp['avg_exp'] - learn_exp['avg_exp'].min()) / (learn_exp['avg_exp'].max() - learn_exp['avg_exp'].min())

    fig = px.scatter(
        learn_exp,
        x="LearnList",
        y="avg_exp",
        size="count",
        color="norm_exp",
        color_continuous_scale="Inferno",
        size_max=60,
        hover_name="LearnList",
        hover_data=["count", "avg_exp"]
    )

    fig.add_trace(go.Scatter(
        x=learn_exp["LearnList"],
        y=learn_exp["avg_exp"],
        mode='lines+markers',
        line=dict(color='rgba(0, 0, 0, 0.3)', width=2),
        marker=dict(size=5, color='black'),
        showlegend=False
    ))

    fig.update_layout(
        title="Learning Methods vs Experience",
        xaxis_title="Learning Resource",
        yaxis_title="Average Experience (Years)",
        xaxis_tickangle=-45,
        margin=dict(t=60, l=50, r=50, b=200),
        height=600,
        template="plotly_white"
    )

    st.plotly_chart(fig)
    st.markdown("This chart shows how experienced developers are based on different ways they learned to code...")

with tab2:
    st.header("Programming Language Usage and Country Trends")

    alt.data_transformers.enable('default', max_rows=None)
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
    ).add_params(click).properties(width=300, height=400, title="Top Programming Languages Globally")

    right_data = lang_df.groupby(['Language', 'Country']).size().reset_index(name='Count')

    pie_chart = alt.Chart(right_data).transform_filter(click).transform_window(
        rank='rank(Count)',
        sort=[alt.SortField('Count', order='descending')],
        groupby=['Language']
    ).transform_filter(alt.datum.rank <= 10).encode(
        theta='Count:Q',
        color=alt.Color('Country:N', legend=alt.Legend(title="Country")),
        tooltip=['Country:N', 'Count:Q']
    ).mark_arc(innerRadius=50, outerRadius=120).properties(width=350, height=400, title="Top 10 Country Share (Donut)")

    st.altair_chart((left_chart | pie_chart).configure_view(stroke=None).resolve_scale())
    st.markdown("This interactive plot shows the top programming languages globally and the top 10 countries using the selected language...")

with tab3:
    st.header("Distribution of Professional Coding Experience")

    df_exp = df[['YearsCodePro']].dropna()
    df_exp['YearsCodePro'] = df_exp['YearsCodePro'].replace({
        'Less than 1 year': 0,
        'More than 50 years': 51
    })
    df_exp['YearsCodePro'] = pd.to_numeric(df_exp['YearsCodePro'], errors='coerce')
    df_exp = df_exp.dropna()

    fig = px.histogram(
        df_exp,
        x='YearsCodePro',
        nbins=50,
        marginal="rug",
        opacity=0.75,
        color_discrete_sequence=['#1f77b4'],
        title="Distribution of Professional Coding Experience"
    )

    fig.update_layout(
        xaxis_title="Years of Professional Coding",
        yaxis_title="Count",
        bargap=0.05,
        hovermode="x unified"
    )

    st.plotly_chart(fig)
    st.markdown("This plot shows how many years of coding experience developers have...")

with tab4:
    st.header("AI Tool Usage by Task")

    df_ai = df.copy()
    ai_cols = ['AIToolCurrently Using', 'AIToolInterested in Using', 'AIToolNot interested in Using']
    ai_long = pd.DataFrame(columns=['Task', 'Status'])

    for col, label in zip(ai_cols, ['Currently Using', 'Interested', 'Not Interested']):
        temp = df_ai[[col]].dropna().copy()
        temp['Status'] = label
        temp['Task'] = temp[col].str.split(';')
        temp = temp.explode('Task')[['Task', 'Status']]
        ai_long = pd.concat([ai_long, temp], axis=0)

    ai_long = ai_long.groupby(['Task', 'Status']).size().reset_index(name='Count')
    top_tasks = ai_long.groupby('Task')['Count'].sum().nlargest(12).index
    ai_long = ai_long[ai_long['Task'].isin(top_tasks)]

    status_param = alt.param(
        name='StatusSelector',
        bind=alt.binding_select(options=['All', 'Currently Using', 'Interested', 'Not Interested'], name='Filter by Status:'),
        value='All'
    )

    chart = alt.Chart(ai_long).mark_bar().encode(
        y=alt.Y('Task:N', sort='-x'),
        x=alt.X('Count:Q'),
        color='Status:N',
        tooltip=['Task', 'Status', 'Count']
    ).add_params(status_param).transform_filter(
        (alt.datum.Status == status_param) | (status_param == 'All')
    ).properties(title='AI Task Adoption: Current vs Interested vs Not Interested', width=700)

    st.altair_chart(chart)
    st.markdown("This plot shows how developers are using AI tools across tasks...")

with tab5:
    st.header("Compensation by Developer Type and Country")

    alt.data_transformers.disable_max_rows()
    df_salary_clean = df[['Country', 'DevType', 'CompTotal']].dropna()
    df_salary_clean['CompTotal'] = df_salary_clean['CompTotal'].astype(int)
    df_salary_clean['DevType'] = df_salary_clean['DevType'].apply(lambda x: 'Other' if str(x).startswith('Other') else str(x).strip())
    low, high = df_salary_clean['CompTotal'].quantile([0.05, 0.95])
    df_salary_filtered = df_salary_clean[(df_salary_clean['CompTotal'] >= low) & (df_salary_clean['CompTotal'] <= high)]

    dropdown = alt.binding_select(
        options=[
            'United States of America', 'Germany', 'India', 'United Kingdom of Great Britain and Northern Ireland',
            'Ukraine', 'France', 'Canada', 'Poland', 'Netherlands', 'Brazil'
        ],
        name='Country: '
    )

    country_param = alt.param(
        value='United States of America',
        bind=dropdown,
        name='selected_country'
    )

    salary_bar_chart = alt.Chart(df_salary_filtered).mark_bar().encode(
        x=alt.X('DevType:N', sort='-y', title='Job Position Type'),
        y=alt.Y('CompTotal:Q', aggregate='mean', title='Average Compensation (local currency)'),
        color=alt.Color('DevType:N', legend=alt.Legend(title="Developer Type")),
        tooltip=['DevType:N', alt.Tooltip('CompTotal:Q', aggregate='mean', title='Avg Compensation')]
    ).add_params(country_param).transform_filter(
        alt.datum.Country == country_param
    ).properties(
        title='Average Compensation by Job Position Type (Select Top 10 Countries)',
        width=800,
        height=400
    ).configure_axisX(labelAngle=-45)

    st.altair_chart(salary_bar_chart)
    st.markdown("In Compensation vs Job Position Type plot, we try to demonstrate average compensation in different job roles...")

