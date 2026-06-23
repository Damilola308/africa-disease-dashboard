# ============================================================
# Africa CDC Disease Surveillance Dashboard
# Author: Opeyemi Ogunbona
# Description: Interactive Plotly Dash dashboard visualising
#              disease burden (Malaria, Cholera, Mpox) across
#              African Union member states (2018–2023).
#              Data is programmatically simulated to mirror
#              realistic Africa CDC epidemiological patterns.
# ============================================================

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# 1.  SIMULATED DATA
# ─────────────────────────────────────────────

np.random.seed(42)

COUNTRIES = {
    "Nigeria":         {"iso": "NGA", "region": "West Africa",    "population": 218_000_000},
    "Ethiopia":        {"iso": "ETH", "region": "East Africa",    "population": 126_000_000},
    "South Africa":    {"iso": "ZAF", "region": "Southern Africa","population":  60_000_000},
    "DR Congo":        {"iso": "COD", "region": "Central Africa", "population":  99_000_000},
    "Kenya":           {"iso": "KEN", "region": "East Africa",    "population":  55_000_000},
    "Ghana":           {"iso": "GHA", "region": "West Africa",    "population":  33_000_000},
    "Tanzania":        {"iso": "TZA", "region": "East Africa",    "population":  63_000_000},
    "Uganda":          {"iso": "UGA", "region": "East Africa",    "population":  48_000_000},
    "Mozambique":      {"iso": "MOZ", "region": "Southern Africa","population":  32_000_000},
    "Cameroon":        {"iso": "CMR", "region": "Central Africa", "population":  27_000_000},
    "Senegal":         {"iso": "SEN", "region": "West Africa",    "population":  17_000_000},
    "Zimbabwe":        {"iso": "ZWE", "region": "Southern Africa","population":  15_000_000},
}

DISEASES = ["Malaria", "Cholera", "Mpox"]
YEARS    = list(range(2018, 2024))

# --- Baseline cases per 100,000 population ---
BASELINES = {
    "Malaria": {
        "Nigeria": 9_200, "Ethiopia": 4_100, "South Africa": 120,
        "DR Congo": 12_500, "Kenya": 3_800, "Ghana": 6_700,
        "Tanzania": 5_900, "Uganda": 7_200, "Mozambique": 8_400,
        "Cameroon": 6_100, "Senegal": 3_200, "Zimbabwe": 2_100,
    },
    "Cholera": {
        "Nigeria": 85, "Ethiopia": 310, "South Africa": 12,
        "DR Congo": 420, "Kenya": 95, "Ghana": 55,
        "Tanzania": 180, "Uganda": 210, "Mozambique": 290,
        "Cameroon": 130, "Senegal": 60, "Zimbabwe": 75,
    },
    "Mpox": {
        "Nigeria": 4, "Ethiopia": 1, "South Africa": 8,
        "DR Congo": 95, "Kenya": 2, "Ghana": 3,
        "Tanzania": 1, "Uganda": 6, "Mozambique": 1,
        "Cameroon": 7, "Senegal": 2, "Zimbabwe": 3,
    },
}

# Year multipliers – subtle trends (Malaria declining slowly, Mpox spike 2022)
YEAR_MULT = {
    "Malaria": {2018:1.00, 2019:0.97, 2020:1.04, 2021:0.96, 2022:0.93, 2023:0.90},
    "Cholera": {2018:1.00, 2019:0.92, 2020:1.15, 2021:0.88, 2022:0.95, 2023:0.80},
    "Mpox":    {2018:1.00, 2019:1.20, 2020:1.40, 2021:1.80, 2022:5.50, 2023:3.20},
}

CASE_FATALITY = {"Malaria": 0.0025, "Cholera": 0.012, "Mpox": 0.032}

rows = []
for country, meta in COUNTRIES.items():
    pop = meta["population"]
    for disease in DISEASES:
        base = BASELINES[disease][country]
        for year in YEARS:
            mult   = YEAR_MULT[disease][year]
            noise  = np.random.uniform(0.88, 1.12)
            rate   = base * mult * noise          # per 100k
            cases  = int(rate * pop / 100_000)
            deaths = int(cases * CASE_FATALITY[disease] * np.random.uniform(0.85, 1.15))
            rows.append({
                "Country":     country,
                "ISO":         meta["iso"],
                "Region":      meta["region"],
                "Population":  pop,
                "Disease":     disease,
                "Year":        year,
                "Cases":       cases,
                "Deaths":      deaths,
                "CFR":         round(deaths / cases * 100, 2) if cases else 0,
                "Rate_per_100k": round(rate, 1),
            })

