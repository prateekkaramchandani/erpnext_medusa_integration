# Copyright (c) 2024, Prateek Karamchandani and contributors
# For license information, please see license.txt

import frappe
from frappe.website.utils import cleanup_page_name
from medusa_integration.medusa_api.product_category import create, delete, update
from frappe.utils.nestedset import NestedSet


class MedusaItemCategory(NestedSet):

    def before_insert(self):
        if not self.handle or not self.handle.strip():
            self.prepare_product_handle()

        data = self.get_payload_data()

        res_data = create(data)
        if not res_data:
            return

        self.medusa_id = res_data["product_category"]["id"]

    def before_save(self):
        if not self.handle or not self.handle.strip():
            self.prepare_product_handle()

        if not self.is_new() and self.medusa_id:
            data = self.get_payload_data()
            res_data = update(self.medusa_id, data)
            if not res_data:
                return

    def on_trash(self):
        if self.medusa_id:
            res = delete(self.medusa_id)
            if not res:
                return

    def prepare_product_handle(self):
        slug = cleanup_page_name(self.category_name).replace("_", "-")
        if self.parent_medusa_item_category:
            parent = frappe.get_doc(
                "Medusa Item Category", self.parent_medusa_item_category
            )
            self.handle = "{0}/{1}".format(parent.handle, slug)
        else:
            self.handle = "/{0}".format(slug)

    def get_payload_data(self):
        data = {
            "name": self.category_name,
            "description": self.description or "",
            "handle": self.handle[1:] if self.handle.startswith("/") else self.handle,
            "is_active": bool(self.enabled),
            "is_internal": bool(self.is_internal),
            "parent_category_id": None,
        }

        if self.parent_medusa_item_category:
            parent = frappe.get_doc(
                "Medusa Item Category", self.parent_medusa_item_category
            )
            data["parent_category_id"] = parent.medusa_id

        return data
