# Customer Segmentation Dashboard

A data science project that segments U.S. households from the **Survey of Consumer Finances (SCF) 2019** dataset using K-Means clustering, PCA, and an interactive Dash web application.

## Overview

We focus on households that have been **turned down for credit or feared being denied credit** in the past 5 years (`TURNFEAR == 1`). Using unsupervised machine learning, we group these households into meaningful clusters and explore their financial profiles.

## Project Structure

```
customer-segmentation/
├── data/
│   ├── SCF_2019.csv.gz          # Compressed dataset (download separately)
│   └── data_dictionary.md       # Variable descriptions
├── 01_exploring_data.ipynb      # EDA: income, assets, debt, demographics
├── 02_clustering_two_features.ipynb  # K-Means with 2 features
├── 03_clustering_mutiple_features.ipynb  # K-Means + PCA (multi-feature)
├── 04_interactive_dash_app.ipynb     # Interactive Dash web app
├── requirements.txt
└── README.md
```

## Dataset

**Survey of Consumer Finances 2019** — Published by the Federal Reserve Board.

Download the public dataset:
- URL: https://www.federalreserve.gov/econres/files/scfp2019s.zip
- Extract and save the CSV as `data/SCF_2019.csv.gz`

Key columns used:
| Column | Description |
|--------|-------------|
| `TURNFEAR` | Turned down or feared denial of credit (1 = Yes) |
| `INCOME` | Household income |
| `NETWORTH` | Net worth |
| `CCBAL` | Credit card balance / debt |
| `HOUSES` | Home value |
| `MRTHEL` | Mortgage debt |
| `EDUC` | Education level |
| `AGE` | Age of household head |
| `SAVBND` | Savings bonds |
| `RETQLIQ` | Retirement account balance |
| `NHNFIN` | Non-home, non-financial assets |
| `DEBT` | Total debt |
| `NFIN` | Non-financial assets |

## Notebooks

### 01 — Exploring Data
- Load and filter `TURNFEAR == 1` households
- Visualize distributions of income, assets, debt, age, education
- Compute correlation matrix and key statistics

### 02 — Clustering: Two Features
- K-Means on 2 features (e.g., home value vs. debt)
- Elbow method and silhouette scores to find optimal K
- Scatter plots of clusters and centroids
- Side-by-side bar chart of cluster means

### 03 — Clustering: Multiple Features
- Filter net worth < $2M
- Compute trimmed variance to identify top 5 high-variance features
- Scale features with StandardScaler
- K-Means pipeline, inertia & silhouette curves
- PCA dimensionality reduction → 2D scatter plot of clusters

### 04 — Interactive Dash App
- Feature selection (trimmed vs. not trimmed variance)
- Slider for number of clusters (K)
- Live-updating bar chart, metrics (inertia, silhouette), and PCA scatter plot
- Fully interactive — retrain K-Means on user selections

## Deployment

The Dash app (notebook 04) is designed for deployment on **Hugging Face Spaces**.

### Hugging Face Spaces Setup
1. Create a new Space on huggingface.co (Gradio or Dash type)
2. Upload `app.py` (exported from notebook 04) and `requirements.txt`
3. Include the dataset or a download script in your Space files

## Workflow

1. **Replit** — Project structure and scaffolding ✅
2. **GitHub** — Push to repo for version control
3. **Google Colab** — Run and iterate on notebooks with GPU/TPU
4. **Hugging Face Spaces** — Deploy the interactive Dash application

## Setup

```bash
pip install -r requirements.txt
jupyter notebook
```

## Key Concepts

- **K-Means Clustering** — Unsupervised ML to find natural household groupings
- **PCA (Principal Component Analysis)** — Reduce high-dimensional data for 2D visualization
- **Elbow Method** — Determine optimal number of clusters via inertia
- **Silhouette Score** — Measure cluster quality (range: -1 to 1, higher is better)
- **Trimmed Variance** — Robust variance estimate after removing extreme outliers
