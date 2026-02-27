# © 2025 initOS GmbH
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _data_normalizer(self, excluded_ids):
        recipient_data = [
            {
                "active": True,
                "email_normalized": data["email_normalized"],
                "id": False,
                "is_follower": False,
                "name": data["name"] or data["email_normalized"],
                "lang": False,
                "groups": [],
                "notif": "email",
                "share": True,
                "type": "customer",
                "uid": False,
                "ushare": False,
            }
            for data in self.read()
            if data["id"] not in excluded_ids
        ]
        return recipient_data

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        pids = super()._notify_get_recipients(message, msg_vals, **kwargs)

        # Avoid email duplication if recipient is a follower and also in cc/bcc
        excluded_ids = (pid["id"] for pid in pids)

        partners_cc = self.env.context.get("partner_cc_ids", None)
        if partners_cc:
            pids.extend(partners_cc._data_normalizer(excluded_ids))

        partners_bcc = self.env.context.get("partner_bcc_ids", None)
        if partners_bcc:
            pids.extend(partners_bcc._data_normalizer(excluded_ids))
        return pids
