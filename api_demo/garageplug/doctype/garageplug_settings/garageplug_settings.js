// Copyright (c) 2024, shahala and contributors
// For license information, please see license.txt

// frappe.ui.form.on("GaragePlug Settings", {
// 	refresh(frm) {
        
//          // Add a custom button to the form header
//          frm.page.add_inner_button(__('Generate Token'), function() {
//             generateToken(frm);
//         });

//         // Automatically trigger the token generation every 24 hours (___ ms)
//         // setInterval(function() {
//         //     generateToken(frm);
//         // }, 86400000);  // 24 hours in milliseconds
// 	},
// });

// function generateToken(frm) {
//     // Call the API to generate the token
//     frappe.call({
//         method: 'api_demo.script.get_access_token', // Path to your server-side method
//         callback: function(response) {
//             if (response.message) {
//                 // Assuming the response contains the token
//                 var token = response.message;

//                 // Set the token in the 'token' field
//                 frm.set_value('token', token);

//                 // Save the form to ensure the token is stored in the database
//                 frm.save();
//                 frm.reload_doc();
//                 frappe.msgprint(__('Token generated successfully.'));
//             } else {
//                 frappe.msgprint(__('Failed to generate token.'));
//             }
//         }
//     });
// }
