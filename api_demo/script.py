import requests
import frappe
from frappe.utils import now_datetime
from frappe import _
from datetime import datetime, timedelta, timezone

@frappe.whitelist()
def get_access_token(garageplug):
    print("inside token function")
    url = "https://gp-test-api.auth.eu-west-1.amazoncognito.com/oauth2/token"
    auth =( garageplug.client_id, garageplug.client_secret)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        'client_id': garageplug.client_id,
        'grant_type': 'client_credentials'
    }
   
    response = requests.post(url, auth=auth, headers=headers, data=body)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("Responce:",response.text)
        raise Exception("Failed to get access token. Status code: {}".format(response.status_code))
        
# Function to get the access token
@frappe.whitelist()
def item_api(**kwargs):
    print("inside function")    
    garageplug = frappe.get_doc('GaragePlug Settings')
    access_token = get_access_token(garageplug)
# To send service data 
    item_new = frappe.get_doc('Item', kwargs.get('item'))

    print(item_new.item_name)

# To access item tax
    if item_new.taxes:
        for tax in item_new.taxes:
            tax_template = frappe.get_doc("Item Tax Template", tax.item_tax_template)
            title = tax_template.title
            for detail in tax_template.taxes:
                rate = detail.tax_rate
    else:
        title = ""
        rate = ""
    
    print(title,rate)
        # rate.append(tax_template.)