df = pd.DataFrame(rows)

# ─────────────────────────────────────────────
# 2.  APP LAYOUT
# ─────────────────────────────────────────────

# Colour palette – Africa CDC greens / dark navy
ACCENT     = "#00843D"   # Africa CDC green
ACCENT2    = "#F5A800"   # amber
DARK       = "#0D1B2A"
SURFACE    = "#1A2A3A"
CARD_BG    = "#162233"
TEXT_MAIN  = "#E8EFF6"
TEXT_MUTED = "#8BA4BE"
GRID_CLR   = "#1F3048"

CARD_STYLE = {
    "background": CARD_BG,
    "border": f"1px solid {GRID_CLR}",
    "borderRadius": "10px",
    "padding": "20px",
    "marginBottom": "16px",
}

app = dash.Dash(
    __name__,
    title="Africa CDC Disease Surveillance Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

app.layout = html.Div(
    style={"background": DARK, "minHeight": "100vh", "fontFamily": "'Segoe UI', Arial, sans-serif", "color": TEXT_MAIN},
    children=[

        # ── HEADER ──────────────────────────────────────
        html.Div(
            style={
                "background": f"linear-gradient(135deg, {SURFACE} 0%, #0A1520 100%)",
                "borderBottom": f"3px solid {ACCENT}",
                "padding": "24px 40px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
            },
            children=[
                html.Div([
                    html.Div(
                        "🌍  Africa CDC",
                        style={"color": ACCENT, "fontWeight": "700", "fontSize": "13px",
                               "letterSpacing": "2px", "textTransform": "uppercase", "marginBottom": "4px"},
                    ),
                    html.H1(
                        "Disease Surveillance Dashboard",
                        style={"margin": "0", "fontSize": "26px", "fontWeight": "700", "color": TEXT_MAIN},
                    ),
                    html.P(
                        "Malaria · Cholera · Mpox  |  12 Member States  |  2018 – 2023",
                        style={"margin": "4px 0 0", "color": TEXT_MUTED, "fontSize": "13px"},
                    ),
                ]),
                html.Div(
                    "Opeyemi Ogunbona",
                    style={"color": TEXT_MUTED, "fontSize": "12px", "textAlign": "right"},
                ),
            ],
        ),

        # ── FILTERS ──────────────────────────────────────
        html.Div(
            style={"padding": "20px 40px 0", "display": "flex", "gap": "20px", "flexWrap": "wrap"},
            children=[
                html.Div([
                    html.Label("Disease", style={"color": TEXT_MUTED, "fontSize": "12px", "marginBottom": "6px", "display":"block"}),
                    dcc.Dropdown(
                        id="disease-filter",
                        options=[{"label": d, "value": d} for d in DISEASES],
                        value="Malaria",
                        clearable=False,
                        style={"width": "200px", "background": SURFACE, "color": DARK, "border": f"1px solid {GRID_CLR}"},
                    ),
                ]),
                html.Div([
                    html.Label("Country", style={"color": TEXT_MUTED, "fontSize": "12px", "marginBottom": "6px", "display":"block"}),
                    dcc.Dropdown(
                        id="country-filter",
                        options=[{"label": "All Countries", "value": "All"}] +
                                [{"label": c, "value": c} for c in sorted(COUNTRIES.keys())],
                        value="All",
                        clearable=False,
                        style={"width": "220px", "background": SURFACE, "color": DARK, "border": f"1px solid {GRID_CLR}"},
                    ),
                ]),
                html.Div([
                    html.Label("Year Range", style={"color": TEXT_MUTED, "fontSize": "12px", "marginBottom": "6px", "display":"block"}),
                    dcc.RangeSlider(
                        id="year-slider",
                        min=2018, max=2023, step=1,
                        marks={y: {"label": str(y), "style": {"color": TEXT_MUTED, "fontSize": "11px"}} for y in YEARS},
                        value=[2018, 2023],
                        tooltip={"always_visible": False},
                    ),
                ], style={"width": "320px", "paddingTop": "4px"}),
            ],
        ),

        # ── KPI CARDS ──────────────────────────────────────
        html.Div(
            id="kpi-cards",
            style={"padding": "20px 40px", "display": "flex", "gap": "16px", "flexWrap": "wrap"},
        ),

        # ── ROW 1: Bar Chart + Line Trend ──────────────────
        html.Div(
            style={"padding": "0 40px", "display": "grid",
                   "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
            children=[
                html.Div([
                    html.H3("Cases by Country", style={"margin":"0 0 12px","fontSize":"15px","color":TEXT_MUTED}),
                    dcc.Graph(id="bar-chart", config={"displayModeBar": False}),
                ], style=CARD_STYLE),
                html.Div([
                    html.H3("Annual Trend", style={"margin":"0 0 12px","fontSize":"15px","color":TEXT_MUTED}),
                    dcc.Graph(id="line-chart", config={"displayModeBar": False}),
                ], style=CARD_STYLE),
            ],
        ),

        # ── ROW 2: Choropleth + CFR Bubble ─────────────────
        html.Div(
            style={"padding": "16px 40px 0", "display": "grid",
                   "gridTemplateColumns": "1.4fr 1fr", "gap": "16px"},
            children=[
                html.Div([
                    html.H3("Case Rate per 100,000 Population", style={"margin":"0 0 12px","fontSize":"15px","color":TEXT_MUTED}),
                    dcc.Graph(id="choropleth", config={"displayModeBar": False}),
                ], style=CARD_STYLE),
                html.Div([
                    html.H3("Case Fatality Rate (%)", style={"margin":"0 0 12px","fontSize":"15px","color":TEXT_MUTED}),
                    dcc.Graph(id="cfr-chart", config={"displayModeBar": False}),
                ], style=CARD_STYLE),
            ],
        ),

        # ── ROW 3: Data Table ──────────────────────────────
        html.Div(
            style={"padding": "16px 40px 40px"},
            children=[
                html.Div([
                    html.H3("Summary Data Table", style={"margin":"0 0 12px","fontSize":"15px","color":TEXT_MUTED}),
                    html.Div(id="data-table-container"),
                ], style=CARD_STYLE),
            ],
        ),
    ],
)

# ─────────────────────────────────────────────
# 3.  CALLBACKS
# ─────────────────────────────────────────────

def filter_data(disease, country, year_range):
    mask = (
        (df["Disease"] == disease) &
        (df["Year"] >= year_range[0]) &
        (df["Year"] <= year_range[1])
    )
    if country != "All":
        mask &= (df["Country"] == country)
    return df[mask]


PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_MAIN, family="Segoe UI, Arial"),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickcolor=TEXT_MUTED),
    yaxis=dict(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickcolor=TEXT_MUTED),
)


