frappe.ui.form.on('Item',  {
    // Triggered when the form is refreshed
    refresh: function(frm) {
    frm.trigger('set_mandatory_fields');
    },
    // Triggered when the item group field is changed
    item_group: function(frm) {
        frm.trigger('set_mandatory_fields');
    },

    
    // Custom function to set mandatory fields
    set_mandatory_fields: function(frm) {
        if (frm.selected_doc.item_group === 'TYRE') {
            frm.toggle_reqd('pattern', true);
            frm.toggle_reqd('size', true);
            frm.toggle_reqd('manufacturing_year', true);
        } else {
            frm.toggle_reqd('pattern', false);
            frm.toggle_reqd('size', false);
            frm.toggle_reqd('manufacturing_year', false);
        }
    },

    after_save: function(frm) {
        console.log("Item saved. Name:", frm.doc.name);
        frappe.call({
            method: 'api_demo.script.item_api',
            args: {
                item: frm.selected_doc.name // Add any arguments if needed
            },
            async: true,
            callback: function(r) {
                                if (r.message) {
                                    // Handle the response from the Python script
                                    frappe.msgprint("Item saved successfully.");
                                }
            }
        });  
    },

    validate: function(frm) {
        if (frm.selected_doc.item_group === 'TYRE') {
            if (!frm.selected_doc.pattern || !frm.selected_doc.size || !frm.selected_doc.manufacturing_year) {
                frappe.throw(__('Pattern, Size, and Manufacturing Year are mandatory fields for TYRE item group.'));
            }
        }
    }


});

// frappe.listview_settings['Item'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button(__('Custom Button'), function() {
//             frappe.msgprint(__('Custom Button Clicked'));
//         });
//     }
// };
