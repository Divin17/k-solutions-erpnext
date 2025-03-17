// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Details"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
			read_only: 1
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "currency",
			label: __("Currency"),
			fieldtype: "Link",
			options: "Currency",
			mandatory_depends_on: "eval:doc.report_type == 'All'"
		},
		{
			fieldname: "report_type",
			label: __("Report Type"),
			fieldtype: "Select",
			options: "All\nLegal Jobs\nInvoices",
			reqd: 1,
			on_change: function () {
				let report_type = frappe.query_report.get_filter_value('report_type');
				if (report_type === "All") {
					// Get the company's default currency
					frappe.call({
						method: "frappe.client.get_value",
						args: {
							doctype: "Company",
							filters: { name: frappe.query_report.get_filter_value('company') },
							fieldname: "default_currency"
						},
						callback: function (response) {
							if (response.message && response.message.default_currency) {
								frappe.query_report.set_filter_value('currency', response.message.default_currency);
							}
						}
					});
				} else {
					frappe.query_report.set_filter_value('currency', "");
				}
			}
		},
		{
			fieldname: "invoices_status",
			label: __("Invoices Status"),
			fieldtype: "Select",
			"depends_on": "eval: doc.report_type == 'Invoices' || doc.report_type == 'All'",
			options: "\nDraft\nReturn\nCredit Note Issued\nSubmitted\nPaid\nPartly Paid\nUnpaid\nUnpaid and Discounted\nPartly Paid and Discounted\nOverdue and Discounted\nOverdue\nCancelled\nInternal Transfer",
			reqd: 0
		},
		{
			fieldname: "legal_jobs_status",
			label: __("Legal Jobs Status"),
			fieldtype: "Select",
			"depends_on": "eval: doc.report_type == 'Legal Jobs'",
			options: "\nOngoing\nOn Hold\nCompleted\nInvoiced\nPartly Paid\nPaid\nRejected",
			reqd: 0
		},
	]
};