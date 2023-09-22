from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    helpdesk_mgmt_portal_select_team = fields.Boolean(
        string="Select team in Helpdesk portal"
    )
