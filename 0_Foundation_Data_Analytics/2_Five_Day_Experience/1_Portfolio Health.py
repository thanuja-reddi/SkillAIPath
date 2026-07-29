# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Portfolio Health Analysis
# MAGIC %md
# MAGIC # Portfolio Health Analysis
# MAGIC
# MAGIC **Dataset:** `workspace.sap_dev.loans`

# COMMAND ----------

# DBTITLE 1,Data Check
# MAGIC %sql
# MAGIC -- Data validation check
# MAGIC SELECT 
# MAGIC   COUNT(*) AS total_loans,
# MAGIC   COUNT(DISTINCT loan_status) AS status_types,
# MAGIC   COUNT(DISTINCT customer_id) AS unique_customers
# MAGIC FROM workspace.sap_dev.loans;

# COMMAND ----------

# DBTITLE 1,Portfolio Status Distribution
# MAGIC %sql
# MAGIC -- Portfolio Status Distribution
# MAGIC
# MAGIC SELECT 
# MAGIC   loan_status,
# MAGIC   COUNT(*) AS loan_count,
# MAGIC   ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
# MAGIC FROM workspace.sap_dev.loans
# MAGIC GROUP BY loan_status
# MAGIC ORDER BY loan_count DESC;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Business Insights
# MAGIC
# MAGIC - Active loans account for **61.54%** of the portfolio, indicating that the majority of loans are performing.
# MAGIC - Defaulted loans represent **14.02%** of all loans, while overdue loans account for **7.66%**, highlighting areas that require close monitoring.
# MAGIC - In terms of value, Active loans contribute **₹130.97 crores**, whereas Defaulted and Overdue loans together represent **₹40.04 crores** of at-risk capital.
# MAGIC - Although most loans are active by volume, the amount tied up in defaulted and overdue loans is significant and requires effective risk management and recovery efforts.

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,Portfolio Scale Metrics
# MAGIC %sql
# MAGIC -- Portfolio Scale Metrics
# MAGIC
# MAGIC SELECT 
# MAGIC   COUNT(DISTINCT customer_id) AS total_customers,
# MAGIC   COUNT(*) AS total_loans,
# MAGIC   ROUND(SUM(loan_amount) / 10000000, 2) AS portfolio_value_cr,
# MAGIC   ROUND(AVG(loan_amount) / 100000, 2) AS avg_loan_size_lakh
# MAGIC FROM workspace.sap_dev.loans;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Business Insights
# MAGIC
# MAGIC - The company serves **2,433 unique customers** with a total of **5,000 loans**.
# MAGIC - The total portfolio value is **₹203.52 crores**, indicating a large lending portfolio.
# MAGIC - The average loan size is **₹4.07 lakhs**, suggesting that the portfolio mainly consists of medium-sized loans.
# MAGIC - On average, each customer has **2.06 loans** (5,000 ÷ 2,433), indicating that many customers have multiple loans.
# MAGIC - The portfolio is diversified across **2,433 customers**, but customers with multiple loans should be monitored to reduce concentration risk.

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,Risk Concentration
# MAGIC %sql
# MAGIC -- Risk Concentration by Loan Size
# MAGIC
# MAGIC SELECT 
# MAGIC   CASE 
# MAGIC     WHEN loan_amount < 300000 THEN 'Small (<₹3L)'
# MAGIC     WHEN loan_amount >= 300000 AND loan_amount <= 600000 THEN 'Medium (₹3L-₹6L)'
# MAGIC     WHEN loan_amount > 600000 THEN 'Large (>₹6L)'
# MAGIC   END AS risk_band,
# MAGIC   COUNT(*) AS total_loans,
# MAGIC   SUM(CASE WHEN loan_status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted_count,
# MAGIC   SUM(CASE WHEN loan_status = 'Overdue' THEN 1 ELSE 0 END) AS overdue_count,
# MAGIC   SUM(CASE WHEN loan_status = 'Active' THEN 1 ELSE 0 END) AS active_count
# MAGIC FROM workspace.sap_dev.loans
# MAGIC GROUP BY risk_band
# MAGIC ORDER BY 
# MAGIC   CASE 
# MAGIC     WHEN risk_band = 'Small (<₹3L)' THEN 1
# MAGIC     WHEN risk_band = 'Medium (₹3L-₹6L)' THEN 2
# MAGIC     WHEN risk_band = 'Large (>₹6L)' THEN 3
# MAGIC   END;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Business Insights
# MAGIC
# MAGIC - Small loans account for the largest portion of the portfolio with **2,682 loans**.
# MAGIC - The **Small loan segment has the highest default rate (16.78%)**, making it the riskiest category.
# MAGIC - Medium and Large loan segments have lower default rates of **11.22%** and **10.43%**, respectively.
# MAGIC - Although Large loans involve higher loan amounts, they have a lower default rate than Small loans.
# MAGIC - The underwriting team should strengthen credit assessment and monitoring for Small loans to reduce future defaults.
# MAGIC
# MAGIC ### Recommendation
# MAGIC
# MAGIC If the company approves **100 Small loans**, approximately **17 loans** may default based on current portfolio performance. In comparison, approving **100 Large loans** would result in approximately **10 defaults**. Therefore, the **Small loan segment requires stricter underwriting policies and enhanced risk monitoring**.

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,Financial Impact
# MAGIC %sql
# MAGIC -- Financial Impact by Status
# MAGIC
# MAGIC SELECT 
# MAGIC   loan_status,
# MAGIC   ROUND(SUM(loan_amount) / 10000000, 2) AS total_value_cr
# MAGIC FROM workspace.sap_dev.loans
# MAGIC GROUP BY loan_status
# MAGIC ORDER BY total_value_cr DESC;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Business Insights
# MAGIC
# MAGIC - The total loan portfolio is valued at **₹203.52 crores**.
# MAGIC - **Active loans contribute ₹130.97 crores**, representing the largest share of the portfolio and generating ongoing revenue.
# MAGIC - **Closed loans account for ₹32.51 crores**, reflecting loans that have been successfully repaid.
# MAGIC - **Defaulted loans amount to ₹24.38 crores**, representing potential credit losses.
# MAGIC - **Overdue loans total ₹15.66 crores** and require immediate follow-up to prevent them from becoming defaults.
# MAGIC - The **total at-risk capital is ₹40.04 crores** (Defaulted + Overdue), which should be considered for provisioning and risk management.
# MAGIC
# MAGIC ### Recommendation
# MAGIC
# MAGIC The company should prioritize reducing **₹40.04 crores of at-risk capital** by strengthening recovery efforts for overdue loans and improving collection strategies for defaulted accounts. Lowering the at-risk portfolio will improve financial stability and reduce future provisioning requirements.

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,Executive Dashboard
# MAGIC %sql
# MAGIC -- Executive Dashboard
# MAGIC
# MAGIC WITH portfolio_metrics AS (
# MAGIC   SELECT 
# MAGIC     COUNT(*) AS total_loans,
# MAGIC     SUM(CASE WHEN loan_status = 'Active' THEN 1 ELSE 0 END) AS active_count,
# MAGIC     SUM(CASE WHEN loan_status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted_count,
# MAGIC     SUM(CASE WHEN loan_status = 'Overdue' THEN 1 ELSE 0 END) AS overdue_count,
# MAGIC     ROUND(SUM(loan_amount) / 10000000, 2) AS portfolio_value_cr,
# MAGIC     ROUND(SUM(CASE WHEN loan_status IN ('Defaulted', 'Overdue') THEN loan_amount ELSE 0 END) / 10000000, 2) AS at_risk_value_cr,
# MAGIC     ROUND((SUM(CASE WHEN loan_status = 'Defaulted' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS default_rate_pct
# MAGIC   FROM workspace.sap_dev.loans
# MAGIC )
# MAGIC
# MAGIC SELECT 
# MAGIC   *,
# MAGIC   CASE 
# MAGIC     WHEN default_rate_pct < 5.00 THEN 'HEALTHY'
# MAGIC     WHEN default_rate_pct >= 5.00 AND default_rate_pct < 10.00 THEN 'MODERATE RISK'
# MAGIC     WHEN default_rate_pct >= 10.00 AND default_rate_pct < 15.00 THEN 'HIGH RISK'
# MAGIC     WHEN default_rate_pct >= 15.00 THEN 'CRITICAL'
# MAGIC   END AS health_classification
# MAGIC FROM portfolio_metrics;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Business Insights
# MAGIC
# MAGIC - The loan portfolio consists of **5,000 loans** with a total value of **₹203.52 crores**.
# MAGIC - **3,077 loans (61.54%)** are active, indicating that most loans are currently performing.
# MAGIC - **1,084 loans** are either overdue or defaulted, requiring immediate attention.
# MAGIC - The **default rate is 14.02%**, which falls under the **HIGH RISK** category based on the defined business thresholds.
# MAGIC - The company currently has **₹40.04 crores of at-risk capital**, representing loans that are overdue or defaulted.

# COMMAND ----------

