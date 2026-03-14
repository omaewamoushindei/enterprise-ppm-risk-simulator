from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DB_PATH = Path(__file__).resolve().parent / "portfolio.db"


def _get_connection() -> sqlite3.Connection:
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


@st.cache_data(show_spinner=False)
def run_query(sql: str, params: tuple = ()) -> pd.DataFrame:
	with _get_connection() as conn:
		return pd.read_sql_query(sql, conn, params=params)


def get_departments() -> list[str]:
	sql = "SELECT DISTINCT department FROM projects ORDER BY department;"
	df = run_query(sql)
	return df["department"].tolist()


def query_risk_by_department(selected_department: str) -> pd.DataFrame:
	where_clause = ""
	params: tuple = ()
	if selected_department != "All":
		where_clause = "WHERE p.department = ?"
		params = (selected_department,)

	sql = f"""
	WITH project_risk AS (
		SELECT
			p.department,
			p.project_id,
			(p.total_required_hours * (p.delay_pct / 100.0)) AS risk_exposure
		FROM projects p
		{where_clause}
	),
	dept_risk AS (
		SELECT
			department,
			SUM(risk_exposure) AS total_risk_exposure
		FROM project_risk
		GROUP BY department
	),
	dept_util AS (
		SELECT
			department,
			AVG(utilization_pct) AS avg_employee_utilization
		FROM employee_capacity_audit
		GROUP BY department
	)
	SELECT
		dr.department,
		dr.total_risk_exposure,
		du.avg_employee_utilization
	FROM dept_risk dr
	LEFT JOIN dept_util du ON du.department = dr.department
	ORDER BY dr.total_risk_exposure DESC;
	"""
	return run_query(sql, params)


def query_top_risk_projects(selected_department: str) -> pd.DataFrame:
	where_clause = ""
	params: tuple = ()
	if selected_department != "All":
		where_clause = "WHERE p.department = ?"
		params = (selected_department,)

	sql = f"""
	WITH ranked_projects AS (
		SELECT
			p.project_id,
			p.department,
			p.progress_pct,
			p.delay_pct,
			p.forecast_delay_weeks,
			p.remaining_hours,
			DENSE_RANK() OVER (
				ORDER BY p.forecast_delay_weeks DESC, p.delay_pct DESC, p.remaining_hours DESC
			) AS risk_rank
		FROM projects p
		{where_clause}
	),
	top5 AS (
		SELECT *
		FROM ranked_projects
		WHERE risk_rank <= 5
	),
	predecessor_status AS (
		SELECT
			d.child_project_id,
			d.predecessor_project_id,
			pp.progress_pct AS predecessor_progress_pct,
			CASE
				WHEN pp.progress_pct >= 100 THEN 'Cleared'
				WHEN pp.progress_pct >= 40 THEN 'Partially Complete'
				ELSE 'Blocking'
			END AS predecessor_state
		FROM project_dependencies d
		LEFT JOIN projects pp ON pp.project_id = d.predecessor_project_id
	)
	SELECT
		t.project_id,
		t.department,
		ROUND(t.forecast_delay_weeks, 2) AS forecast_delay_weeks,
		ROUND(t.delay_pct, 2) AS delay_pct,
		ROUND(t.progress_pct, 2) AS progress_pct,
		ROUND(t.remaining_hours, 2) AS remaining_hours,
		COALESCE(GROUP_CONCAT(ps.predecessor_project_id), 'No Predecessor') AS predecessor_ids,
		COALESCE(GROUP_CONCAT(ps.predecessor_state), 'No Predecessor') AS predecessor_statuses
	FROM top5 t
	LEFT JOIN predecessor_status ps ON ps.child_project_id = t.project_id
	GROUP BY
		t.project_id,
		t.department,
		t.forecast_delay_weeks,
		t.delay_pct,
		t.progress_pct,
		t.remaining_hours
	ORDER BY
		t.forecast_delay_weeks DESC,
		t.delay_pct DESC,
		t.project_id;
	"""
	return run_query(sql, params)


def query_weekly_rework_growth() -> pd.DataFrame:
	sql = """
	WITH rework_series AS (
		SELECT
			week,
			total_rework_hours,
			LAG(total_rework_hours) OVER (ORDER BY week) AS prev_week_rework
		FROM weekly_rework
	)
	SELECT
		week,
		ROUND(total_rework_hours, 2) AS total_rework_hours,
		ROUND(total_rework_hours - COALESCE(prev_week_rework, 0), 2) AS wow_abs_growth,
		ROUND(
			CASE
				WHEN prev_week_rework IS NULL OR prev_week_rework = 0 THEN NULL
				ELSE ((total_rework_hours - prev_week_rework) / prev_week_rework) * 100.0
			END,
			2
		) AS wow_pct_growth
	FROM rework_series
	ORDER BY week;
	"""
	return run_query(sql)


