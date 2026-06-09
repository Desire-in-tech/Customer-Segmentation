# Customer Segmentation Dashboard

A data science project that segments U.S. households from the **Survey of Consumer Finances (SCF) 2019** dataset using K-Means clustering, PCA, and an interactive Dash web application.

**🚀 [Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Desire-in-tech/Customer-Segmentation)** *(update URL after deployment)*

## Overview

This project analyzes households that have been **turned down for credit or feared being denied credit** in the past 5 years (`TURNFEAR == 1`). Using unsupervised machine learning, we identify natural groupings of similar households based on financial characteristics including income, net worth, debt, assets, and demographics.

### Key Insights
- Identifies 2-12 distinct household segments (configurable)
- Ranks features by variance to determine which financial metrics matter most
- Uses PCA for interpretable 2D visualization of high-dimensional clusters
- Compares trimmed vs. raw variance for robust feature selection

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

Visit the [Hugging Face Spaces deployment](https://huggingface.co/spaces/Desire-in-tech/Customer-Segmentation) *(update URL after deployment)* to interact with the dashboard online — no installation required!

## Project Structure

```
Customer-Segmentation/
├── dash_app/
│   ├── app.py                          # Interactive Dash web application
│   └── requirements.txt                # Python dependencies
├── data/
│   ├── SCF_2019.csv.gz                # Survey of Consumer Finances 2019 dataset
│   └── data_dictionary.md             # Variable descriptions and metadata
├── 01_exploring_data.ipynb            # EDA: distributions, correlations, summaries
├── 02_clustering_two_features.ipynb   # K-Means on 2 features with elbow method
├── 03_clustering_multiple_features.ipynb # K-Means + PCA (multi-feature analysis)
├── 04_interactive_dash_app.ipynb      # Notebook version of the Dash app
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

2. **K-Means Clustering**
   - Adjust number of clusters from 2 to 12
   - Real-time inertia and silhouette score metrics
   - Feature selection display

3. **PCA Visualization**
   - 2D scatter plot of household clusters
   - Color-coded by cluster assignment
   - Reduced from 5 dimensions to 2 for interpretability

## Machine Learning Concepts

- **K-Means Clustering** — Unsupervised learning to partition households into K distinct groups
- **PCA (Principal Component Analysis)** — Reduce high-dimensional data to 2D for visualization while preserving variance
- **Elbow Method** — Find optimal number of clusters by examining inertia curve
- **Silhouette Score** — Measure cluster quality (range: -1 to 1; higher is better)
- **Trimmed Variance** — Robust variance estimate that removes top/bottom 10% of values to reduce outlier impact
- **StandardScaler** — Normalize features to mean=0, std=1 before clustering

## Deployment to Hugging Face Spaces

This project is optimized for deployment on [Hugging Face Spaces](https://huggingface.co/spaces).

### Deploy in 5 Steps:

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"** → Select **Dash** as the Space type
3. Connect your GitHub repo (`Desire-in-tech/Customer-Segmentation`)
4. Set app file to `dash_app/app.py`
5. Click **"Create Space"** — Hugging Face will auto-deploy within minutes

### What Happens Automatically:
- ✅ Install all dependencies from `dash_app/requirements.txt`
- ✅ Clone your repository (including `data/SCF_2019.csv.gz`)
- ✅ Run the Dash app on port 7860
- ✅ Provide a public URL for sharing

**Your live Space:** https://huggingface.co/spaces/Desire-in-tech/Customer-Segmentation *(update this URL after deployment)*

## Development Workflow

1. **Local Development** — Iterate on notebooks and app logic
2. **GitHub** — Push code for version control
3. **Google Colab** — Run notebooks with GPU/TPU for faster computation
4. **Hugging Face Spaces** — Deploy interactive web app for live demonstration

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
