frappe.listview_settings["Salary Slip"] = {
    onload(listview) {
        listview.page.add_inner_button(__("Print 4 Salary Slip Sheet"), function() {
            let selected = listview.get_checked_items();

            if (selected.length === 0) {
                frappe.msgprint(__("Please select at least one salary slip to print."));
                return;
            }

            if (selected.length > 4) {
                frappe.msgprint(__("Please select maximum of 4 salary slips."));
                return;
            }

            let names = selected.map(i => i.name);

            window.open(
                "/api/method/multi_invoice_print.api.print_four_salary_slips?names=" + encodeURIComponent(JSON.stringify(names))
            );
        }, __("Actions"));
    }
};
