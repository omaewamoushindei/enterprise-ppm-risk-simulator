# Enterprise Project Portfolio Risk & Analytics Simulator
## Dashboard Preview

The Streamlit dashboard provides an overview of portfolio health,
departmental risk exposure, and operational rework trends.

![Portfolio Dashboard](images/dashboard.jpg)
## 📌 Project Overview
This platform simulates a complex engineering portfolio (120 projects, 80 employees) to analyze risk exposure and resource bottlenecks in an enterprise environment (e.g., Semiconductor or Automotive industries). It moves beyond static planning by introducing stochastic modeling, project dependencies, and real-time capacity constraints.

## 🛠️ Tech Stack
- **Engine:** Python (Object-Oriented Programming)
- **Analytics:** SQL (SQLite3) using CTEs and Window Functions
- **Visualization:** Streamlit & Plotly
- **Data Engineering:** NumPy (Stochastic Modeling), Pandas

## 🚀 Key Features
- **Stochastic Risk Modeling:** Uses Poisson distribution for operational issues and Gamma distribution for project durations.
- **Dependency-Aware Network:** Implements Directed Acyclic Graph (DAG) logic where software progress is constrained by hardware milestones.
- **Resource Optimization:** Models "Context Switching Penalties" and departmental throughput caps.
- **SQL-Based PMO Insights:** Relational database architecture to track "Risk Exposure" and "Workforce Utilization."
- **Executive Dashboard:** Interactive web-app for portfolio health monitoring and forecasting.

## 📊 Sample Insights (SQL)
- **Bottleneck Detection:** Identified Software Department at 99.97% utilization.
- **Forecasting:** Calculated project-specific delay weeks based on recent burn rates.
- **Risk Trends:** Tracked week-over-week rework growth to predict portfolio-wide shocks.

## ⚙️ How to Run
1. Clone the repo: `git clone https://github.com/omaewamoushindei/enterprise-ppm-risk-simulator.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run app.py`
# Enterprise Project Portfolio Risk & Analytics Simulator

## 📌 Project Overview
This platform simulates a complex engineering portfolio (120 projects, 80 employees) to analyze risk exposure and resource bottlenecks in an enterprise environment (e.g., Semiconductor or Automotive industries). It moves beyond static planning by introducing stochastic modeling, project dependencies, and real-time capacity constraints.

## 🛠️ Tech Stack
- **Engine:** Python (Object-Oriented Programming)
- **Analytics:** SQL (SQLite3) using CTEs and Window Functions
- **Visualization:** Streamlit & Plotly
- **Data Engineering:** NumPy (Stochastic Modeling), Pandas

## 🚀 Key Features
- **Stochastic Risk Modeling:** Uses Poisson distribution for operational issues and Gamma distribution for project durations.
- **Dependency-Aware Network:** Implements Directed Acyclic Graph (DAG) logic where software progress is constrained by hardware milestones.
- **Resource Optimization:** Models "Context Switching Penalties" and departmental throughput caps.
- **SQL-Based PMO Insights:** Relational database architecture to track "Risk Exposure" and "Workforce Utilization."
- **Executive Dashboard:** Interactive web-app for portfolio health monitoring and forecasting.

## 📊 Sample Insights (SQL)
- **Bottleneck Detection:** Identified Software Department at 99.97% utilization.
- **Forecasting:** Calculated project-specific delay weeks based on recent burn rates.
- **Risk Trends:** Tracked week-over-week rework growth to predict portfolio-wide shocks.

## ⚙️ How to Run
1. Clone the repo: `git clone https://github.com/omaewamoushindei/enterprise-ppm-risk-simulator.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run app.py`
