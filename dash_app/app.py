import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import mstats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from dash import Dash, dcc, html, Input, Output
import warnings
import os

warnings.filterwarnings("ignore")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "SCF_2019.csv.gz")

EXCLUDE_COLS = [
    "YY1", "Y1", "WGT", "TURNFEAR", "RACECL4", "RACECL", "HHSEX",
    "MARRIED", "KIDS", "OCCAT1", "OCCAT2", "EDUC", "INCOME_RANK"
]


def trimmed_variance(x, proportiontocut=0.1):
    """Variance after trimming the top/bottom proportiontocut of values."""
    x_trimmed = mstats.trimr(np.array(x), proportiontocut, proportiontocut)
    return np.var(x_trimmed.compressed())


def wrangle(filepath=DATA_PATH):
    """
    Load SCF 2019 data.
    - Implicate 1 only (every 5th row)
    - TURNFEAR == 1 (turned down or feared credit denial)
    - NETWORTH < 2,000,000
    """
    df = pd.read_csv(filepath, compression="gzip", index_col=0)
    df = df.iloc[::5].reset_index(drop=True)
    df = df[df["TURNFEAR"] == 1].copy()
    df = df[df["NETWORTH"] < 2_000_000].copy()
    return df.reset_index(drop=True)


def get_high_var_features(df, trimmed=True, n=5):
    """
    Return the n features with the highest variance.

    Parameters
    ----------
    df : pd.DataFrame
    trimmed : bool
        If True, use trimmed variance (robust against outliers).
        If False, use raw variance.
    n : int
        Number of top features to return.

    Returns
    -------
    list of str
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    feature_cols = [c for c in numeric_cols if c not in EXCLUDE_COLS]

    if trimmed:
        var_dict = {
            col: trimmed_variance(df[col].dropna().values)
            for col in feature_cols
            if df[col].notna().sum() > 50
        }
        var_series = pd.Series(var_dict).sort_values(ascending=False)
    else:
        var_series = df[feature_cols].var().sort_values(ascending=False)

    return var_series.head(n).index.tolist()


def serve_bar_chart(trimmed=True):
    """
    Plotly bar chart of the top 5 high-variance features.

    Parameters
    ----------
    trimmed : bool

    Returns
    -------
    plotly.graph_objects.Figure
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    feature_cols = [c for c in numeric_cols if c not in EXCLUDE_COLS]

    if trimmed:
        var_dict = {
            col: trimmed_variance(df[col].dropna().values)
            for col in feature_cols
            if df[col].notna().sum() > 50
        }
        var_series = pd.Series(var_dict).sort_values(ascending=False).head(5)
        title_suffix = "(Trimmed Variance)"
    else:
        var_series = df[feature_cols].var().sort_values(ascending=False).head(5)
        title_suffix = "(Raw Variance)"

    fig = px.bar(
        x=var_series.values,
        y=var_series.index,
        orientation="h",
        title=f"Top 5 High-Variance Features {title_suffix}",
        labels={"x": "Variance", "y": "Feature"},
        color=var_series.values,
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def get_model_metrics(trimmed=True, k=3):
    """
    Build, train, and evaluate a KMeans pipeline (StandardScaler + KMeans).

    Parameters
    ----------
    trimmed : bool
        Whether to use trimmed variance for feature selection.
    k : int
        Number of clusters.

    Returns
    -------
    dict with keys:
        model     — fitted sklearn Pipeline
        labels    — np.ndarray of cluster labels
        inertia   — float
        silhouette — float
        X         — pd.DataFrame of features
        X_scaled  — np.ndarray of scaled features
    """
    high_var_cols = get_high_var_features(df, trimmed=trimmed)
    X = df[high_var_cols].copy()

    model = make_pipeline(
        StandardScaler(),
        KMeans(n_clusters=k, random_state=42, n_init=10),
    )
    model.fit(X)

    labels = model.named_steps["kmeans"].labels_
    inertia = model.named_steps["kmeans"].inertia_
    X_scaled = model.named_steps["standardscaler"].transform(X)
    sil = silhouette_score(X_scaled, labels)

    return {
        "model": model,
        "labels": labels,
        "inertia": inertia,
        "silhouette": sil,
        "X": X,
        "X_scaled": X_scaled,
    }


def serve_metrics(trimmed=True, k=3):
    """
    Return Dash HTML components showing inertia and silhouette score.

    Returns
    -------
    list of dash html components
    """
    result = get_model_metrics(trimmed=trimmed, k=k)
    return [
        html.H3(
            f"Inertia: {result['inertia']:,.2f}",
            style={"color": "#636EFA", "marginBottom": "6px"},
        ),
        html.H3(
            f"Silhouette Score: {result['silhouette']:.4f}",
            style={"color": "#00CC96", "marginTop": "0"},
        ),
        html.P(
            f"Features used: {', '.join(get_high_var_features(df, trimmed=trimmed))}",
            style={"color": "#555", "fontSize": "13px"},
        ),
    ]


def get_pca_labels(trimmed=True, k=3):
    """
    Subset to top 5 high-variance features, reduce to 2D with PCA,
    and return a DataFrame with columns ['PC1', 'PC2', 'labels'].

    Parameters
    ----------
    trimmed : bool
    k : int

    Returns
    -------
    pd.DataFrame
    """
    result = get_model_metrics(trimmed=trimmed, k=k)
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(result["X_scaled"])
    df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
    df_pca["labels"] = result["labels"].astype(str)
    return df_pca


def serve_scatter_plot(trimmed=True, k=3):
    """
    2D PCA scatter plot with colour-coded cluster labels.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    df_pca = get_pca_labels(trimmed=trimmed, k=k)
    fig = px.scatter(
        df_pca,
        x="PC1",
        y="PC2",
        color="labels",
        title=f"PCA Representation of Clusters (K={k})",
        labels={"PC1": "PC1", "PC2": "PC2", "labels": "Cluster"},
        opacity=0.65,
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )
    fig.update_layout(legend_title_text="Cluster")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Load data once at startup
# ─────────────────────────────────────────────────────────────────────────────
print("Loading SCF 2019 data...")
df = wrangle()
print(f"Loaded {len(df):,} households.")

# ─────────────────────────────────────────────────────────────────────────────
# Dash Application
# ─────────────────────────────────────────────────────────────────────────────
app = Dash(__name__)
server = app.server  # expose Flask server for Hugging Face / gunicorn

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "1200px",
        "margin": "0 auto",
        "padding": "24px",
        "backgroundColor": "#fafafa",
    },
    children=[
        # ── Header ───────────────────────────────────────────────────────────
        html.H1(
            "Survey of Consumer Finances",
            style={"textAlign": "center", "color": "#1a1a2e", "marginBottom": "4px"},
        ),
        html.H2(
            "Customer Segmentation Dashboard",
            style={"textAlign": "center", "color": "#444", "fontWeight": "normal",
                   "marginTop": "0", "marginBottom": "4px"},
        ),
        html.P(
            "Households turned down for credit or fearing denial (TURNFEAR = 1, Net Worth < $2M)",
            style={"textAlign": "center", "color": "#888", "marginBottom": "36px",
                   "fontSize": "14px"},
        ),

        # ── Section 1: Variance Toggle + Bar Chart ───────────────────────────
        html.Div(
            style={"background": "#fff", "borderRadius": "10px",
                   "padding": "24px", "marginBottom": "24px",
                   "boxShadow": "0 2px 8px rgba(0,0,0,0.07)"},
            children=[
                html.H2("High Variance Features",
                        style={"color": "#16213e", "marginTop": "0"}),
                html.P("Select how variance is computed:"),
                dcc.RadioItems(
                    id="trim-button",
                    options=[
                        {"label": "  Trimmed (robust, removes extreme outliers)", "value": True},
                        {"label": "  Not Trimmed (raw variance)", "value": False},
                    ],
                    value=True,
                    inline=True,
                    style={"marginBottom": "16px"},
                ),
                dcc.Graph(id="bar-chart"),
            ],
        ),

        # ── Section 2: K-Means Controls ──────────────────────────────────────
        html.Div(
            style={"background": "#fff", "borderRadius": "10px",
                   "padding": "24px", "marginBottom": "24px",
                   "boxShadow": "0 2px 8px rgba(0,0,0,0.07)"},
            children=[
                html.H2("K-means Clustering", style={"color": "#16213e", "marginTop": "0"}),
                html.H3("Number of Clusters (k)", style={"marginBottom": "8px"}),
                dcc.Slider(
                    id="k-slider",
                    min=2,
                    max=12,
                    step=1,
                    value=3,
                    marks={i: str(i) for i in range(2, 13)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                html.Br(),

                # Metrics output
                html.Div(
                    id="metrics",
                    style={
                        "background": "#f0f4ff",
                        "borderRadius": "8px",
                        "padding": "16px 20px",
                        "marginTop": "16px",
                    },
                ),
            ],
        ),

        # ── Section 3: PCA Scatter ────────────────────────────────────────────
        html.Div(
            style={"background": "#fff", "borderRadius": "10px",
                   "padding": "24px", "marginBottom": "24px",
                   "boxShadow": "0 2px 8px rgba(0,0,0,0.07)"},
            children=[
                html.H2("PCA Cluster Visualization",
                        style={"color": "#16213e", "marginTop": "0"}),
                html.P(
                    "Principal Component Analysis reduces the 5 selected features to 2 dimensions "
                    "for visualization. Each point is a household, colored by its cluster.",
                    style={"color": "#555", "fontSize": "14px"},
                ),
                dcc.Graph(id="pca-scatter"),
            ],
        ),

        # ── Footer ────────────────────────────────────────────────────────────
        html.P(
            "Data: Federal Reserve Board — Survey of Consumer Finances 2019. "
            "Method: K-Means + StandardScaler pipeline, PCA for 2D visualization.",
            style={"color": "#aaa", "fontSize": "12px", "textAlign": "center"},
        ),
    ],
)


# ─────────────────────────────────────────────────────────────────────────────
# Callbacks
# ─────────────────────────────────────────────────────────────────────────────

@app.callback(
    Output("bar-chart", "figure"),
    Input("trim-button", "value"),
)
def update_bar_chart(trimmed):
    return serve_bar_chart(trimmed=trimmed)


@app.callback(
    Output("metrics", "children"),
    Input("trim-button", "value"),
    Input("k-slider", "value"),
)
def update_metrics(trimmed, k):
    return serve_metrics(trimmed=trimmed, k=k)


@app.callback(
    Output("pca-scatter", "figure"),
    Input("trim-button", "value"),
    Input("k-slider", "value"),
)
def update_scatter_plot(trimmed, k):
    return serve_scatter_plot(trimmed=trimmed, k=k)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(debug=False, host="0.0.0.0", port=port)