# To access purchase tax details

    if item_new.purchase_tax_name:
        
        purchase_template = frappe.get_doc("Purchase Taxes and Charges Template",item_new.purchase_tax_name)
        p_title = purchase_template.title
        for detail in purchase_template.taxes:
            p_rate = detail.rate
    else:
        p_rate = ""
        p_title = ""   
    print(p_title," and ",p_rate)


    # to get the year from end_of_life
    date_with_year = item_new.end_of_life
    if date_with_year:
        str_date_with_year = str(date_with_year)
        exp_year = str_date_with_year[:4]

    if item_new.service_item:
        print(item_new.service_item)
        url = "https://devintegration.garageplug.com/service"
        headers = {
                'x-api-key': garageplug.x_api_key,
                'x-location-id': garageplug.x_location_id,
                'Content-Type': 'application/json',
                'Accept': 'application/problem+json',
                'Authorization': f'Bearer {access_token}'
            }
   

        body = [
            {
                "service_name":  item_new.item_name,
                "service_number": item_new.item_code,
                "description":  item_new.description,
                "sales_tax_name": title,
                "sales_tax_percentage": rate,
                "sales_price_without_tax": item_new.standard_rate,
                "component_category": item_new.component_category,
                "benchmark_hours": item_new.benchmark_hours,
                "external_id": ""
            }
            ]

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            print("Item data sent successfully.")
            print("Response:", response.text)
            res = response.json()
            print(res[0]["service_id"])
            item_new.item_id = res[0]["service_id"]
            item_new.save()

        else:
            print("Failed to send item data. Status code:", response.status_code)
            print("Response:", response.text)

    elif item_new.opening_stock:

        
        item_default = frappe.get_doc("Item Default",item_new.item_defaults)
        warehouse = frappe.get_doc("Warehouse",item_default.default_warehouse)
        

        url = "https://devintegration.garageplug.com/part_with_inventory"
        headers = {
                'x-api-key': garageplug.x_api_key,
                'x-location-id': garageplug.x_location_id,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        body = [
        {
        "part_name": item_new.item_name,
        "part_number": item_new.item_code,
        "type": item_new.item_group,
        "pattern": item_new.pattern,
        "sku": item_new.sku,
        "size": item_new.size,
        "purchase_price_without_tax": item_new.valuation_rate,
        "purchase_tax_name": p_title,
        "purchase_tax_percentage": p_rate,
        "description": item_new.description,
        "part_barcode": item_new.barcodes if isinstance(item_new.barcodes, str) else item_new.barcodes[0] if item_new.barcodes else '',
        "manufacturing_year": item_new.manufacturing_year,
        "component_category": item_new.component_category,
        "expire_year": exp_year,
        "sales_price_without_tax":  item_new.standard_rate,
        "sales_tax_name": title,
        "sales_tax_percentage": rate,
        "unit_of_measure": item_new.stock_uom,
        "manufacturer": item_new.manufacturer,
        "external_id": item_new.external_id,
        "inventory_request": {
        "current_stock": item_new.opening_stock,
        "max_stock": item_new.max_stock,
        "min_stock": item_new.safety_stock,
        "rack_id": warehouse.rack_id
        }
        },
   
        ] 
        response = requests.post(url, headers=headers, json=body) 

        if response.status_code == 200:
            print("Item data sent successfully.")
            print("Response:", response.text)
            res = response.json()
            print(res[0]["part_id"])
            item_new.item_id = res[0]["part_id"]
            item_new.save()

        else:
            print("Failed to send item data. Status code:", response.status_code)
            print("Response:", response.text) 


# To send item data
    else:

        url = "https://devintegration.garageplug.com/part"
        headers = {
                'x-api-key': garageplug.x_api_key,
                'x-location-id': garageplug.x_location_id,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
    
            

        body = [
            {
            "part_name": item_new.item_name,
            "part_number":  item_new.item_code,
            "type":      
            item_new.item_group
            ,
            "unit_of_measure": item_new.stock_uom,
            "manufacturer": item_new.manufacturer,
            "expire_year": exp_year,
            "sales_price_without_tax": item_new.standard_rate,
            "sales_tax_name": title,
            "sales_tax_percentage": rate,
            "manufacturing_year": item_new.manufacturing_year,
            "component_category": item_new.component_category,
            "description": item_new.description,
            "part_barcode": item_new.barcodes if isinstance(item_new.barcodes, str) else item_new.barcodes[0] if item_new.barcodes else '',
            "purchase_price_without_tax": item_new.valuation_rate,
            "purchase_tax_name": p_title,
            "purchase_tax_percentage": p_rate,
            "size": item_new.size,
            "sku":item_new.sku,
            "pattern": item_new.pattern,
            "external_id": item_new.external_id
            }
            ]

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            print("Item data sent successfully.")
            print("Response:", response.text)
            res = response.json()
            print(res[0]["part_id"])
            item_new.item_id = res[0]["part_id"]
            item_new.save()

        else:
            print("Failed to send item data. Status code:", response.status_code)
            print("Response:", response.text)
        #   print(e)

#Sending customer data
@frappe.whitelist()
def customer_api(**kwargs):
    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)
    print("Inside func")

    # to get the year from end_of_life
    # date_with_year = item_new[0]['end_of_life']
    # str_date_with_year = str(date_with_year)
    # exp_year = str_date_with_year[:4]

    cust_new = frappe.get_doc("Customer", kwargs.get("cust"))
    # print(cust_new.customer_primary_contact)

    customer_url = "https://devintegration.garageplug.com/customer"

    # Taking contact details
    primary = None
    secondary_phone = None

    contact = frappe.get_doc("Contact", cust_new.customer_primary_contact)
    ph_no = contact.phone_nos
    for phone in ph_no:
        if phone.is_primary_phone or phone.is_primary_mobile_no:
            primary = phone.phone
            # type(primary)

        else:
            secondary_phone = phone.phone

    # Customer address
    addr = frappe.get_doc("Address", cust_new.customer_primary_address)

    customer_body = [
        {
            "customer_category": cust_new.invoice_type,
            "email": contact.email_id,
            "mobile_number": primary if primary else secondary_phone,
            "name": cust_new.customer_name,
            "external_id": "",
            "secondary_phone": secondary_phone,
            "tax_number": cust_new.tax_id,
            "group_tax_number": cust_new.group_tax_number,
            "occupation": contact.designation,
            "organisation": contact.company_name,
            "additional_number": "",
            "customer_group_name": cust_new.customer_group,
            "address": {
                "address_line1": addr.address_line1,
                "address_type": addr.address_type,
                "attributes": addr.attributes,
                "phone": addr.phone,
                "geo_coordinates": addr.geo_coordinates,
                "map_url": addr.map_url,
                "state_code": addr.state_code,
                "address_line2": addr.address_line2,
                "pincode": addr.pincode,
                "city": addr.city,
                "state": addr.state,
                "street": cust_new.street_name,
                "country_code": addr.country_code,
                "building_number": cust_new.building_number,
                "neighbourhood": addr.neighbourhood,
                "additional_street": cust_new.additional_street_name,
            },
        }
    ]
    # Add the access token to the headers
    customer_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-location-id": garageplug.x_location_id,
        "x-api-key": garageplug.x_api_key,
    }

    # Send data to garageplug
    customer_response = requests.request(
        "POST", customer_url, headers=customer_headers, json=customer_body
    )
    if customer_response.status_code == 200:
        print("data sent successfully")
        print("Response: ", customer_response.text)
        res = customer_response.json()
        print(res[0]["customer_id"])
        cust_new.customer_id = res[0]["customer_id"]
        cust_new.save()
    else:
        print("Error sending data.Status code: ", customer_response.status_code)
        print("RESPONSE: ", customer_response.text)
        # frappe.msg("Please make necessary changes and resubmit. Contact system admin for more details")
        # exit()






