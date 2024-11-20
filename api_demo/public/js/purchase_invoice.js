frappe.ui.form.on('Purchase Invoice', {
    on_submit: function(frm) {  // Use on_submit instead of after_save
        frappe.call({
            method: 'api_demo.script.purchaseinvoice_api',  // Ensure this is the correct path to your Python method
            args: {
                pi: frm.selected_doc.name  // Correctly pass the Purchase Order name
            },
            async: true,  // Optional, async call ensures it doesn't block
            callback: function(r) {
                if (r.message) {
                    // Display a success message after submission
                    frappe.msgprint("Purchase Invoice submitted and processed successfully.");
                }
            }
        });
    }
});