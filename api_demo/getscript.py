import requests
import frappe
import io
import string

#function for access token
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



#function for get item.
@frappe.whitelist()
def getitem_api():
    print("inside get")

    garageplug = frappe.get_doc("GaragePlug Settings")
    access_token = get_access_token(garageplug)

    getitem_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "x-location-id": garageplug.x_location_id,
            "x-api-key": garageplug.x_api_key,
        }
    
    getitem_url = "https://18vlz2k60m.execute-api.eu-west-1.amazonaws.com/dev/part?pageSize=<string>&fromDateTime=<string>&pageNumber=<string>&partId=<string>&toDateTime=<string>&filterBy=<string>"
    getitem_params = {
    "pageSize": "25",
    "fromDateTime": "2024-10-02 01:02:28",
    "pageNumber": "0",
    "toDateTime":"2024-10-02 23:02:28",
    "filterBy":"created_by"
    }

    getitem_response = requests.request("GET",getitem_url,headers= getitem_headers,params= getitem_params,data =None)

    if getitem_response.status_code == 200:
        print("Request was successful!")
        # print(getitem_response.json())
        items = frappe.get_all("Item", fields=["item_id","item_code"])
        print(items)

        garageplug_parts = getitem_response.json()
        item_ids = {item['item_id'] for item in items}
        print(item_ids)
    else:
        print(f"Request failed with status code {getitem_response.status_code}")
        print(getitem_response.text)
    
