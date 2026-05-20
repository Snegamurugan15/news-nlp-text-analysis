import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_PATH = "data/news_metrics_sample.csv"


df = pd.read_csv(DATA_PATH)
app = Dash(__name__)
app.title = "News NLP Text Analysis"

metric_style = {
    "border": "1px solid #dde3ea",
    "borderRadius": "8px",
    "padding": "16px",
    "background": "#fbfcfd",
}

app.layout = html.Div(
    style={"fontFamily": "Segoe UI, sans-serif", "margin": "32px", "maxWidth": "1180px"},
    children=[
        html.H1("News NLP Text Analysis"),
        html.P(
            "Dash application for article sentiment, readability, and editorial review prioritization.",
            style={"color": "#566"},
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "12px"},
            children=[
                html.Div([html.H3(len(df)), html.P("Articles")], style=metric_style),
                html.Div([html.H3(f"{df['polarity'].mean():.2f}"), html.P("Avg polarity")], style=metric_style),
                html.Div([html.H3(f"{df['fog_index'].mean():.1f}"), html.P("Avg fog index")], style=metric_style),
                html.Div([html.H3(f"{int(df['word_count'].sum()):,}"), html.P("Words analyzed")], style=metric_style),
            ],
        ),
        html.Br(),
        html.Label("Readability threshold"),
        dcc.Slider(8, 20, 1, value=14, id="fog-threshold"),
        dcc.Graph(id="sentiment-chart"),
        dcc.Graph(id="readability-chart"),
        html.H3("Editorial Review Queue"),
        html.Div(id="review-table"),
    ],
)


@app.callback(
    Output("sentiment-chart", "figure"),
    Output("readability-chart", "figure"),
    Output("review-table", "children"),
    Input("fog-threshold", "value"),
)
def update_dashboard(threshold):
    flagged = df[df["fog_index"] >= threshold].sort_values("fog_index", ascending=False)
    sentiment = px.scatter(
        df,
        x="subjectivity",
        y="polarity",
        size="word_count",
        color="fog_index",
        hover_name="title",
        color_continuous_scale="Viridis",
        title="Sentiment vs. Subjectivity",
    )
    readability = px.histogram(df, x="fog_index", nbins=18, title="Readability Distribution")
    rows = [
        html.Tr([html.Th(col) for col in ["url_id", "title", "polarity", "fog_index", "word_count"]])
    ] + [
        html.Tr([html.Td(row[col]) for col in ["url_id", "title", "polarity", "fog_index", "word_count"]])
        for _, row in flagged.head(12).iterrows()
    ]
    table = html.Table(rows, style={"width": "100%", "borderCollapse": "collapse"})
    return sentiment, readability, table


if __name__ == "__main__":
    app.run(debug=True)