@app.callback(
    Output("kpi-cards", "children"),
    Output("bar-chart", "figure"),
    Output("line-chart", "figure"),
    Output("choropleth", "figure"),
    Output("cfr-chart", "figure"),
    Output("data-table-container", "children"),
    Input("disease-filter", "value"),
    Input("country-filter", "value"),
    Input("year-slider", "value"),
)
def update_all(disease, country, year_range):
    filtered = filter_data(disease, country, year_range)
    agg_country = filtered.groupby("Country").agg(
        Cases=("Cases","sum"), Deaths=("Deaths","sum"),
        Rate_per_100k=("Rate_per_100k","mean"), ISO=("ISO","first"),
        CFR=("CFR","mean"),
    ).reset_index().sort_values("Cases", ascending=False)

    agg_year = filtered.groupby(["Year","Country"]).agg(Cases=("Cases","sum")).reset_index()

    total_cases  = filtered["Cases"].sum()
    total_deaths = filtered["Deaths"].sum()
    avg_cfr      = round(filtered["CFR"].mean(), 2)
    countries_n  = filtered["Country"].nunique()
    years_label  = f"{year_range[0]}–{year_range[1]}"

    # ── KPI cards ──────────────────────────────
    def kpi(label, value, colour=ACCENT):
        return html.Div([
            html.Div(f"{value:,}", style={"fontSize":"28px","fontWeight":"700","color":colour}),
            html.Div(label, style={"fontSize":"12px","color":TEXT_MUTED,"marginTop":"4px"}),
        ], style={**CARD_STYLE, "flex":"1","minWidth":"150px","textAlign":"center","marginBottom":"0"})

    kpis = [
        kpi("Total Cases", total_cases),
        kpi("Total Deaths", total_deaths, ACCENT2),
        kpi(f"Avg CFR %", avg_cfr, "#E05C5C"),
        kpi("Countries Covered", countries_n),
        kpi("Period", years_label, TEXT_MUTED),
    ]

    # ── Bar chart ──────────────────────────────
    bar_fig = go.Figure(go.Bar(
        x=agg_country["Country"],
        y=agg_country["Cases"],
        marker_color=ACCENT,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Cases: %{y:,}<extra></extra>",
    ))
    bar_fig.update_layout(**PLOT_LAYOUT, height=300, showlegend=False)
    bar_fig.update_xaxes(tickangle=-30, tickfont=dict(size=11))

    # ── Line trend ─────────────────────────────
    countries_for_line = (
        [country] if country != "All"
        else agg_country.head(5)["Country"].tolist()
    )
    colors_palette = [ACCENT, ACCENT2, "#4EA8DE", "#E05C5C", "#A78BFA"]
    line_fig = go.Figure()
    for i, c in enumerate(countries_for_line):
        sub = agg_year[agg_year["Country"] == c].sort_values("Year")
        line_fig.add_trace(go.Scatter(
            x=sub["Year"], y=sub["Cases"],
            mode="lines+markers",
            name=c,
            line=dict(color=colors_palette[i % len(colors_palette)], width=2),
            marker=dict(size=6),
            hovertemplate=f"<b>{c}</b> %{{x}}<br>Cases: %{{y:,}}<extra></extra>",
        ))
    line_fig.update_layout(**PLOT_LAYOUT, height=300, legend=dict(
        font=dict(size=11, color=TEXT_MUTED), bgcolor="rgba(0,0,0,0)"))

    # ── Choropleth ─────────────────────────────
    # aggregate full df for the selected disease/years, all countries (for map)
    map_data = df[
        (df["Disease"] == disease) &
        (df["Year"] >= year_range[0]) &
        (df["Year"] <= year_range[1])
    ].groupby(["Country","ISO"]).agg(Rate_per_100k=("Rate_per_100k","mean")).reset_index()

    choro_fig = px.choropleth(
        map_data,
        locations="ISO",
        color="Rate_per_100k",
        hover_name="Country",
        color_continuous_scale=[[0,"#0D1B2A"],[0.3,"#00592A"],[0.7,ACCENT],[1.0,ACCENT2]],
        labels={"Rate_per_100k": "Rate/100k"},
        scope="africa",
    )
    choro_fig.update_geos(
        bgcolor=DARK,
        landcolor=SURFACE,
        showcoastlines=True, coastlinecolor=GRID_CLR,
        showframe=False,
    )
    choro_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        geo_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_MAIN),
        margin=dict(l=0, r=0, t=0, b=0),
        height=340,
        coloraxis_colorbar=dict(
            tickfont=dict(color=TEXT_MUTED, size=10),
            title=dict(text="Rate/100k", font=dict(color=TEXT_MUTED, size=11)),
            bgcolor=SURFACE,
            bordercolor=GRID_CLR,
        ),
    )

    # ── CFR bar ────────────────────────────────
    cfr_sorted = agg_country.sort_values("CFR", ascending=True)
    cfr_fig = go.Figure(go.Bar(
        x=cfr_sorted["CFR"],
        y=cfr_sorted["Country"],
        orientation="h",
        marker_color=ACCENT2,
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>CFR: %{x:.2f}%<extra></extra>",
    ))
    cfr_fig.update_layout(**PLOT_LAYOUT, height=300, showlegend=False)

    # ── Data Table ─────────────────────────────
    table_df = agg_country[["Country","Cases","Deaths","CFR","Rate_per_100k"]].copy()
    table_df.columns = ["Country","Total Cases","Total Deaths","Avg CFR (%)","Avg Rate/100k"]
    table_df["Total Cases"]   = table_df["Total Cases"].map("{:,}".format)
    table_df["Total Deaths"]  = table_df["Total Deaths"].map("{:,}".format)

    table = dash_table.DataTable(
        data=table_df.to_dict("records"),
        columns=[{"name": c, "id": c} for c in table_df.columns],
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": SURFACE,
            "color": ACCENT,
            "fontWeight": "600",
            "fontSize": "13px",
            "border": f"1px solid {GRID_CLR}",
        },
        style_cell={
            "backgroundColor": CARD_BG,
            "color": TEXT_MAIN,
            "fontSize": "13px",
            "border": f"1px solid {GRID_CLR}",
            "padding": "10px 14px",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": SURFACE},
        ],
        page_size=12,
        sort_action="native",
    )

    return kpis, bar_fig, line_fig, choro_fig, cfr_fig, table


# ─────────────────────────────────────────────
# 4.  RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n✅  Africa CDC Disease Surveillance Dashboard")
    print("    Author: Opeyemi Ogunbona")
    print("    Open your browser at:  http://127.0.0.1:8050\n")
    app.run(debug=True)