#sending vendor data
@frappe.whitelist()
def vendor_api(**kwargs):
    garageplug = frappe.get_doc("GaragePlug Settings")
    print(garageplug)
    access_token = get_access_token(garageplug)
    print("Inside func")

    # to get the year from end_of_life
    # date_with_year = item_new[0]['end_of_life']
    # str_date_with_year = str(date_with_year)
    # exp_year = str_date_with_year[:4]
    vendor_new = frappe.get_doc("Supplier", kwargs.get("supp"))

    vendor_url = "https://devintegration.garageplug.com/vendor"

    addr = frappe.get_doc("Address", vendor_new.supplier_primary_address)

    vendor_body = [
        {
            "phone": addr.phone,
            "vendor_name": vendor_new.supplier_name,
            "tax_number": vendor_new.tax_id,
            "address": vendor_new.supplier_primary_address,
            "email": vendor_new.email_id,
            "pin": addr.pincode,
            "state": addr.state,
            "city": addr.city,
            "building_number": vendor_new.building_number,
            "street": vendor_new.street_name,
            "group_tax_number": vendor_new.group_tax_number,
            "additional_number": "",
            "neighbourhood": "",
            "additional_street": vendor_new.additional_street_name,
            "country_code": addr.country_code,
            "external_id": "",
            "vendor_code": vendor_new.supplier_code
        }
    ]
    # Add the access token to the headers
    vendor_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-location-id": garageplug.x_location_id,
        "x-api-key": garageplug.x_api_key,
    }

    # Send data to garageplug
    vendor_response = requests.request(
        "POST", vendor_url, headers=vendor_headers, json=vendor_body
    )

    if vendor_response.status_code == 200:
        print("data sent successfully")
        print("Response: ", vendor_response.text)
        res = vendor_response.json()
        vendor_new.supplier_id = res[0]["garage_vendor_id"]
        vendor_new.save()
    else:
        print(
            "Error sending data.Status code: ",
            vendor_response.status_code,
            vendor_response.text,
        )
        # frappe.msg("Please make necessary changes and resubmit. Contact system admin for more details")
        # exit()




