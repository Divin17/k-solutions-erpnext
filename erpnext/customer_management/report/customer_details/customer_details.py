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
                "label": "Invoice #",
                "fieldname": "invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 160,
            },
            {
                "fieldname": "currency",
                "label": "Currency",
                "fieldtype": "Link",
                "options": "Currency",
                "hidden": 1,
                "width": 160,
            },
            {
                "label": "ITM-001: Project (Company Currency)",
                "fieldname": "item_1",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "ITM-002:Retainers (Company Currency)",
                "fieldname": "item_2",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "ITM-003: Litigations (Company Currency)",
                "fieldname": "item_3",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "ITM-004: Company Secretarial (Company Currency)",
                "fieldname": "item_4",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "ITM005: Others (Company Currency)",
                "fieldname": "item_5",
                "fieldtype": "Currency",
                "options": "currency",
                "width": 160,
            },
            {
                "label": "Start Date",
                "fieldname": "start_date",
                "fieldtype": "Date",
                "options": "",
                "width": 160,
            },
            {
                "label": "End Date",
                "fieldname": "end_date",
                "fieldtype": "Date",
                "options": "",
                "width": 160,
            },
            {
                "label": "Period Taken",
                "fieldname": "period_taken",
                "fieldtype": "Data",
                "options": "",
                "width": 160,
            },
            {
                "label": "Paid On",
                "fieldname": "paid_on",
                "fieldtype": "Data",
                "options": "",
                "width": 160,
            },
            {
                "label": "Days Unpaid",
                "fieldname": "days_unpaid",
                "fieldtype": "Data",
                "options": "",
                "width": 160,
            },
            {
                "label": "Done By",
                "fieldname": "done_by",
                "fieldtype": "Link",
                "options": "User",
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
                "hidden": 1,
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
                "label": "Days Taken",
                "fieldname": "days_taken",
                "fieldtype": "Data",
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
                "hidden": 1,
            },
            {
                "fieldname": "company_currency",
                "label": "Company Currency",
                "fieldtype": "Link",
                "options": "Currency",
                "width": 160,
                "hidden": 1,
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
                "hidden": 1,
            },
            {
                "label": "Total (Company Currency)",
                "fieldname": "company_currency_total",
                "fieldtype": "Currency",
                "options": "company_currency",
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
            conditions.append("`tabSales Invoice`.customer = %(customer)s")
        if filters.get("invoices_status"):
            conditions.append("`tabSales Invoice`.status = %(invoices_status)s")

        where_clause = " AND ".join(conditions)
        if where_clause:
            where_clause = "WHERE " + where_clause
        else:
            where_clause = ""

        # Fetch Data
        data = frappe.db.sql(
            f"""
                SELECT
                    `tabSales Invoice`.`posting_date` AS `date`,
                    `tabSales Invoice`.`name` AS `invoice`,
                    `tabSales Invoice`.`customer`,
                    `tabSales Invoice`.`job_description`,
                    `tabSales Invoice`.`price_list_currency`,
                    SUM(CASE WHEN `tabSales Invoice Item`.`item_code` = 'ITM-001' THEN `tabSales Invoice Item`.`base_amount` ELSE 0 END) AS `item_1`,
                    SUM(CASE WHEN `tabSales Invoice Item`.`item_code` = 'ITM-002' THEN `tabSales Invoice Item`.`base_amount` ELSE 0 END) AS `item_2`,
                    SUM(CASE WHEN `tabSales Invoice Item`.`item_code` = 'ITM-003' THEN `tabSales Invoice Item`.`base_amount` ELSE 0 END) AS `item_3`,
                    SUM(CASE WHEN `tabSales Invoice Item`.`item_code` = 'ITM-004' THEN `tabSales Invoice Item`.`base_amount` ELSE 0 END) AS `item_4`,
                    SUM(CASE WHEN `tabSales Invoice Item`.`item_code` = 'ITM-005' THEN `tabSales Invoice Item`.`base_amount` ELSE 0 END) AS `item_5`,
                    `tabLegal Job`.`start_date`,
                    `tabLegal Job`.`end_date`,
                    CONCAT(
                        TIMESTAMPDIFF(DAY, `tabLegal Job`.`start_date`, `tabLegal Job`.`end_date`), ' day(s)'
                    ) AS `period_taken`,
                    CONCAT(
                        TIMESTAMPDIFF(DAY, `tabLegal Job`.`start_date`, `tabLegal Job`.`end_date`), ' day(s)'
                    ) AS `period_taken`,
                    DATE_FORMAT(MAX(`tabPayment Entry`.`reference_date`), '%%d-%%m-%%Y') AS `paid_on`,
                    CASE
                        WHEN `tabSales Invoice`.`status` = 'Unpaid' 
                        THEN CONCAT(DATEDIFF(CURDATE(), `tabSales Invoice`.`posting_date`), ' day(s)')
                        WHEN `tabSales Invoice`.`status` = 'Overdue' 
                        THEN CONCAT(DATEDIFF(CURDATE(), `tabSales Invoice`.`due_date`), ' day(s) overdue')
                        ELSE 'Paid'
                     END AS `days_unpaid`,
                    `tabLegal Job`.`done_by`
                FROM
                    `tabSales Invoice`
                LEFT JOIN
                    `tabSales Invoice Item` ON `tabSales Invoice`.`name` = `tabSales Invoice Item`.`parent`
                LEFT JOIN
                    `tabLegal Job` ON `tabSales Invoice`.`legal_job` = `tabLegal Job`.`name`
                LEFT JOIN
                    `tabPayment Entry Reference` ON `tabSales Invoice`.`name` = `tabPayment Entry Reference`.`reference_name`
                LEFT JOIN
                    `tabPayment Entry` ON `tabPayment Entry Reference`.`parent` = `tabPayment Entry`.`name`
                {where_clause}
                GROUP BY
                    `tabSales Invoice`.`name`;

            """,
            filters,
            as_dict=True,
        )

    if filters.get("report_type") == "Legal Jobs":
        if filters.get("customer"):
            conditions.append("lj.customer = %(customer)s")
        if filters.get("from_date") and filters.get("to_date"):
            conditions.append("lj.start_date BETWEEN %(from_date)s AND %(to_date)s")
        if filters.get("legal_jobs_status"):
            conditions.append("lj.status = %(legal_jobs_status)s")
        if filters.get("currency"):
            conditions.append("lj.currency = %(currency)s")

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
                lj.status AS status,
                CASE
                    WHEN lj.end_date IS NULL
                    THEN CONCAT(DATEDIFF(CURDATE(), lj.start_date), ' day(s)')
                    ELSE CONCAT(DATEDIFF(lj.end_date, lj.start_date), ' day(s)')
                END AS `days_taken`
            FROM
                `tabLegal Job` lj
            {where_clause}
        """,
            filters,
            as_dict=True,
        )
    if filters.get("report_type") == "Invoices":
        conditions.append("si.docstatus = 1")
        if filters.get("customer"):
            conditions.append("si.customer = %(customer)s")
        if filters.get("from_date") and filters.get("to_date"):
            conditions.append("si.posting_date BETWEEN %(from_date)s AND %(to_date)s")
        if filters.get("invoices_status"):
            conditions.append("si.status = %(invoices_status)s")
        if filters.get("currency"):
            conditions.append("si.currency = %(currency)s")

        where_clause = " AND ".join(conditions)
        if where_clause:
            where_clause = "WHERE " + where_clause
        # Query Legal Jobs Data
        data = frappe.db.sql(
            f"""
            SELECT
                si.posting_date AS date,
                si.currency AS currency,
                si.price_list_currency AS company_currency,
                si.customer AS customer,
                si.name AS invoice,
                si.base_grand_total AS company_currency_total,
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
