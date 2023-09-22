from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    canonical_tag = fields.Boolean(
        related='website_id.canonical_tag',
        readonly=False)