#For Customer price part and vendor price part
@frappe.whitelist()
def itemprice_api(**kwargs):
    print("inside function")

    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)

    itemprice_new = frappe.get_doc("Item Price", kwargs.get("itemprice"))

    # For customer item price
    if itemprice_new.price_list == "Standard Selling":

        customer = frappe.get_doc("Customer", itemprice_new.customer)
        item = frappe.get_doc("Item",itemprice_new.item_code)
        

        itemprice_url = "https://devintegration.garageplug.com/customer_price_part"

        itemprice_body = {
            "customer_id": customer.customer_id,
            "part_price_list": [
                {
                    "part_id": item.item_id,
                    "price": itemprice_new.price_list_rate,
                }
            ],
        }
        # Add the access token to the headers
        itemprice_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/problem+json",
            "x-location-id": garageplug.x_location_id,
            "x-api-key": garageplug.x_api_key,
        }

        # Send data to garageplug
        itemprice_response = requests.request(
            "POST", itemprice_url, headers=itemprice_headers, json=itemprice_body
        )
        if itemprice_response.status_code == 200:
            print("data sent successfully")
            print("Response: ", itemprice_response.text)
        else:
            print(
                "Failed to send item data. Status code:", itemprice_response.status_code
            )
            print("Response:", itemprice_response.text)
    # For vendor price list
    elif itemprice_new.price_list == "Standard Buying":

        supplier = frappe.get_doc("Supplier", itemprice_new.supplier)
        item = frappe.get_doc("Item",itemprice_new.item_code)
        print(item.item_id)
        itemprice_url = "https://devintegration.garageplug.com/vendor_price_part"

        itemprice_body = {
            "vendor_id": supplier.supplier_id,
            "vendor_price_lists": [
                {
                    "part_id": item.item_id,
                    "purchase_price": itemprice_new.price_list_rate,
                }
            ],
        }
        # Add the access token to the headers
        itemprice_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/problem+json",
            "x-location-id": garageplug.x_location_id,
            "x-api-key": garageplug.x_api_key,
        }

        # Send data to garageplug
        itemprice_response = requests.request(
            "POST", itemprice_url, headers=itemprice_headers, json=itemprice_body
        )
        if itemprice_response.status_code == 200:
            print("data sent successfully")
            print("Response: ", itemprice_response.text)
        else:
            print(
                "Failed to send item data. Status code:", itemprice_response.status_code
            )
            print("Response:", itemprice_response.text)
    # customer service price part
    else:
        customer = frappe.get_doc("Customer", itemprice_new.customer)
        item = frappe.get_doc("Item",itemprice_new.item_code)
        

        itemprice_url = "https://devintegration.garageplug.com/customer_price_service"


        
        itemprice_body = {
            "customer_id": customer.customer_id,
            "service_price_list": [
                {
                    "price": itemprice_new.price_list_rate,
                    "service_id": item.item_id,
                }
            ],
        }
        # Add the access token to the headers
        itemprice_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-location-id": garageplug.x_location_id,
            "x-api-key": garageplug.x_api_key,
        }

        # Send data to garageplug
        itemprice_response = requests.request(
            "POST", itemprice_url, headers=itemprice_headers, json=itemprice_body
        )
        if itemprice_response.status_code == 200:
            print("data sent successfully")
            print("Response: ", itemprice_response.text)
        else:
            print(
                "Failed to send item data. Status code:", itemprice_response.status_code
            )
            print("Response:", itemprice_response.text)
        

