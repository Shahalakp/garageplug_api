frappe.ui.form.on('Item Price', {
    after_save: function(frm) {
        // Execute the Python script when the item is saved
        frappe.call({
            method: 'api_demo.script.itemprice_api',
            args: {
                itemprice: frm.selected_doc.name // Pass the current Item name to the server-side method
            },
            async: true, // Ensures the call is asynchronous
            callback: function(r) {
                // console.log("ju\jjjjjjj")
                if (r.message) {
                    // Handle the response from the Python script
                    frappe.msgprint("Customer saved successfully.");
                }
            }
        });
    }
});