# Enterprise Project Portfolio Risk & Analytics Simulator

## Project Overview

This project simulates an enterprise-scale engineering portfolio to analyze **project risk exposure, workforce capacity constraints, and operational disruptions** in complex R&D environments such as semiconductor or automotive industries.

The system models **120 projects and 80 employees** and introduces realistic enterprise dynamics including:

- resource capacity constraints
- project dependencies
- operational issues and rework
- portfolio-level risk exposure

The goal is to demonstrate how **simulation, SQL analytics, and interactive dashboards** can be combined to monitor portfolio health and identify potential bottlenecks.

---

## Dashboard Preview

The Streamlit dashboard provides an overview of portfolio health, departmental risk exposure, and operational rework trends.

![Portfolio Dashboard](images/dashboard.jpg)

---

## Tech Stack

**Simulation Engine**
- Python
- Object-Oriented Programming

**Data Engineering**
- Pandas
- NumPy
- SQLite

**Analytics**
- SQL (CTE queries)
- Window Functions (LAG, DENSE_RANK)

**Visualization**
- Streamlit
- Plotly

---

## Key Features

### Portfolio Simulation Engine

The simulation models a complex multi-project environment where:

- employees have weekly capacity limits
- projects require varying workloads and durations
- operational issues generate additional rework
- project dependencies affect progress

This allows realistic modeling of **enterprise project portfolio dynamics**.

---

### Dependency-Aware Project Network

Projects can depend on other projects through a **Directed Acyclic Graph (DAG)** structure.

This simulates real-world situations where certain projects cannot progress until upstream tasks are completed.

---

### Workforce Capacity Modeling

Employee productivity includes:

- weekly capacity limits
- multi-project context switching penalties
- department-based project assignments

This allows the simulation to capture **resource bottlenecks and utilization effects**.

---

### Stochastic Operational Disruptions

Operational issues are generated using a **Poisson distribution**.

These issues introduce additional rework hours and create unpredictable disruptions in project timelines.

---

### Risk Exposure Analytics (SQL)

The simulation outputs are stored in a **relational SQLite database** and analyzed using SQL.

Key analytics include:

- departmental risk exposure
- workforce utilization
- project delay forecasting
- dependency impact analysis

SQL queries use modern analytics patterns such as:

- Common Table Expressions (CTE)
- Window Functions (LAG, DENSE_RANK)

---

### Interactive Portfolio Dashboard

The Streamlit dashboard allows users to explore:

- portfolio risk exposure by department
- weekly rework growth trends
- the most delayed projects in the portfolio
- dependency status for at-risk projects
  
---

## ⚙️ How to Run
1. Clone the repo: `git clone https://github.com/omaewamoushindei/enterprise-ppm-risk-simulator.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run app.py`
