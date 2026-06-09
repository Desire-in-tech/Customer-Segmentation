# Customer Segmentation Dashboard

A data science project that segments U.S. households from the **Survey of Consumer Finances (SCF) 2019** dataset using K-Means clustering, PCA, and an interactive Dash web application.

**🚀 [Live Demo on Render](https://customer-segmentation-lq9d.onrender.com)** *(update URL after deployment)*

## Overview

This project analyzes households that have been **turned down for credit or feared being denied credit** in the past 5 years (`TURNFEAR == 1`). Using unsupervised machine learning, we identify natural groupings of similar households based on financial characteristics including income, net worth, debt, assets, and demographics.

### Key Insights
- Identifies 2-12 distinct household segments (configurable)
- Ranks features by variance to determine which financial metrics matter most
- Uses PCA for interpretable 2D visualization of high-dimensional clusters
- Compares trimmed vs. raw variance for robust feature selection

---

## 📊 Dashboard Preview

### High-Variance Features Analysis
The app identifies and visualizes the top 5 features with the highest variance, with a toggle between trimmed (robust) and raw variance calculations:

![High-Variance Features Bar Chart](assets/01_bar_chart.png)

*Features ranked by variance help identify which financial metrics have the most variation across households.*

### Clustering Metrics
Real-time metrics update as you adjust the number of clusters (K). The silhouette score measures cluster quality, while inertia shows within-cluster compactness:

![Clustering Metrics](assets/02_metrics.png)

*Inertia and Silhouette Score guide optimal cluster selection.*

### Cluster Visualization (PCA)
Interactive 2D scatter plot showing household clusters reduced from 5 dimensions using Principal Component Analysis. Each point represents a household, colored by cluster assignment:

![PCA Scatter Plot](assets/03_pca_scatter.png)

*Hover over points to explore individual households and their cluster assignments.*

---

## Quick Start

### Run Locally

```bash
# Clone the repository
git clone https://github.com/Desire-in-tech/Customer-Segmentation.git
cd Customer-Segmentation

# Install dependencies
pip install -r dash_app/requirements.txt

# Run the Dash app
cd dash_app
python app.py
```

Then open http://localhost:7860 in your browser.

### Use the Live Demo

Visit the [live Render deployment](https://customer-segmentation-lq9d.onrender.com) *(update URL after deployment)* to interact with the dashboard online!

**Note:** The free tier may take 30-60 seconds to load after periods of inactivity. Once loaded, it runs smoothly!

## Project Structure

```
Customer-Segmentation/
├── dash_app/
│   ├── app.py                          # Interactive Dash web application
│   └── requirements.txt                # Python dependencies
├── data/
│   ├── SCF_2019.csv.gz                # Survey of Consumer Finances 2019 dataset
│   └── data_dictionary.md             # Variable descriptions and metadata
├── assets/
│   ├── 01_bar_chart.png               # Dashboard screenshot: variance features
│   ├── 02_metrics.png                 # Dashboard screenshot: clustering metrics
│   └── 03_pca_scatter.png             # Dashboard screenshot: PCA visualization
├── 01_exploring_data.ipynb            # EDA: distributions, correlations, summaries
├── 02_clustering_two_features.ipynb   # K-Means on 2 features with elbow method
├── 03_clustering_multiple_features.ipynb # K-Means + PCA (multi-feature analysis)
├── 04_interactive_dash_app.ipynb      # Notebook version of the Dash app
├── render.yaml                        # Render.com deployment configuration
├── README.md
└── requirements.txt                    # All project dependencies
```

## Dataset

**Survey of Consumer Finances 2019** — Published by the Federal Reserve Board.

- **Source:** https://www.federalreserve.gov/econres/scfindex.htm
- **Size:** ~5MB (compressed)
- **Households included:** Those with `TURNFEAR == 1` and Net Worth < $2,000,000
- **Target variable:** `TURNFEAR` — Was the household turned down for credit or did they fear being denied credit in the past 5 years?

### Key Features Used

| Feature | Description |
|---------|-------------|
| `INCOME` | Total household income (USD) |
| `NETWORTH` | Net worth: assets minus liabilities (USD) |
| `CCBAL` | Credit card balance / debt (USD) |
| `HOUSES` | Value of primary residence (USD) |
| `MRTHEL` | Mortgage debt on primary residence (USD) |
| `DEBT` | Total household debt (USD) |
| `NFIN` | Total non-financial assets (USD) |
| `RETQLIQ` | Retirement account balance (USD) |
| `AGE` | Age of household head |
| `EDUC` | Education level of household head |
| `NHNFIN` | Non-home, non-financial assets (USD) |

See `data/data_dictionary.md` for the full data dictionary.

## Notebooks

### 01 — Exploring Data
- Load and filter households with `TURNFEAR == 1`
- Visualize distributions of income, assets, debt, age, education
- Compute correlation matrix and key statistics
- Identify high-variance features

### 02 — Clustering: Two Features
- K-Means clustering on 2 features (e.g., home value vs. debt)
- Elbow method and silhouette scores to find optimal K
- Scatter plots of clusters and centroids
- Comparison of cluster characteristics

### 03 — Clustering: Multiple Features
- Filter to net worth < $2,000,000
- Compute trimmed variance to identify top 5 high-variance features
- StandardScaler feature normalization
- K-Means pipeline with inertia & silhouette score analysis
- PCA dimensionality reduction → 2D visualization of clusters

### 04 — Interactive Dash App
- Feature selection: trimmed vs. raw variance
- Slider to adjust number of clusters (K=2 to 12)
- Live-updating visualizations:
  - Bar chart of top 5 high-variance features
  - Model metrics (inertia, silhouette score)
  - 2D PCA scatter plot of clusters
- Fully interactive — retrain K-Means on user input

## Dashboard Features

The interactive Dash app (`dash_app/app.py`) includes:

1. **Variance Analysis**
   - Toggle between trimmed (robust) and raw variance
   - View top 5 high-variance features in a bar chart
   - Real-time updates as you switch methods

2. **K-Means Clustering**
   - Adjust number of clusters from 2 to 12 using an intuitive slider
   - Real-time inertia and silhouette score metrics
   - Feature selection display showing which variables are used
   - Instant model retraining on cluster adjustment

3. **PCA Visualization**
   - 2D scatter plot of household clusters
   - Color-coded by cluster assignment
   - Reduced from 5 dimensions to 2 for interpretability
   - Interactive hover tooltips for data exploration

## Machine Learning Concepts

- **K-Means Clustering** — Unsupervised learning to partition households into K distinct groups
- **PCA (Principal Component Analysis)** — Reduce high-dimensional data to 2D for visualization while preserving variance
- **Elbow Method** — Find optimal number of clusters by examining inertia curve
- **Silhouette Score** — Measure cluster quality (range: -1 to 1; higher is better)
- **Trimmed Variance** — Robust variance estimate that removes top/bottom 10% of values to reduce outlier impact
- **StandardScaler** — Normalize features to mean=0, std=1 before clustering

## Deployment

### Live on Render.com

This project is deployed on [Render.com](https://render.com), a modern cloud platform that supports Python web applications.

**Live URL:** https://customer-segmentation-lq9d.onrender.com *(update after deployment)*

### How to Deploy to Render

1. Go to https://render.com and create a free account
2. Click **"New +"** → Select **"Web Service"**
3. Connect your GitHub repository (`Desire-in-tech/Customer-Segmentation`)
4. Fill in the deployment details:
   - **Name:** `customer-segmentation`
   - **Build Command:** `pip install -r dash_app/requirements.txt`
   - **Start Command:** `cd dash_app && python app.py`
   - **Instance Type:** Select the Free tier
5. Click **"Create Web Service"** and wait 3-5 minutes for deployment
6. Your live URL will appear once the deployment is complete

### Deployment Configuration

The `render.yaml` file in this repository defines all deployment settings:
- Python 3.11 environment
- Automatic dependency installation
- Correct startup command for the Dash app
- Oregon region for optimal performance

### Notes on the Free Tier

- **Cold start:** First request after 15 minutes of inactivity takes 30-60 seconds to load (app spins up)
- **Always-on:** Once active, the app responds instantly
- **Cost:** Completely free!
- **Upgrade option:** Paid plans available if you need always-on performance

---

## Local Development Workflow

1. **Local Development** — Iterate on notebooks and app logic
2. **GitHub** — Push code for version control
3. **Google Colab** — Run notebooks with GPU/TPU for faster computation
4. **Render.com** — Auto-deploys from GitHub (changes sync automatically)

## Requirements

```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0
plotly>=5.15.0
dash>=2.12.0
gunicorn>=21.2.0
```

Install with: `pip install -r dash_app/requirements.txt`

## Author & License

**Author:** Desire-in-tech

This project is open source. Feel free to fork, contribute, or use it for your own projects!

---

**Questions or feedback?** Feel free to open an [issue](https://github.com/Desire-in-tech/Customer-Segmentation/issues) or contribute with a pull request!
