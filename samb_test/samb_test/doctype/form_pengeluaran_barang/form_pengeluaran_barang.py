# Copyright (c) 2024, JSD and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from samb_test.utils import handle_stock_update

class FormPengeluaranBarang(Document):
	def on_submit(self):
		self.update_stock(method="stock_out")

	def on_cancel(self):
		self.update_stock(method="stock_in")

	def update_stock(self, method):
		for item in self.pengeluaran_barang_detail_table:
			handle_stock_update(method, self.supplier_warehouse, item)
