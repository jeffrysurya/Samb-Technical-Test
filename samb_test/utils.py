import frappe

def handle_stock_update(method, warehouse, item):

	warehouse_doc = frappe.get_doc("Warehouse", warehouse)
	stock_not_found = True
	if warehouse_doc.warehouse_stock_detail_table:
		for stock in warehouse_doc.warehouse_stock_detail_table:
			if stock.item_code == item.item_code:
				update_stock(warehouse_doc, stock, item, method)
				stock_not_found = False
				break
		if stock_not_found:
			append_stock(warehouse_doc, item)
	# handle for first item
	elif not warehouse_doc.warehouse_stock_detail_table and method == "stock_in":
		append_stock(warehouse_doc, item)

def update_stock(warehouse_doc, stock, item, method):
	if method == "stock_in":
		stock.qty_dus += item.qty_dus
		stock.qty_pcs += item.qty_pcs
	elif method == "stock_out":
		validate_stock(stock, item)
		stock.qty_dus -= item.qty_dus
		stock.qty_pcs -= item.qty_pcs
	warehouse_doc.save()


def append_stock(warehouse_doc, item):
	warehouse_doc.append("warehouse_stock_detail_table", {
		"item_code": item.item_code,
		"qty_dus": item.qty_dus,
		"qty_pcs": item.qty_pcs
	})
	warehouse_doc.save()


def validate_stock(stock, item):
	if stock.qty_dus < item.qty_dus or stock.qty_pcs < item.qty_pcs:
		frappe.throw("Stock not enough")
