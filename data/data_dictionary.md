# SCF 2019 Data Dictionary

Selected variables from the **Survey of Consumer Finances 2019** used in this project.

## Target Variable

| Variable | Description | Values |
|----------|-------------|--------|
| `TURNFEAR` | Was the household turned down for credit or did they fear being denied credit in the past 5 years? | 1 = Yes, 0 = No |

## Demographic Variables

| Variable | Description | Notes |
|----------|-------------|-------|
| `AGE` | Age of household head | Continuous |
| `EDUC` | Education of household head | 1=No high school, 2=High school diploma, 3=Some college, 4=College degree, 5=Graduate degree |
| `MARRIED` | Marital status | 1=Married/partnered, 2=Single |
| `KIDS` | Number of children | Count |
| `OCCAT1` | Occupation category | Categorical |
| `RACE` | Race/ethnicity of household head | 1=White, 2=Black, 3=Hispanic, 4=Asian, 5=Other |

## Income & Wealth Variables

| Variable | Description | Notes |
|----------|-------------|-------|
| `INCOME` | Total household income | USD, annual |
| `NETWORTH` | Net worth (assets minus liabilities) | USD |
| `ASSET` | Total assets | USD |
| `DEBT` | Total debt | USD |

## Asset Variables

| Variable | Description | Notes |
|----------|-------------|-------|
| `HOUSES` | Value of primary residence | USD |
| `ORESRE` | Value of other real estate | USD |
| `NFIN` | Total non-financial assets | USD |
| `NHNFIN` | Non-home, non-financial assets | USD |
| `FIN` | Total financial assets | USD |
| `SAVBND` | Savings bonds value | USD |
| `CHECKING` | Checking account balance | USD |
| `SAVING` | Savings account balance | USD |
| `RETQLIQ` | Retirement account balance (liquid) | USD |
| `STOCKS` | Stock holdings | USD |
| `BOND` | Bond holdings | USD |
| `CASHLI` | Cash value of life insurance | USD |

## Debt Variables

| Variable | Description | Notes |
|----------|-------------|-------|
| `MRTHEL` | Mortgage debt on primary residence | USD |
| `RESDBT` | Debt on other real estate | USD |
| `CCBAL` | Credit card balance | USD |
| `INSTALL` | Installment loans | USD |
| `ODEBT` | Other debt | USD |

## Computed / Derived Variables

| Variable | Description | Formula |
|----------|-------------|---------|
| Debt-to-income ratio | Debt relative to income | `DEBT / INCOME` |
| Loan-to-value ratio | Mortgage relative to home value | `MRTHEL / HOUSES` |

## Notes on the Dataset

- The SCF uses a **multiple imputation** methodology — each household has 5 implicates (copies) with slightly different values to account for survey non-response. For simplicity in this project, we use **implicate 1** only (every 5th row).
- All dollar values are in **nominal 2019 USD**.
- The dataset is publicly available from the Federal Reserve Board: https://www.federalreserve.gov/econres/scfindex.htm
- Codebook / full data dictionary: https://www.federalreserve.gov/econres/files/codebk2019.txt