#For Purchase Order Post
@frappe.whitelist()
def purchaseorder_api(**kwargs):
    print("inside function")

    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)

    po_new = frappe.get_doc("Purchase Order", kwargs.get("po"))

    po_url = "https://devintegration.garageplug.com/purchase_order"

    if po_new.taxes_and_charges:
        purchase_template = frappe.get_doc("Purchase Taxes and Charges Template",po_new.taxes_and_charges)
        p_title = purchase_template.title
        for detail in purchase_template.taxes:
            p_rate = detail.rate
    else:
        p_rate = ""
        p_title = "" 


    mapped_items = []
    for item in po_new.items: 
        item_now = frappe.get_doc("Item", item.item_code)

        mapped_item = {
        "part_id": item_now.item_id,
        "purchase_price_without_tax": item.rate,
        "quantity": item.qty,
        "purchase_tax_name": p_title,
        "purchase_tax_percentage": p_rate,
        "external_id": "",
        "private_note": item.description,
        "unit_category": "",
        "unit_of_measure": item.uom,
        }
    mapped_items.append(mapped_item)

    # stat = []
    # for item in po_new.items:
    #     stat.append("APPROVED")
     
    supp = frappe.get_doc("Supplier", po_new.supplier)
    supp_id = supp.supplier_id

    po_datetime = now_datetime()

    po_datetime_str = po_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    
    if po_new.status == "To Receive and Bill" or po_new.status == "Completed":
        stat = "APPROVED"
    
    po_body = {
    "items": mapped_items,
    "status": stat,
    "vendor_id": supp_id,
    "po_date": po_datetime_str,
    "order_id": "",
    "external_purchase_order_id": "",
    "comment": po_new.comment
    }

    po_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-location-id": garageplug.x_location_id,
            "x-api-key": garageplug.x_api_key,
        }

    po_response = requests.request(
        "POST", po_url, headers=po_headers, json=po_body
    )

    if po_response.status_code == 200:
        print("data sent successfully")
        print("Response: ", po_response.text)
        res = po_response.json()

        if "purchase_order_id" in res:
        # Set the purchase_order_id in the ERPNext PO document
            po_new.db_set("po_id", res["purchase_order_id"])
            print(f"Purchase Order ID from GaragePlug has been set to {res['purchase_order_id']}")
        else:
            print("Key 'purchase_order_id' not found in the response:", res)
    else:
        print(
            "Error sending data.Status code: ",
            po_response.status_code,
            po_response.text,
        )


#For Purchase Order Post
@frappe.whitelist()
def purchaseinvoice_api(**kwargs):
    print("inside function")

    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)

    pi_new = frappe.get_doc("Purchase Invoice", kwargs.get("pi"))

    pi_url = "https://devintegration.garageplug.com/perform_stock_in"

    if pi_new.taxes_and_charges:
        purchase_template = frappe.get_doc("Purchase Taxes and Charges Template",pi_new.taxes_and_charges)
        p_title = purchase_template.title
        for detail in purchase_template.taxes:
            p_rate = detail.rate
    else:
        p_rate = ""
        p_title = "" 
    
    # if pi_new.purchase_order:
    #     # Fetch the linked Purchase Order document
    #     po = frappe.get_doc("Purchase Order", pi_new.purchase_order)
    #     poid = po.po_id
    # else:
    #     poid = ""
    poid = ""
    for item in pi_new.items:
        if item.purchase_order:
            po = frappe.get_doc("Purchase Order", item.purchase_order)
            poid = po.po_id
            break 


    mapped_items = []
    for item in pi_new.items: 
        item_now = frappe.get_doc("Item", item.item_code)
        if item.sales_taxes_and_charges_template:
            sales_template = frappe.get_doc("Sales Taxes and Charges Template",item.sales_taxes_and_charges_template)
            s_title = sales_template.title
            for detail in sales_template.taxes:
                s_rate = detail.rate
        else:
            s_rate = ""
            s_title = "" 
        mapped_item = {
            "part_id": item_now.item_id,
            "purchase_price_without_tax": item.rate,
            "quantity": item.qty,
            "purchase_tax_name": p_title,
            "purchase_tax_percentage": p_rate,
            "sales_price_without_tax": item.sales_price_without_tax,
            "sales_tax_name": s_title,
            "sales_tax_percentage": s_rate,
            "external_id": item_now.external_id,
            "unit_category": "",
            "unit_of_measure": item.uom
        }
        mapped_items.append(mapped_item)

    supp=frappe.get_doc("Supplier", pi_new.supplier)
    
    pi_datetime = now_datetime()
    pi_datetime_str = pi_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    # paymentmode = []
    # paymentmode.append(pi_new.mode_of_payment)
    
    pr_body = {
    "purchase_items": mapped_items,
    "vendor_id": supp.supplier_id,
    "purchase_date": pi_datetime_str,
    "external_id": pi_new.external_id,
    "total_tax_amount": pi_new.total_taxes_and_charges,
    "total_amount": pi_new.grand_total,
    "payment_reference_number": pi_new.purchase_referance_number,
    # "externalpurchase_order_id": "",
    "purchase_order_id": poid,
    "comments": pi_new.comment,
    "payment_request": {
        "payment_mode": pi_new.mode_of_payment,
        "paid_amount": pi_new.paid_amount
    }
    }

    pr_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-location-id": garageplug.x_location_id,
            "x-api-key": garageplug.x_api_key,
        }

    pi_response = requests.request(
        "POST", pi_url, headers=pr_headers, json=pr_body
    )

    try:
    
        if pi_response.status_code == 200:
            print("data sent successfully")
            print("Response:", pi_response.text)
            res = pi_response.json()
        else:
            print("Failed to send item data. Status code:", pi_response.status_code)
            print("Response:", pi_response.text)
    except Exception as e:
        print("An error occurred:", e)


