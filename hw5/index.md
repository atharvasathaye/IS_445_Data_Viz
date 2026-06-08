---
layout: none
title: Bigfoot Visualizations
---

<script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>

<style>
body {
  font-family: 'Segoe UI', sans-serif;
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: #f7f9fb;
  color: #222;
}
h1, h2 {
  text-align: center;
}
.viz-container {
  margin: 2rem 0;
  background: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #3367d6;
  color: white;
  border: none;
  border-radius: 6px;
  margin-right: 1rem;
  cursor: pointer;
}
button:hover {
  background-color: #264f9c;
}
</style>

# Homework 5: Bigfoot Sightings Visualization

<div class="viz-container">
  <h2>Bigfoot Reports per Year</h2>
  <p>This bar chart shows how many Bigfoot sightings were reported each year. The color intensity helps highlight years with more reports.</p>
  <div id="chart1"></div>
</div>

<div class="viz-container">
  <h2>Bigfoot Sightings by Location and Season</h2>
  <p>This interactive map shows the location of sightings, color-coded by season. Use the legend to filter and explore seasonal patterns.</p>
  <div id="chart2"></div>
</div>

---

## Write-up

### Plot 1: Bigfoot Sightings Per Year

This bar chart displays the total number of reported Bigfoot sightings for each year. It helps identify trends over time, such as whether sightings are increasing or decreasing. The x-axis shows the year as an ordinal variable, while the y-axis encodes the count as a quantitative variable. Tooltips provide exact sighting counts on hover.

For transformation, the `date` field was parsed into datetime and the `year` extracted. Then, I grouped the data by year and used `.size()` to count the number of reports. I didn’t use a color map since the bar height clearly communicates variation in counts. This plot is new for Homework 5 and wasn’t reused from previous assignments. It was exported to JSON for Vega-Lite embedding.

### Plot 2: Sightings by Location and Season

The second plot is a scatter plot of sightings across North America, using longitude and latitude as coordinates. Each dot is color-coded by season, allowing us to see both where and when sightings happen. I used color as a nominal encoding and position as quantitative.

To prepare this, I removed entries missing location or season data. Each dot includes a tooltip showing the state, location, date, and season. This plot is also new and wasn’t reused. It was saved in HTML and JSON formats.

---

## Interactivity

The first chart includes tooltips that show exact sighting counts for each year. The second chart includes interactivity via Altair’s `selection_point`, which lets users filter the data by season through the legend. This makes it easier to spot seasonal patterns and regional trends without overwhelming the map.

---

## Resources

<a href="https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/bfro_reports_fall2022.csv">
  <button>The Data</button>
</a>

<a href="https://github.com/atharvasathaye/hw5/blob/main/Workbook.ipynb">
  <button>The Analysis</button>
</a>

<script>
vegaEmbed('#chart1', 'charts/bigfoot_reports_per_year.json', { actions: false });
vegaEmbed('#chart2', 'charts/bigfoot_map_interactive.json', { actions: false });
</script>
