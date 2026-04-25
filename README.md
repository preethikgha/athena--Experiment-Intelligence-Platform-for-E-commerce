# Athena — Experiment Intelligence Platform

End-to-end ML experiment platform that runs statistically rigorous A/B tests on 1.4M real users to decide which recommendation model ships to production.


![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

---

## Overview

Most ML teams ship models based on offline metrics like AUC and RMSE without validating real user impact. Athena solves this by running statistically rigorous online controlled experiments that measure what actually matters: clicks, carts, and purchases.

This project evaluates two competing recommendation strategies on 1.4 million historical user interactions from the Retailrocket e-commerce platform.

---

## Experiment Design

**Dataset:** Retailrocket Recommender System — Kaggle  
**Events:** 2,756,101 across 1,407,580 unique users  
**Event types:** view, addtocart, transaction  
**Period:** October – November 2015  

**Hypothesis:** An engagement-weighted recommendation model incorporating views and cart signals will outperform a purchase-only popularity baseline on downstream conversion metrics.

| | Model A — Control | Model B — Treatment |
|---|---|---|
| Strategy | Purchase popularity baseline | Engagement-weighted scoring |
| Signal | Transactions only | Views x1 + Cart x3 + Purchase x5 |
| Users | 703,998 | 703,582 |

---

## Statistical Framework

- Deterministic MD5 hash assignment — same user always gets same variant, no mid-experiment flipping
- Two-sample Welch t-test per metric
- Bonferroni correction across 3 simultaneous metrics — adjusted alpha = 0.0167
- Sample Ratio Mismatch detection via chi-squared test on observed vs expected split
- Cohen's d effect size reported alongside p-values

---

## Results

| Metric | Model A | Model B | Lift | p-value | Significant |
|--------|---------|---------|------|---------|-------------|
| Click-through Rate | 99.76% | 99.75% | -0.01% | 0.3906 | No |
| Add-to-Cart Rate | 2.67% | 2.69% | +1.01% | 0.3235 | No |
| Purchase CVR | 0.83% | 0.84% | +1.04% | 0.5749 | No |

SRM check passed — p = 0.8051, split integrity confirmed.

Model B shows consistent directional lift across cart and purchase metrics but does not reach statistical significance at alpha = 0.05 with Bonferroni correction. Decision: do not ship. Extend experiment duration or recompute required sample size via power analysis.

---


## Key Concepts

**Bonferroni Correction** — When testing multiple metrics simultaneously, the probability of a false positive increases. Bonferroni correction divides alpha by the number of tests, making the threshold stricter.

**Sample Ratio Mismatch** — If your 50/50 split is actually 48/52 due to logging bugs or bot traffic, your results are invalid. Athena detects this automatically via chi-squared test on the observed vs expected user split.

**Deterministic Assignment** — MD5 hashing ensures the same user always lands in the same variant across sessions, preventing contamination.

**Effect Size** — p-values alone do not tell you if a result is practically meaningful. Cohen's d measures the magnitude of the difference independent of sample size.

---

Built by Preethikgha M