@frappe.whitelist()
def stockentry_api(**kwargs):
    print("inside function")

    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)

    se_new = frappe.get_doc("Stock Entry", kwargs.get("se"))

    entry_type = se_new.stock_entry_type
    first_invitems=[]
    notfirst_invitems=[]
    bins = frappe.get_all("Bin", fields=["item_code", "actual_qty"])
    if entry_type == "Material Receipt":
        for item in se_new.items:
            for bin in bins:
                 if bin.item_code == item.item_code:
                    if bin.actual_quantity == 0:
                      first_invitems.append(item.item_code)
            
                    else:
                        notfirst_invitems.append(item.item_code)
        print(first_invitems)
        print(notfirst_invitems)
        



    
    # mapped_items=[]
    # if entry_type == "Material Issue" or entry_type == "Material Receipt":
    #     for item in se_new.items: 
    #         item_now = frappe.get_doc("Item", item.item_code)
    #         item_default = frappe.get_doc("Item Default",item_now.item_defaults)
    #         warehouse = frappe.get_doc("Warehouse",item_default.default_warehouse)

    #         if entry_type == "Material Issue":
    #             qty = -abs(item.qty)
    #         else:
    #             qty = item.qty

    #         mapped_item = {
    #             "current_stock": qty,
    #             "max_stock": item_now.max_stock,
    #             "min_stock": item_now.safety_stock,
    #             "part_id": item_now.item_id,
    #             "rack_id": warehouse.rack_id,
    #             "unit_category": "",
    #             "unit_of_measure": item.uom
    #         }
    #         mapped_items.append(mapped_item)
    # else:
    #     print("No data to send.")
    


    # se_url = "https://devintegration.garageplug.com/inventory"

    # se_body = mapped_items
    

    # se_headers = {
    #         "Authorization": f"Bearer {access_token}",
    #         "Content-Type": "application/json",
    #         "Accept": "application/json",
    #         "x-location-id": garageplug.x_location_id,
    #         "x-api-key": garageplug.x_api_key,
    #     }

    # se_response = requests.request(
    #     "POST", se_url, headers=se_headers, json=se_body
    # )

    # try:
    
    #     if se_response.status_code == 200:
    #         print("data sent successfully")
    #         print("Response:", se_response.text)
    #         # res = se_response.json()
    #     else:
    #         print("Failed to send item data. Status code:", se_response.status_code)
    #         print("Response:", se_response.text)
    # except Exception as e:
    #     print("An error occurred:", e)


