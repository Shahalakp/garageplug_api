# Copyright (c) 2024, shahala and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GaragePlugSettings(Document):
    pass

# def trigger_generate_token():
#     # Fetch the single record of Garageplug Settings
#     settings_doc = frappe.get_single('Garageplug Settings')
    
#     # Call the method associated with the Generate Token button
#     if settings_doc:
#         response = frappe.call('api_demo.script.get_access_token', name=settings_doc.name)
    
#     # if response.get('message'):
#     #         # Set the token in the 'token' field
#         settings_doc.token = response['message']
#         settings_doc.save()
#         frappe.msgprint(__('Token generated successfully.'))
#         frappe.msgprint(__('Failed to generate token.'))
    