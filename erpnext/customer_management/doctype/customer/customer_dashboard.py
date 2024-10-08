from frappe import _


def get_data():
	return {
		"heatmap": True,
		"heatmap_message": _(
			"This is based on transactions against this Customer. See timeline below for details"
		),
		"fieldname": "customer",
		"non_standard_fieldnames": {
			"Payment Entry": "party",
			"Bank Account": "party",
			# "Quotation": "party_name",
			# "Opportunity": "party_name",
			# "Subscription": "party",
		},
		# "dynamic_links": {
		# 	"party_name": ["Customer", "quotation_to"],
		# 	"party": ["Customer", "party_type"],
		# },
		"transactions": [
			# {"label": _("Pre Sales"), "items": ["Opportunity", "Quotation"]},
			{"label": _("Orders"), "items": ["Sales Invoice"]},
			{"label": _("Payments"), "items": ["Payment Entry", "Bank Account"]},
			# {
				# "label": _("Support"),
				# "items": ["Issue", "Maintenance Visit", "Installation Note", "Warranty Claim"],
			# },
			# {"label": _("Projects"), "items": ["Project"]},
			# {"label": _("Pricing"), "items": ["Pricing Rule"]},
			# {"label": _("Subscriptions"), "items": ["Subscription"]},
		],
	}
