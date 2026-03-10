import frappe
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def print_four_invoices(names):
    # Parse the names if it's a string
    if isinstance(names, str):
        import json
        names = json.loads(names)
    
    invoices = []
    for invoice_name in names[:4]:
        inv = frappe.get_doc("Sales Invoice", invoice_name)
        
        # Calculate totals - use try/except for optional fields
        try:
            net_total = getattr(inv, 'net_total', 0) or 0
        except:
            net_total = 0
            
        try:
            discount_amount = getattr(inv, 'discount_amount', 0) or 0
        except:
            discount_amount = 0
            
        # Get tax details
        tax_details = []
        total_tax = 0
        
        # First try to get total tax from total_taxes_and_charges field
        try:
            total_tax = inv.total_taxes_and_charges or 0
        except:
            total_tax = 0
            
        # Also try to get individual tax details
        try:
            if inv.taxes:
                for tax in inv.taxes:
                    tax_rate = 0
                    tax_amount = 0
                    try:
                        tax_rate = float(tax.rate) if tax.rate else 0
                    except:
                        pass
                    try:
                        # Use tax_amount instead of amount
                        tax_amount = float(tax.tax_amount) if getattr(tax, 'tax_amount', None) else 0
                    except:
                        pass
                    tax_details.append({
                        "tax_type": tax.charge_type,
                        "tax_rate": tax_rate,
                        "tax_amount": tax_amount
                    })
        except Exception as e:
            pass
            
        grand_total = inv.grand_total or 0
        
        try:
            paid_amount = getattr(inv, 'paid_amount', 0) or 0
        except:
            paid_amount = 0
            
        try:
            outstanding_amount = getattr(inv, 'outstanding_amount', 0) or 0
        except:
            outstanding_amount = 0
            
        change_amount = paid_amount - grand_total if paid_amount > grand_total else 0
        
        # Get items list properly
        items_list = []
        if hasattr(inv, 'items'):
            items_list = inv.items
        
        invoice_data = {
            "name": inv.name,
            "customer": inv.customer,
            "customer_name": getattr(inv, 'customer_name', '') or inv.customer,
            "posting_date": inv.posting_date,
            "company": inv.company,
            "currency": inv.currency,
            "net_total": net_total,
            "discount_amount": discount_amount,
            "total_tax": total_tax,
            "grand_total": grand_total,
            "paid_amount": paid_amount,
            "outstanding_amount": outstanding_amount,
            "change_amount": change_amount,
            "tax_details": tax_details,
            "items": []
        }
        
        for item in items_list:
            invoice_data["items"].append({
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.amount,
                "discount_percent": getattr(item, 'discount_percentage', 0) or 0,
                "discount_amount": getattr(item, 'discount_amount', 0) or 0
            })
        
        invoices.append(invoice_data)

    html = frappe.render_template(
        "multi_invoice_print/templates/print/four_invoice.html",
        {"invoices": invoices}
    )

    pdf = get_pdf(html)

    frappe.local.response.filename = "four_invoices.pdf"
    frappe.local.response.filecontent = pdf
    frappe.local.response.type = "download"

@frappe.whitelist()
def print_four_salary_slips(names):
    # Parse the names if it's a string
    if isinstance(names, str):
        import json
        names = json.loads(names)
    
    salary_slips = []
    for slip_name in names[:4]:
        slip = frappe.get_doc("Salary Slip", slip_name)
        
        # Get earnings and deductions
        earnings = []
        for e in slip.earnings:
            earnings.append({
                "salary_component": e.salary_component,
                "amount": e.amount
            })
        
        deductions = []
        for d in slip.deductions:
            deductions.append({
                "salary_component": d.salary_component,
                "amount": d.amount
            })
        
        # Get company info
        company = frappe.get_doc("Company", slip.company)
        
        slip_data = {
            "name": slip.name,
            "employee_name": slip.employee_name,
            "department": slip.department,
            "start_date": slip.start_date,
            "end_date": slip.end_date,
            "payment_days": slip.payment_days,
            "gross_pay": slip.gross_pay,
            "total_deduction": slip.total_deduction,
            "net_pay": slip.net_pay,
            "company": slip.company,
            "company_address": company.address or "",
            "owner": slip.owner,
            "earnings": earnings,
            "deductions": deductions
        }
        
        salary_slips.append(slip_data)

    html = frappe.render_template(
        "multi_invoice_print/templates/print/four_salary_slip.html",
        {"salary_slips": salary_slips}
    )

    pdf = get_pdf(html)

    frappe.local.response.filename = "four_salary_slips.pdf"
    frappe.local.response.filecontent = pdf
    frappe.local.response.type = "download"
