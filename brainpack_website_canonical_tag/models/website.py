from odoo import api, fields, models

class Website(models.Model):

    _inherit = "website"

    canonical_tag = fields.Boolean('Canonical Tag')