# Copyright (c) 2024, Prateek Karamchandani and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe import _
import frappe


class MedusaIntegrationSettings(Document):
    def before_save(self):
        self.medusa_store_url = self.medusa_store_url.rstrip("/")

    def validate(self):
        if self.enable_api and not self.can_enable_api():
            frappe.throw(
                _("Kindly enter Medusa Store URL and Secret API Key to enable API")
            )

    def can_enable_api(self):
        return self.medusa_store_url and self.secret_api_key
