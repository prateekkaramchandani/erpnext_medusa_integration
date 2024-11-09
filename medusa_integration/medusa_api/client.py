from urllib.parse import urljoin
from frappe import _
import requests
import frappe


class MedusaAPI:
    def __init__(self):
        self.settings = frappe.get_cached_doc("Medusa Integration Settings")
        self.base_url = self.settings.medusa_store_url
        self.api_key = self.settings.get_password("secret_api_key")
        self.default_headers = {"Authorization": "Basic {0}".format(self.api_key)}

    def get(self, *args, **kwargs):
        return self._make_request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._make_request("POST", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._make_request("DELETE", *args, **kwargs)

    def _make_request(self, method, endpoint, params=None, headers=None, json=None):
        if not self.settings.enable_api:
            return

        if method not in ("GET", "POST", "DELETE"):
            frappe.throw(_("Invalid method {0}".format(method)))

        request_args = frappe._dict(
            url=self.get_url(endpoint),
            params=params,
            headers={
                **self.default_headers,
                **(headers or {}),
            },
        )

        if method == "POST" and json:
            request_args.json = json
        try:
            response = requests.request(method, **request_args)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            raise http_err

    def get_url(self, endpoint):
        return urljoin(self.base_url, endpoint)