@frappe.whitelist()
def customergroup_api(**kwargs):
    print("inside function")

    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)

    cg_new = frappe.get_doc("Customer Group", kwargs.get("cg"))
    mapped_items = []
    if cg_new.service_group:
        print("service group")
    else:
        cg_url = "https://devintegration.garageplug.com/customer_group_price_part/external_id"

        for item in cg_new.table_rmmj: 
            mapped_item = {
                "external_part_id": item.data_jakr,
                "price": item.rate
            }
            mapped_items.append(mapped_item)

        cg_body = {
            "customer_group_name": cg_new.customer_group_name,
            "part_price_list": mapped_items
        }

        cg_headers = {
            "Authorization": f"Bearer {access_token}",
            "x-location-id": garageplug.x_location_id,
            "x-api-key": garageplug.x_api_key,
        }

        cg_response = requests.request(
            "POST", cg_url, headers=cg_headers, json=cg_body
        )

        try:
        
            if cg_response.status_code == 200:
                print("data sent successfully")
                print("Response:", cg_response.text)
                # res = se_response.json()
            else:
                print("Failed to send item data. Status code:", cg_response.status_code)
                print("Response:", cg_response.text)
        except Exception as e:
            print("An error occurred:", e)






@frappe.whitelist()
def fetch_purchase_orders_from_garageplug():
    print("Starting GET request for Purchase Orders.")

    # Get settings from the GaragePlug Settings doctype
    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)  # Assume this function exists
    print("Access toked granted.")
    # Define GET request parameters
    params = {
        "pageSize": "10",
        # "fromDateTime": "2024-12-01T00:00:00",  # Adjust dynamically
        # "toDateTime": now_datetime().strftime('%Y-%m-%dT%H:%M:%S'),
        "pageNumber": "1",
        # "filterBy": "status:open",
    }
    print("params set")
    # Define headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-location-id": garageplug.x_location_id,
        "x-api-key": garageplug.x_api_key,
    }
    print("headers set")
    # Make the GET request
    url="https://devintegration.garageplug.com/purchase_order"
    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print("GET request successful. Response:", response.json())
            # Process the response (e.g., update Frappe documents)
            process_purchase_orders(response.json())
        else:
            frappe.log_error(
                _("Failed to fetch purchase orders"),
                f"Status: {response.status_code}, Response: {response.text}"
            )
    except Exception as e:
        frappe.log_error(_("Error in GET request"), str(e))


def process_purchase_orders(response_data):
    """
    Process the GaragePlug response data and create or update ERPNext Purchase Orders.
    
    Args:
        response_data (list): List of purchase orders from GaragePlug.
    """
    for po in response_data:
        try:
            # Extract Purchase Order details
            purchase_order_id = po.get("purchase_order_id")
            po_date = po.get("po_date")
            vendor_id = po.get("vendor_id")
            total_amount = po.get("total_amount")
            comment = po.get("comment")
            status = po.get("status")  # Default to "Draft" if not provided
            vendor_invoice_link = po.get("vendor_invoice_link", "")
            created_at = po.get("created_at")
            updated_at = po.get("updated_at")
            external_po_id = po.get("external_purchase_order_id")

            # Get or create Supplier based on vendor_id
            # supplier_name = f"Supplier-{vendor_id}"  # Example supplier naming convention
            # supplier = frappe.db.get_value("Supplier", {"supplier_id": vendor_id}, "name")
            # if not supplier:
            #     supplier_doc = frappe.get_doc({
            #         "doctype": "Supplier",
            #         "supplier_name": supplier_name,
            #         "supplier_id": vendor_id
            #     })
            #     supplier_doc.insert(ignore_permissions=True)
            #     supplier = supplier_doc.name
            stat =""
            if status == "Created":
                stat=="To Receive and Bill"
            elif status == "Rejected":
                stat == "Cancelled"
            

            supplier = frappe.get_doc("Supplier", {"supplier_id": vendor_id})
            if supplier:
                po_doc = frappe.get_doc({
                    "doctype": "Purchase Order",
                    "po_id": purchase_order_id,
                    "supplier": supplier,
                    "transaction_date": created_at,
                    "status": stat,
                    "total": total_amount,
                    "comment": comment,
                    "schedule_date" : po_date,
                    # "vendor_invoice_link": vendor_invoice_link,
                    # "external_purchase_order_id": external_po_id,
                    # "created_at": created_at,
                    # "updated_at": updated_at
                })
                po_doc.flags.ignore_mandatory = True  # Bypass mandatory fields during insert

            # Map Purchase Items
            po_doc.items = []  # Clear existing items if updating
            for item in po.get("purchase_items", []):
                po_doc.append("items", {
                    "item_code": item.get("part_number", ""),
                    "item_name": item.get("part_name", ""),
                    "rate": item.get("purchase_price_without_tax", 0),
                    "qty": item.get("quantity", 0),
                    # "taxes_and_charges": item.get("purchase_tax_name", ""),
                    # "description": item.get("component_category", ""),
                    "uom": item.get("unit_of_measure", "")
                })

            # Save the Purchase Order
            po_doc.save(ignore_permissions=True)
            frappe.db.commit()
            print(f"Processed Purchase Order: {po_doc.name}")

        except Exception as e:
            frappe.log_error(f"Error processing Purchase Order {po.get('purchase_order_id')}: {str(e)}")





