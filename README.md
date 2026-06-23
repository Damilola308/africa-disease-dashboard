# Africa CDC Disease Surveillance Dashboard

**Author:** Opeyemi Ogunbona  
**Project Type:** Personal Portfolio Project  
**Tools:** Python · Plotly Dash · Pandas · NumPy

---

## Overview

An interactive web dashboard that visualises disease burden across 12 African Union member states for three key diseases — **Malaria**, **Cholera**, and **Mpox** — covering the period **2018–2023**.

The dashboard is fully self-contained: all data is programmatically simulated inside `app.py` using realistic baselines calibrated to Africa CDC and WHO epidemiological reports, with no external API calls or file downloads required.

---

## Dashboard Features

| Feature | Description |
|---|---|
| 🎛️ Disease Filter | Switch between Malaria, Cholera, and Mpox |
| 🌍 Country Filter | Drill down into a single country or view all 12 |
| 📅 Year Range Slider | Select any sub-range from 2018–2023 |
| 📊 KPI Cards | Total cases, deaths, CFR, countries covered |
| 📉 Bar Chart | Total cases ranked by country |
| 📈 Line Trend | Annual case trends for top 5 countries (or selected country) |
| 🗺️ Choropleth Map | Africa map shaded by case rate per 100,000 population |
| 🟡 CFR Bar Chart | Case fatality rate comparison across countries |
| 📋 Summary Table | Sortable data table with all metrics |

---

## Countries Included

Nigeria · Ethiopia · South Africa · DR Congo · Kenya · Ghana · Tanzania · Uganda · Mozambique · Cameroon · Senegal · Zimbabwe

---

## Data Note

This dashboard uses **simulated data** that mirrors the structure and scale of real Africa CDC epidemiological reports. Baseline case rates, year-over-year trends, and the 2022 Mpox surge are modelled to reflect documented patterns in public health literature. This approach ensures the dashboard is fully reproducible without relying on live APIs or licensed datasets.

---

## How to Run Locally

### 1. Prerequisites
- Python 3.9 or later installed
- A terminal / Command Prompt / PowerShell

### 2. Install dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 3. Launch the dashboard

```bash
python app.py
```

### 4. Open in your browser

Once you see the message:

```
✅  Africa CDC Disease Surveillance Dashboard
    Open your browser at:  http://127.0.0.1:8050
```

Navigate to **http://127.0.0.1:8050** in any browser.

Press `Ctrl + C` in the terminal to stop the server.

---

## Project Structure

```
africa-disease-dashboard/
│
├── app.py              # Main Dash application (self-contained)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Pushing to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Africa CDC Disease Surveillance Dashboard"
git branch -M main
git remote add origin https://github.com/opeyemi-ogunbona/africa-disease-dashboard.git
git push -u origin main
```

> Recommended repo name: `africa-disease-dashboard`

---

## Skills & Libraries Demonstrated

- **Plotly Dash** — multi-callback interactive web app
- **Plotly Express / Graph Objects** — choropleth maps, bar charts, line charts
- **Pandas** — data aggregation and transformation
- **NumPy** — statistical simulation (Geometric Brownian-style noise)
- **Dash DataTable** — sortable, styled summary table
- **Data storytelling** — KPI cards, colour-coded alerts, drill-down filters

---

*This project is part of a data analyst portfolio built by Opeyemi Ogunbona.*
