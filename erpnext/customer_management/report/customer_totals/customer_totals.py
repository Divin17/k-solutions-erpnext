# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    # Ensure filters exist
    if not filters:
        filters = {}

    # Initialize query conditions and parameters
    query_conditions = []
    query_params = {}

    # Apply customer filter if provided
    if filters.get("customer"):
        query_conditions.append("c.name = %(customer)s")
        query_params["customer"] = filters["customer"]

    # Handle Date Filters
    legal_job_date_filter = ""
    invoice_date_filter = ""
    payment_date_filter = ""

    if filters.get("from_date"):
        legal_job_date_filter += " AND lj.start_date >= %(from_date)s"
        invoice_date_filter += " AND si.posting_date >= %(from_date)s"
        payment_date_filter += " AND p.posting_date >= %(from_date)s"
        query_params["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        legal_job_date_filter += " AND lj.start_date <= %(to_date)s"
        invoice_date_filter += " AND si.posting_date <= %(to_date)s"
        payment_date_filter += " AND p.posting_date <= %(to_date)s"
        query_params["to_date"] = filters["to_date"]

    # Start SQL Query with dynamic date filters
    query = f"""
    SELECT
        c.name AS customer,

        -- Get total Legal Jobs per Currency using subqueries
        (SELECT COALESCE(SUM(lj.total_amount), 0) FROM `tabLegal Job` lj
         WHERE lj.customer = c.name AND lj.currency = 'RWF' {legal_job_date_filter}) AS total_legal_jobs_rwf,

        (SELECT COALESCE(SUM(lj.total_amount), 0) FROM `tabLegal Job` lj
         WHERE lj.customer = c.name AND lj.currency = 'USD' {legal_job_date_filter}) AS total_legal_jobs_usd,

        (SELECT COALESCE(SUM(lj.total_amount), 0) FROM `tabLegal Job` lj
         WHERE lj.customer = c.name AND lj.currency = 'EUR' {legal_job_date_filter}) AS total_legal_jobs_eur,

        (SELECT COALESCE(SUM(lj.total_amount), 0) FROM `tabLegal Job` lj
         WHERE lj.customer = c.name AND lj.currency = 'GBP' {legal_job_date_filter}) AS total_legal_jobs_gbp,

        -- Get total Invoices per Customer (converted to base currency)
        (SELECT COALESCE(SUM(si.base_grand_total), 0) FROM `tabSales Invoice` si
         WHERE si.customer = c.name AND si.docstatus = 1 {invoice_date_filter}) AS total_invoices_company_currency,

        -- Get total Payments per Customer (converted to base currency)
        (SELECT COALESCE(SUM(p.base_paid_amount), 0) FROM `tabPayment Entry` p
         WHERE p.party = c.name AND p.party_type = 'Customer' AND p.docstatus = 1 {payment_date_filter}) AS total_payments_company_currency,

        -- Fixed Currency Labels
        'USD' AS currency_usd,
        'EUR' AS currency_eur,
        'GBP' AS currency_gbp

    FROM `tabCustomer` c
    """

    # Append WHERE clause if conditions exist
    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    # Ensure ORDER BY is correctly placed at the end
    query += " ORDER BY c.name ASC"

    # Debugging: Print final query before execution
    print("Final SQL Query:", query)
    print("Query Params:", query_params)

    # Execute query and fetch data
    data = frappe.db.sql(query, query_params, as_dict=True)

    # Define report columns
    columns = [
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 300,
        },
        {
            "label": "Legal Jobs (RWF)",
            "fieldname": "total_legal_jobs_rwf",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Legal Jobs (USD)",
            "fieldname": "total_legal_jobs_usd",
            "fieldtype": "Currency",
            "options": "currency_usd",
            "width": 150,
        },
        {
            "label": "Legal Jobs (EUR)",
            "fieldname": "total_legal_jobs_eur",
            "fieldtype": "Currency",
            "options": "currency_eur",
            "width": 150,
        },
        {
            "label": "Legal Jobs (GBP)",
            "fieldname": "total_legal_jobs_gbp",
            "fieldtype": "Currency",
            "options": "currency_gbp",
            "width": 150,
        },
        {
            "label": "Invoices Total (Base Currency)",
            "fieldname": "total_invoices_company_currency",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Payments Total (Base Currency)",
            "fieldname": "total_payments_company_currency",
            "fieldtype": "Currency",
            "width": 150,
        },
        {"fieldname": "currency_usd", "fieldtype": "Data", "label": "USD", "hidden": 1},
        {"fieldname": "currency_eur", "fieldtype": "Data", "label": "EUR", "hidden": 1},
        {"fieldname": "currency_gbp", "fieldtype": "Data", "label": "GBP", "hidden": 1},
    ]

    return columns, data
