import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import json
import os

def install():
    make_custom_fields()

def make_custom_fields():

	custom_fields = {
		"Purchase Order": [
            {
            "doctype":"Purchase Order",
            "insert_after": "aming_series",
            "depends_on": "doc.docstatus == 1\n",
            "fieldname": "po_id",
            "fieldtype": "Data",
            "label": "PO ID",
            "oldfieldname": "naming_series",
            "oldfieldtype": "Select",
            "read_only": 1,
            "read_only_depends_on": "\n"

            },
            {
            "doctype":"Purchase Order",
            "insert_after": "ref_sq",
            "fieldname": "comment",
            "fieldtype": "Data",
            "label": "Comment",
            "oldfieldname": "ref_sq",
            "oldfieldtype": "Data"
            }
            ],
		"Item": [
			{
                "doctype":"Item", 
                "fieldname": "item_id",
                "fieldtype": "Data",
                "label": "Item ID",
                "read_only": 1,
                "insert_after":"naming_series"
            },
			{
            "doctype":"Item",
            "fieldname": "size",
            "fieldtype": "Data",
            "label": "Size",
            "mandatory_depends_on": "eval:doc.item_group == \"TYRE\"",
            "insert_after":"item_group"
            },
            {
            "doctype":"Item",
            "fieldname": "pattern",
            "fieldtype": "Data",
            "label": "Pattern",
            "mandatory_depends_on": "eval:doc.item_group == \"TYRE\"",
            "insert_after":"size"
            },
            {
            "doctype":"Item",
            "fieldname": "manufacturing_year",
            "fieldtype": "Data",
            "label": "Manufacturing Year",
            "insert_after":"pattern"
            },
            {
            "doctype":"Item",
            "fieldname": "sku",
            "fieldtype": "Link",
            "label": "SKU",
            "options": "UOM",
            "insert_after":"stock_uom"
            },
            {
            "doctype":"Item",
            "fieldname": "component_category",
            "fieldtype": "Link",
            "label": "Component Category",
            "options": "UOM",
            "insert_after":"sku"
            },
            {
            "doctype":"Item",
            "fieldname": "benchmark_hours",
            "fieldtype": "Duration",
            "hide_days": 1,
            "hide_seconds": 1,
            "label": "Benchmark Hours",
            "insert_after":"component_category"
            },
            {
            "doctype":"Item",
            "fieldname": "manufacturer",
            "fieldtype": "Link",
            "label": "Manufacturer",
            "options": "Manufacturer",
            "insert_after":"image"
            },
            {
            "doctype":"Item",
            "default": "0",
            "fieldname": "service_item",
            "fieldtype": "Check",
            "label": "Service Item",
            "insert_after":"has_variants"
            },
            {
            "doctype":"Item",
            "fieldname": "custom_section_break_xk0gp",
            "fieldtype": "Section Break",
            "insert_after":"taxes"
            },
            {
            "doctype":"Item",
            "fieldname": "purchase_tax_name",
            "fieldtype": "Link",
            "label": "Purchase Tax Name",
            "options": "Purchase Taxes and Charges Template",
            "insert_after":"custom_section_break_xk0gp"
            },
            {
            "doctype":"Item",
            "fieldname": "external_id",
            "fieldtype": "Data",
            "label": "External ID",
            "insert_after":"expiry_year"
            },

		],
		"Supplier":[
            {
                "doctype": "Supplier",
                "fieldname": "supplier_id",
                "fieldtype": "Data",
                "label": "Supplier ID",
                "read_only": 1,
                "insert_after":"naming_series"
            },
            {
                "doctype": "Supplier",
                "fieldname": "group_tax_number",
                "fieldtype": "Data",
                "label": "Group Tax Number",
                "insert_after":"tax_id"
            },
            {
                "doctype": "Supplier",
                "fieldname": "building_number",
                "fieldtype": "Data",
                "label": "Building Number",
                "insert_after":"primary_address"
            },
            {
                "doctype": "Supplier",
                "fieldname": "street_name",
                "fieldtype": "Data",
                "label": "Street Name",
                "insert_after":"building_number"

            },
            {
                "doctype": "Supplier",
                "fieldname": "additional_street_name",
                "fieldtype": "Data",
                "label": "Additional Street Name",
                "insert_after":"street_name"
                
            }
        ],
        "Customer":[
            {
                "doctype":"Customer",
                "fieldname": "customer_id",
                "fieldtype": "Data",
                "label": "Customer ID",
                "read_only": 1,
                "insert_after":"sbasic_info"
            },
            {
                "doctype":"Customer",
                "fieldname": "invoice_type",
                "fieldtype": "Select",
                "label": "Invoice Type",
                "options": "B2B\nB2C",
                "insert_after":"customer_type"
            },
            {
                "doctype":"Customer",
                "fieldname": "group_tax_number",
                "fieldtype": "Data",
                "label": "Group Tax Number",
                "insert_after":"tax_id"
            }
        ],

        "Address": [
            {
                "doctype": "Address",
                "fieldname": "address_line1_arabic",
                "fieldtype": "Data",
                "label": "Address Line 1- Arabic",
                "insert_after":"address_line_1"
            },
            {
                "doctype": "Address",
                "fieldname": "address_line2_arabic",
                "fieldtype": "Data",
                "label": "Address Line 2- Arabic",
                "insert_after":"address_line_2"
            },
            {
                "doctype": "Address",
                "fieldname": "city_arabic",
                "fieldtype": "Data",
                "label": "City- Arabic",
                "insert_after":"city"
            },
            {
                "doctype": "Address",
                "fieldname": "state_code",
                "fieldtype": "Data",
                "label": "State Code",
                "insert_after":"state"
            },
            {
                "doctype": "Address",
                "fieldname": "country_arabic",
                "fieldtype": "Data",
                "label": "Country- Arabic",
                "insert_after":"country"
            },
            {
                "doctype": "Address",
                "fieldname": "map_url",
                "fieldtype": "Data",
                "label": "Map URL",
                "options": "URL",
                "insert_after":"geo_coordinates"
            },
            {
                "doctype": "Address",
                "fieldname": "attributes",
                "fieldtype": "Data",
                "label": "Attributes",
                "insert_after":"address_line_2_arabic"
            },
            {
                "doctype": "Address",
                "fieldname": "geo_coordinates",
                "fieldtype": "Data",
                "label": "Geo-coordinates",
                "insert_after":"attributes"
            },
            {
                "doctype": "Address",
                "fieldname": "country_code",
                "fieldtype": "Data",
                "label": "Country Code",
                "insert_after":"country_arabic"
            },
            {
            "doctype": "Address",
            "fieldname": "neighbourhood",
            "fieldtype": "Data",
            "label": "Neighbourhood",
            "insert_after":"map_url"
            }      
        ],

        "Purchase Invoice":[
            {                  
            "doctype": "Purchase Invoice",
            "insert_after": "use_transaction_date_exchange_rate",
            "fieldname": "external_id",
            "fieldtype": "Data",
            "label": "External Id"   
            },
            {
            "doctype": "Purchase Invoice",
            "insert_after": "comment",
            "fieldname": "purchase_referance_number",
            "fieldtype": "Data",
            "label": "Purchase Referance Number"
            },
            {
            "doctype": "Purchase Invoice",
            "insert_after": "external_id",
            "fieldname": "comment",
            "fieldtype": "Long Text",
            "label": "Comment"
            }
        ]
    }

	create_custom_fields(custom_fields, ignore_validate=True, update=True)