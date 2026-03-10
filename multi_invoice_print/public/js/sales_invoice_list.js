frappe.listview_settings["Sales Invoice"] = {
    onload(listview) {
        listview.page.add_inner_button(__("Print Invoices (4 per page)"), function() {
            let selected = listview.get_checked_items();

            if (selected.length === 0) {
                frappe.msgprint(__("Please select at least one invoice to print."));
                return;
            }

            let names = selected.map(i => i.name);

            window.open(
                "/api/method/multi_invoice_print.api.print_four_invoices?names=" + encodeURIComponent(JSON.stringify(names))
            );
        }, __("Actions"));
    }
};
