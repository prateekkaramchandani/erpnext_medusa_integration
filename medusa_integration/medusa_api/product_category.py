from frappe import throw, _
from requests.exceptions import HTTPError
from .client import MedusaAPI


def create(data):
    medusa_client = MedusaAPI()

    try:
        res = medusa_client.post(endpoint="/admin/product-categories", json=data)
    except HTTPError as e:
        error_json = e.response.json()
        throw(
            title=_("Medusa Product Category Create Failed"),
            msg=_("Error: {0}".format(error_json["message"])),
        )

    if res and res.ok:
        return res.json()


def update(id, data):
    medusa_client = MedusaAPI()

    try:
        res = medusa_client.post(
            endpoint="/admin/product-categories/{0}".format(id), json=data
        )
    except HTTPError as e:
        error_json = e.response.json()
        throw(
            title=_("Medusa Product Category Update Failed"),
            msg=_("Error: {0}".format(error_json["message"])),
        )

    if res and res.ok:
        return res.json()


def delete(id):
    medusa_client = MedusaAPI()

    try:
        res = medusa_client.delete(endpoint="/admin/product-categories/{0}".format(id))
    except HTTPError as e:
        error_json = e.response.json()
        throw(
            title=_("Medusa Product Category Delete Failed"),
            msg=_("Error: {0}".format(error_json["message"])),
        )

    return res and res.ok
