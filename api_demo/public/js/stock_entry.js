frappe.ui.form.on('Stock Entry', {
    on_submit: function(frm) {  // Use on_submit instead of after_save
        frappe.call({
            method: 'api_demo.script.stockentry_api',  // Ensure this is the correct path to your Python method
            args: {
                se: frm.selected_doc.name  // Correctly pass the stock entry name
            },
            async: true,  // Optional, async call ensures it doesn't block
            callback: function(r) {
                if (r.message) {
                    // Display a success message after submission
                    frappe.msgprint("Stock Entry submitted and processed successfully.");
                }
            }
        });
    }
});
