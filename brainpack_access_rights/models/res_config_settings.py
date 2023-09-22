from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    # add hide fields for config settings
    field_ids = fields.Many2many(related='company_id.field_ids',readonly=False)
    modules_ids = fields.Many2many(related='company_id.modules_ids',readonly=False)
    support_url = fields.Char('Support Url',default='https://www.brainpack.io/support')
