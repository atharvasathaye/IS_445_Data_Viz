import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="UFO Sightings", layout="centered")

st.title("🛸 UFO Sightings Analysis")
st.markdown("Explore trends in UFO sightings across time and shape types using data from the [UFO Sightings dataset](https://github.com/UIUC-iSchool-DataViz/is445_data/raw/main/ufo-scrubbed-geocoded-time-standardized-00.csv).")

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

st.header("🔺 Plot 1: Most Common UFO Shapes")

shape_counts = df['shape'].value_counts().reset_index()
shape_counts.columns = ['shape', 'count']

bar_chart = alt.Chart(shape_counts.head(10)).mark_bar().encode(
    x=alt.X('shape:N', sort='-y', title='UFO Shape'),
    y=alt.Y('count:Q', title='Number of Sightings'),
    tooltip=['shape', 'count']
).properties(width=600, height=400)

st.altair_chart(bar_chart, use_container_width=True)

st.markdown("""
**What is being visualized:**  
This bar chart displays the ten most frequently reported UFO shapes. It offers insight into how witnesses categorize their sightings.

**Design choices:**  
- Bar chart format allows for easy comparison of categorical frequency.
- Sorted bars make the distribution immediately understandable.
- Tooltips reveal the exact number of sightings for each shape.
- Missing data in the shape column was excluded to ensure clarity.

**Data manipulation:**  
Used `value_counts()` to aggregate the number of sightings for each shape. Top 10 shapes were selected for focused comparison.

**What I would change:**  
I would include filters to isolate shapes over time or by country for deeper analysis.
""")

st.header("📈 Plot 2: UFO Sightings Over Time")

sightings_by_year = df.groupby('year').size().reset_index(name='count')
sightings_by_year = sightings_by_year[sightings_by_year['year'].between(1950, 2020)]

line_chart = alt.Chart(sightings_by_year).mark_line(point=True).encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('count:Q', title='Number of Sightings'),
    tooltip=['year', 'count']
).properties(width=700, height=400)

st.altair_chart(line_chart, use_container_width=True)

st.markdown("""
**What is being visualized:**  
This line chart shows the number of UFO sightings reported each year, highlighting long-term trends in reporting behavior.

**Design choices:**  
- A line chart illustrates the temporal flow of sightings.
- Point markers add precision for each year's count.
- Ordinal x-axis ensures chronological accuracy.
- Tooltips improve user insight with exact values.

**Data manipulation:**  
Converted `date_time` to datetime, extracted the `year`, grouped by it, and filtered for realistic years (1950–2020).

**What I would change:**  
I would add geographic filters or layer in shapes per year to explore how different UFO types have evolved over time.
""")

st.markdown("---")
st.markdown("📄 **Data Source**: [UFO Sightings Dataset (CSV)](https://github.com/UIUC-iSchool-DataViz/is445_data/raw/main/ufo-scrubbed-geocoded-time-standardized-00.csv)")
