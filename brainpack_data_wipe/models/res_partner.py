import logging

from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(index=True, default_export_compatible=True,translate=True)

class ResCompany(models.Model):
    _inherit = 'res.company'

    name = fields.Char(related='partner_id.name', string='Company Name', required=True, store=True, readonly=False,translate=True)