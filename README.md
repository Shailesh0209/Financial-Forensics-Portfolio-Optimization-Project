# Financial Portfolio Optimization Project


## 🎯 Project Objective

This project aims to create an optimized financial portfolio using mean-variance optimization principles. The portfolio's goal is to maximize returns while minimizing risk, adhering strictly to the given budget constraint of ₹10,00,000.

---

## 📂 Data Sources

- **T1_data/Annual_P_L_1.csv**: Historical annual profit/loss data (Time period T1)
- **T1_data/price.csv**: Stock prices at period T1 (buying prices)
- **T2_data/price.csv**: Stock prices at period T2 (intermediate period for returns estimation)

---

## 🚀 **Project Methodology**

### **Step 1: Data Loading & Preprocessing**

- Loaded datasets using pandas.
- Aligned stocks by merging T1 and T2 data based on stock names.
- Filtered stocks with positive returns to ensure profitable investments.

---

## 📈 Mean-Variance Portfolio Optimization

- **Objective**: Maximize returns and minimize risk (variance).
- **Constraints applied**:

| Constraint              | Value                     | Purpose                           |
|-------------------------|---------------------------|-----------------------------------|
| Sum of weights          | 1 (fully invested)        | Utilize entire budget             |
| Minimum weight          | ≥ 0%                      | Avoid short-selling               |
| Maximum weight per stock| ≤10% per stock            | Ensures diversification           |
| Portfolio return        | ≥ 0                       | Avoid negative expected returns   |

---

## 🎯 Final Selected Portfolio

Below is our optimized and diversified portfolio:

| BSE Code | NSE Code | Stock Name        | Units |
|----------|----------|-------------------|-------|
|          |          | Ankit Met.Power   | 3     |
|          |          | Ashima            | 2113  |
|          |          | Essar Shipping    | 2017  |
|          |          | FCS Software      | 4     |
|          |          | H D I L           | 2113  |
|          |          | Prem. Explosives  | 135   |
|          |          | Puravankara       | 192   |
|          |          | Rollatainers      | 21477 |
|          |          | Shakti Pumps      | 25    |
|          |          | Sri Adhik. Bros.  | 397   |
|          |          | TCI Finance       | 6128  |
|          |          | Transwar.Fin.     | 4072  |
|          |          | Zenith Exports    | 245   |

---

## 📊 Final Portfolio Performance

| Metric                      | Value                |
|-----------------------------|----------------------|
| Portfolio Cost (₹)          | 9,99,807.49          |
| Final Portfolio Value (₹)   | 13,06,990.31         |
| Portfolio Delta (₹)         | +3,07,182.82         |
| Percentage Gain (%)         | 30.72%               |
| Portfolio Performance Score | **100 (capped)**     |

**Calculation:**

- **Portfolio Delta (₹)** = Final Value - Cost = 13,06,990.31 - 9,99,807.49 = ₹3,07,182.82
- **Percentage Gain/Loss (%)** = (Delta / Cost) × 100 = (3,07,182.82/9,99,807.49) × 100 = **30.72%**
- **Portfolio Performance Score (PPS)** = Base Score (70) + Gain% = 70 + 30.72 = **100 (max capped)**

---

## 🚀 Key Project Highlights

- **Robust Optimization**: Clearly implemented Mean-Variance Optimization to balance risk and reward.
- **Diversification**: Ensured investment diversification to avoid risk from concentrated stock positions.
- **High Returns**: Achieved an excellent overall portfolio return of **30.72%**.
- **Realistic Constraints**: Adhered strictly to budget constraints.

---

## 🧑‍💻 Technologies Used

- Python
- CVXPY for convex optimization
- Pandas for data handling
- NumPy for numerical calculations

---

## 📌 Future Improvement Possibilities

- **Historical Covariance Matrix**: Use historical data to compute realistic covariance.
- **Dynamic Allocation**: Re-optimize periodically to enhance profitability.

---

## 📜 Conclusion

Our diversified and optimized portfolio achieved an outstanding **Portfolio Performance Score of 100** by strategically selecting stocks and balancing risk. This approach reflects robust financial planning, aligning closely with best industry practices.

---

## 👨‍💻 Submission Files

- `team_03_portfolio.csv`: Detailed selected portfolio.
- `team_03_score_share.csv`: Group member score distribution.

---

## 🏅 Conclusion

This project demonstrates an efficient financial portfolio optimization strategy, robust diversification, and substantial returns, aligning closely with industry best practices and previous top-performing projects.

---

**Prepared by:**

- **Team 03**  
- Date: March 2025  
- Course: Financial Forensics Project

---

*Best of luck!* 🚀