@frappe.whitelist()
def fetch_customer_from_garageplug():
    print("Starting GET request for customer.")

    # Get settings from the GaragePlug Settings doctype
    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)  # Ensure this function works
    print("Access token granted.")

    # Define GET request parameters
    to_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    from_datetime = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')

    params = {
        # "customerCategory": "B2C",
        "pageSize": "20",
        "pageNumber": "1",
        # "fromDateTime": from_datetime,
        # "toDateTime": to_datetime,
        # "filterBy": ""
    }
    print("Params set:", params)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-location-id": garageplug.x_location_id,
        "x-api-key": garageplug.x_api_key,
        "Accept": "application/json",
    }
    print("Headers set:", headers)

    url = "https://devintegration.garageplug.com/customer"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)

        # Parse and process the response
        customers = response.json()
        if not customers:
            print("No customers found in the response.")
            return

        print("Fetched customers:", customers)

        for customer_data in customers:
            customer_id = customer_data.get('customer_id')
            customer_name = customer_data.get('name')
            mobile_number = customer_data.get('mobile_number')
            secondary_phone = customer_data.get('secondary_phone')
            email = customer_data.get('email', '')
            address = customer_data.get('address', {})
         
    except requests.exceptions.RequestException as e:
        error_message = f"Error syncing customers: {str(e)}"
        print(error_message)
        frappe.log_error(error_message[:140], "Customer Sync Error")  # Truncate if necessary

def process_customer(customer):
    """
    Example function to process individual customers.
    """
    print(f"Processing customer: {customer}")
    # Implement customer synchronization logic here.


# def sync_customers():
#     GP_API_URL = "https://18vlz2k60m.execute-api.eu-west-1.amazonaws.com/dev/customer"
#     GP_HEADERS = {
#     "Authorization": "Bearer YOUR_GARAGEPLUG_TOKEN",
#     "Content-Type": "application/json"
# }
#     """Fetch customers from GaragePlug and sync with ERPNext."""
    

#         # Process customers
#     for customer in customers:
#             # Check if customer exists in ERPNext
#         existing = frappe.get_all("Customer", filters={"email": customer.get("email")}, limit=1)
#             if existing:
#                 # Update existing customer
#                 frappe.db.set_value("Customer", existing[0].name, {
#                     "customer_name": customer.get("name"),
#                     "mobile_no": customer.get("mobile_number"),
#                     "tax_id": customer.get("tax_number"),
#                 })
#             else:
#                 # Create new customer
#                 doc = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": customer.get("name"),
#                     "email": customer.get("email"),
#                     "mobile_no": customer.get("mobile_number"),
#                     "tax_id": customer.get("tax_number"),
#                     "customer_group": customer.get("customer_group_name", "Individual"),
#                     "territory": "All Territories",
#                 })
#                 doc.insert(ignore_permissions=True)

#         frappe.db.commit()
#         frappe.log("Customer sync completed successfully.")
    