def query_total_projects(selected_department: str) -> int:
	if selected_department == "All":
		sql = "SELECT COUNT(*) AS total_projects FROM projects;"
		params: tuple = ()
	else:
		sql = "SELECT COUNT(*) AS total_projects FROM projects WHERE department = ?;"
		params = (selected_department,)
	df = run_query(sql, params)
	return int(df.loc[0, "total_projects"])


def query_department_utilization(department: str) -> float:
	sql = """
	SELECT AVG(utilization_pct) AS avg_department_utilization
	FROM employee_capacity_audit
	WHERE department = ?;
	"""
	df = run_query(sql, (department,))
	val = df.loc[0, "avg_department_utilization"]
	return 0.0 if pd.isna(val) else float(val)


def query_total_portfolio_risk(selected_department: str) -> float:
	if selected_department == "All":
		sql = """
		SELECT SUM(total_required_hours * (delay_pct / 100.0)) AS total_portfolio_risk
		FROM projects;
		"""
		params: tuple = ()
	else:
		sql = """
		SELECT SUM(total_required_hours * (delay_pct / 100.0)) AS total_portfolio_risk
		FROM projects
		WHERE department = ?;
		"""
		params = (selected_department,)

	df = run_query(sql, params)
	val = df.loc[0, "total_portfolio_risk"]
	return 0.0 if pd.isna(val) else float(val)


def main() -> None:
	st.set_page_config(page_title="Portfolio Risk & Capacity Dashboard", layout="wide")

	st.title("Portfolio Risk & Capacity Dashboard")
	st.caption("Source: SQLite portfolio.db | PMO analytics for project risk and workforce utilization")

	if not DB_PATH.exists():
		st.error(f"Database not found at {DB_PATH}. Please run the simulation and SQL setup first.")
		st.stop()

	departments = get_departments()
	if not departments:
		st.error("No department data found in database.")
		st.stop()

	st.sidebar.header("Filters")
	selected_department = st.sidebar.selectbox(
		"Department",
		options=["All", *departments],
		index=0,
	)

	risk_by_dept = query_risk_by_department(selected_department)
	top_risk_projects = query_top_risk_projects(selected_department)
	rework_growth = query_weekly_rework_growth()

	total_projects = query_total_projects(selected_department)

	if selected_department != "All":
		utilization_department = selected_department
	elif "Chip Design" in departments:
		utilization_department = "Chip Design"
	else:
		utilization_department = departments[0]

	department_utilization = query_department_utilization(utilization_department)
	total_portfolio_risk = query_total_portfolio_risk(selected_department)

	kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
	kpi_col1.metric("Total Projects", f"{total_projects:,}")
	kpi_col2.metric(f"{utilization_department} Utilization", f"{department_utilization:.2f}%")
	kpi_col3.metric("Total Portfolio Risk", f"{total_portfolio_risk:,.2f}")

	chart_col1, chart_col2 = st.columns(2)

	with chart_col1:
		st.subheader("Risk Exposure by Department")
		if risk_by_dept.empty:
			st.info("No risk data available for the selected filter.")
		else:
			fig_risk = px.bar(
				risk_by_dept,
				x="department",
				y="total_risk_exposure",
				color="department",
				text_auto=".2s",
				labels={
					"department": "Department",
					"total_risk_exposure": "Risk Exposure",
				},
				title="Departmental Risk Exposure",
			)
			fig_risk.update_layout(showlegend=False, margin=dict(l=10, r=10, t=60, b=10))
			st.plotly_chart(fig_risk, use_container_width=True)

	with chart_col2:
		st.subheader("Weekly Rework Growth")
		if rework_growth.empty:
			st.info("No rework growth data available.")
		else:
			fig_rework = px.line(
				rework_growth,
				x="week",
				y=["total_rework_hours", "wow_abs_growth"],
				markers=True,
				labels={
					"value": "Hours",
					"week": "Week",
					"variable": "Metric",
				},
				title="Portfolio Rework Trend and WoW Growth",
			)
			fig_rework.update_layout(margin=dict(l=10, r=10, t=60, b=10))
			st.plotly_chart(fig_rework, use_container_width=True)

	st.subheader("Top 5 At-Risk Projects")
	if top_risk_projects.empty:
		st.info("No at-risk project data available for the selected filter.")
	else:
		st.dataframe(top_risk_projects, use_container_width=True, hide_index=True)

	if selected_department != "All":
		st.caption("Note: Rework growth is portfolio-level and is not department-scoped.")


if __name__ == "__main__":
	main()