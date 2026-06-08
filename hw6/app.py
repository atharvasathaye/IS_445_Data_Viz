import streamlit as st
import pandas as pd
import altair as alt

st.title("🛸 UFO Sightings Analysis")
st.markdown("This app visualizes UFO sighting data to explore shapes and trends over time.")

url = "https://github.com/UIUC-iSchool-DataViz/is445_data/raw/main/ufo-scrubbed-geocoded-time-standardized-00.csv"
df = pd.read_csv(url, low_memory=False)

if 'date_time' not in df.columns:
    df.columns = df.columns.str.strip()
    if 'datetime' in df.columns:
        df.rename(columns={'datetime': 'date_time'}, inplace=True)
    elif df.columns[0].lower().startswith("10/10/"):
        df.columns = ['date_time', 'city', 'state', 'country', 'shape', 'duration_seconds',
                      'duration_hours_min', 'comments', 'date_posted', 'latitude', 'longitude']

df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
df['year'] = df['date_time'].dt.year

shape_counts = df['shape'].value_counts().reset_index()
shape_counts.columns = ['shape', 'count']

st.subheader("🔺 Most Common UFO Shapes")
bar_chart = alt.Chart(shape_counts.head(10)).mark_bar().encode(
    x=alt.X('shape:N', sort='-y', title='UFO Shape'),
    y=alt.Y('count:Q', title='Number of Sightings'),
    tooltip=['shape', 'count']
).properties(width=600, height=400)

st.altair_chart(bar_chart, use_container_width=True)

st.markdown("""
**Plot 1 Highlights:**  
This bar chart highlights the most frequently reported UFO shapes. The most common shape appears to be *light*, followed by *circle* and *triangle*.

**Design Choices:**  
A bar chart was used to emphasize categorical frequency. The shapes are sorted in descending order and have tooltips to support exploration.

**Future Improvements:**  
I would add interactivity like filtering by country or year.
""")

sightings_by_year = df.groupby('year').size().reset_index(name='count')
sightings_by_year = sightings_by_year[sightings_by_year['year'].between(1950, 2020)]

st.subheader("📈 UFO Sightings Over Time")
line_chart = alt.Chart(sightings_by_year).mark_line(point=True).encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('count:Q', title='Number of Sightings'),
    tooltip=['year', 'count']
).properties(width=700, height=400)

st.altair_chart(line_chart, use_container_width=True)

st.markdown("""
**Plot 2 Highlights:**  
This line chart shows the number of UFO sightings reported each year. Sightings increased during the 1990s and early 2000s, before leveling off.

**Design Choices:**  
A line chart with points was used to show both trend and yearly precision. Tooltips help reveal exact counts.

**Future Improvements:**  
I would explore adding regional filters or interactive sliders.
""")
