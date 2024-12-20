# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    report_type = filters.get("report_type")
    columns = []
    if report_type == "All":
        columns = [
            {
                "label": "Customer",
                "fieldname": "customer",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 160,
            },
            {
                "fieldname": "currency",
                "label": "Currency",
                "fieldtype": "Link",
                "options": "Currency",
                "width": 160,
            },
            {
                "label": "Legal Jobs Total",
                "fieldname": "legal_jobs_total",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "Invoices Total",
                "fieldname": "invoices_total",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
        ]
    if report_type == "Legal Jobs":
        columns = [
            {
                "label": "Date",
                "fieldname": "date",
                "fieldtype": "Date",
                "width": 160,
            },
            {
                "fieldname": "currency",
                "label": "Currency",
                "fieldtype": "Link",
                "options": "Currency",
                "width": 160,
            },
            {
                "label": "Customer",
                "fieldname": "customer",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 160,
            },
            {
                "label": "Legal Job",
                "fieldname": "legal_job",
                "fieldtype": "Link",
                "options": "Legal Job",
                "width": 160,
            },
            {
                "label": "Total",
                "fieldname": "total",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "Status",
                "fieldname": "status",
                "fieldtype": "Data",
                "width": 160,
            },
        ]
    if report_type == "Invoices":
        columns = [
            {
                "label": "Date",
                "fieldname": "date",
                "fieldtype": "Date",
                "width": 160,
            },
            {
                "fieldname": "currency",
                "label": "Currency",
                "fieldtype": "Link",
                "options": "Currency",
                "width": 160,
            },
            {
                "label": "Customer",
                "fieldname": "customer",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 160,
            },
            {
                "label": "Invoice",
                "fieldname": "invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 160,
            },
            {
                "label": "Total",
                "fieldname": "total",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "Status",
                "fieldname": "status",
                "fieldtype": "Data",
                "width": 160,
            },
        ]
    return columns


def get_data(filters):
    data = []
    conditions = []
    if filters.get("report_type") == "All":
        # Build Query Conditions Based on Filters
        if filters.get("customer"):
            conditions.append("c.customer_name = %(customer)s")

        where_clause = " AND ".join(conditions)
        if where_clause:
            where_clause = "WHERE " + where_clause
        else:
            where_clause = ""

        # Fetch Data
        data = frappe.db.sql(
            f"""
            SELECT
                c.customer_name AS customer,
                c.default_currency AS currency,
                COALESCE((
                    SELECT SUM(lj.total_amount)
                    FROM `tabLegal Job` lj
                    WHERE lj.customer = c.customer_name
                    {f"AND lj.start_date BETWEEN %(from_date)s AND %(to_date)s" if filters.get("from_date") and filters.get("to_date") else ""}
                ), 0) AS legal_jobs_total,
                COALESCE((
                    SELECT SUM(si.grand_total)
                    FROM `tabSales Invoice` si
                    WHERE si.customer = c.customer_name
                    AND si.docstatus = 1
                    {f"AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s" if filters.get("from_date") and filters.get("to_date") else ""}
                ), 0) AS invoices_total
            FROM
                `tabCustomer` c
            {where_clause}
            """,
            filters,
            as_dict=True,
        )

    if filters.get("report_type") == "Legal Jobs":
        if filters.get("customer"):
            conditions.append("lj.customer = %(customer)s")
        if filters.get("from_date") and filters.get("to_date"):
            conditions.append("lj.start_date BETWEEN %(from_date)s AND %(to_date)s")

        where_clause = " AND ".join(conditions)
        if where_clause:
            where_clause = "WHERE " + where_clause

        # Query Legal Jobs Data
        data = frappe.db.sql(
            f"""
            SELECT
                lj.start_date AS date,
                lj.currency AS currency,
                lj.customer AS customer,
                lj.name AS legal_job,
                lj.total_amount AS total,
                lj.status AS status
            FROM
                `tabLegal Job` lj
            {where_clause}
        """,
            filters,
            as_dict=True,
        )
    if filters.get("report_type") == "Invoices":
        if filters.get("customer"):
            conditions.append("si.customer = %(customer)s")
        if filters.get("from_date") and filters.get("to_date"):
            conditions.append("si.posting_date BETWEEN %(from_date)s AND %(to_date)s")

        where_clause = " AND ".join(conditions)
        if where_clause:
            where_clause = "WHERE " + where_clause
        # Query Legal Jobs Data
        data = frappe.db.sql(
            f"""
            SELECT
                si.posting_date AS date,
                si.currency AS currency,
                si.customer AS customer,
                si.name AS invoice,
                si.grand_total AS total,
                si.status AS status
            FROM
                `tabSales Invoice` si
            {where_clause}
        """,
            filters,
            as_dict=True,
        )
    return data
