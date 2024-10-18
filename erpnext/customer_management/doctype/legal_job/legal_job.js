// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Legal Job", {
	refresh: function (frm) {
		frm.add_custom_button("Invoice the Job", function () {
			console.log(frm.doc.services);
			frappe.route_options = {
				customer: frm.doc.customer,
				legal_job: frm.doc.name,
			};
			frappe.new_doc("Sales Invoice");
		});
	},
	onload_post_render: function (frm) {
		frm.refresh_field("services");
	},
	customer: async function (frm) {
		let default_currency = (await frappe.db.get_value("Company", frm.doc.company, "default_currency"))
			.message.default_currency;
		let customer_currency = (await frappe.db.get_value("Customer", frm.doc.customer, "default_currency"))
			.message.default_currency;
		let exchange_rate = (
			await frappe.db.get_value(
				"Currency Exchange",
				{
					to_currency: customer_currency,
					from_currency: default_currency,
				},
				"exchange_rate"
			)
		).message.exchange_rate;
		console.log("Currency", exchange_rate);

		frm.set_value("currency", customer_currency);
		frm.set_value("conversion_rate", exchange_rate);
		frm.refresh();
	},
	address: function (frm) {
		if (frm.doc.address) {
			frappe.call({
				method: "frappe.contacts.doctype.address.address.get_address_display",
				args: {
					address_dict: frm.doc.address,
				},
				callback: function (r) {
					frm.set_value("address_detail", r.message);
				},
			});
		}
		if (!frm.doc.address) {
			frm.set_value("primary_address", "");
		}
	},
	quotation: function (frm) {
		frm.events.get_quotation_items(frm);
	},
	get_quotation_items: function (frm) {
		frappe.db
			.get_list("Quotation Item", {
				fields: ["item_code", "item_name", "qty", "rate", "amount"],
				filters: { parent: frm.doc.quotation },
			})
			.then((res) => {
				frm.clear_table("services");
				res.forEach((item) => {
					let row = frm.add_child("services");
					frappe.model.set_value(row.doctype, row.name, "item", item.item_code);
					frappe.model.set_value(row.doctype, row.name, "qty", item.qty);
					frappe.model.set_value(row.doctype, row.name, "rate", item.rate);
					frappe.model.set_value(row.doctype, row.name, "amount", item.amount);
					frm.refresh_field("services");
				});
			});
	},
});
frappe.ui.form.on("Legal Job Items", {
	qty: function (frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
		calculate_total_amount(frm);
	},
	rate: function (frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
		calculate_total_amount(frm);
	},
	amount: function (frm, cdt, cdn) {
		calculate_total_amount(frm);
	},
});
var calculate_amount = (frm, cdt, cdn) => {
	let amount = locals[cdt][cdn]["qty"] * locals[cdt][cdn]["rate"];
	frappe.model.set_value(cdt, cdn, "amount", amount);
};
var calculate_total_amount = (frm) => {
	let total = frm.doc.services.reduce((total, item) => total + item.amount, 0);
	frm.set_value("total_amount", total);
};
