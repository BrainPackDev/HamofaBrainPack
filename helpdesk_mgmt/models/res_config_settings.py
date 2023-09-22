from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    helpdesk_mgmt_portal_select_team = fields.Boolean(
        related="company_id.helpdesk_mgmt_portal_select_team",
        readonly=False,
    )
