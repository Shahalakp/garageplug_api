app_name = "api_demo"
app_title = "api-demo"
app_publisher = "shahala"
app_description = "demo for practicing api integration"
app_email = "shahalakp182@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/api_demo/css/api_demo.css"
# app_include_js = "/assets/api_demo/js/api_demo.js"

# include js, css files in header of web template
# web_include_css = "/assets/api_demo/css/api_demo.css"
# web_include_js = "/assets/api_demo/js/api_demo.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "api_demo/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views

doctype_js = {"Item" : "public/js/item.js",
              "Customer" : "public/js/customer.js",
              "Supplier" : "public/js/supplier.js",
              "Item Price" : "public/js/item_price.js",
              "Purchase Order" : "public/js/purchase_order.js",
              "Purchase Invoice" : "public/js/purchase_invoice.js",
              "Stock Entry": "public/js/stock_entry.js",
              "Customer Group": "public/js/customer_group.js"}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "api_demo/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "api_demo.utils.jinja_methods",
#	"filters": "api_demo.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "api_demo.install.before_install"
after_install = "api_demo.install.install.install"

# Uninstallation
# ------------

# before_uninstall = "api_demo.uninstall.before_uninstall"
# after_uninstall = "api_demo.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "api_demo.utils.before_app_install"
# after_app_install = "api_demo.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "api_demo.utils.before_app_uninstall"
# after_app_uninstall = "api_demo.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "api_demo.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

#doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }



# Scheduled Tasks
# ---------------

scheduler_events = {
    "all": [
            "api_demo.script.fetch_purchase_orders_from_garageplug",
            "api_demo.script.fetch_customer_from_garageplug"
        ]
    
}

# scheduler_events = {
#	"all": [
#		"api_demo.tasks.all"
#	],
#	"daily": [
#		"api_demo.tasks.daily"
#	],
#	"hourly": [
#		"api_demo.tasks.hourly"
#	],
#	"weekly": [
#		"api_demo.tasks.weekly"
#	],
#	"monthly": [
#		"api_demo.tasks.monthly"
#	],
# }
# scheduler_events = {
# 	"all": [
# 		"api_demo.api_demo.getscript.getitem_api"
# 	],
# }

# Testing
# -------

# before_tests = "api_demo.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "api_demo.event.get_events"
# }

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "api_demo.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["api_demo.utils.before_request"]
# after_request = ["api_demo.utils.after_request"]

# Job Events
# ----------
# before_job = ["api_demo.utils.before_job"]
# after_job = ["api_demo.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"api_demo.auth.validate"
# ]
