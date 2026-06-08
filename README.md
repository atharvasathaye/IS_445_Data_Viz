# IS 445: Data Visualization Portfolio

This repository contains a collection of data visualization projects, labs, and assignments completed for the IS 445: Data Visualization course. The work spans foundational exploratory data analysis to complex, interactive web-based dashboards using modern Python data visualization libraries.

## Overview

The purpose of this repository is to showcase various techniques in data visualization, ranging from static plots to interactive, web-based applications. The tools utilized throughout the projects include **Python**, **Vega-Lite**, **Altair**, **Plotly**, and **Streamlit**.

## Key Projects

### 1. Developer Observatory: 2024 Stack Overflow Survey (Final Project)
**Location:** `project/part2/`  
**Technologies:** Streamlit, Plotly, Altair, Pandas

A comprehensive dashboard analyzing the 2024 Stack Overflow Developer Survey dataset. The interactive application provides insights into:
- **Learning Methods vs. Experience:** How different coding education paths correlate with developer experience.
- **Language Usage by Country:** Global trends in programming language popularity and distribution.
- **Coding Experience Distribution:** Demographics of professional coding experience.
- **AI Tool Usage by Task:** Adoption rates of AI tools for different development tasks (Current vs. Interested).
- **Compensation by Job Role:** Average compensation across various developer roles in top countries.

*Group Members: Atharva Sathaye, Poojan Shah, Anupama Singh, Liao Vincent, Kim Alex*

### 2. COVID-19 Dashboard & Movie Data Analysis
**Location:** Root Directory / `hw` folders  
**Technologies:** Vega-Lite, Python

Interactive visualizations exploring COVID-19 statistics and movie datasets, demonstrating the ability to craft compelling narratives and interactive filters using Vega-Lite and Altair.

## Repository Structure

- `project/`: Contains the final group project, split into exploratory data analysis (Part 1) and the final Streamlit dashboard application (Part 2).
- `hw3/`, `hw5/`, `hw6/`: Homework assignments focusing on different data visualization principles and libraries.
- `week */`, `lab*`: Weekly workbook exercises, lab notebooks, and datasets (e.g., geographical data, building inventories).
- `online_cv_public-main/`: Source code for an online CV/portfolio website template to host visualization projects.

## Setup and Usage

To run the final Streamlit dashboard locally:

1. Navigate to the project dashboard directory:
   ```bash
   cd project/part2
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
