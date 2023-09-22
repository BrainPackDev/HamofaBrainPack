from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class InvestmentAmount(models.Model):
    _name = 'investment.amount'
    _description = 'Investment Amount'
    _order = 'sequence, id'

    sequence = fields.Integer()
    name = fields.Char('Name')
    currency_id = fields.Many2one('res.currency','Currency')

