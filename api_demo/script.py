import requests
import frappe
from frappe.utils import now_datetime

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
        if item.slaes_taxes_and_charges_template:
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


# @frappe.whitelist()
# def getitem_api(**kwargs):
#     print("inside get")

#     garageplug = frappe.get_doc("GaragePlug Settings")
#     access_token = get_access_token(garageplug)