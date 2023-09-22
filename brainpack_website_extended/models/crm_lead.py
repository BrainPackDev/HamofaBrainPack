from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from odoo.http import request
from odoo.tools import date_utils, email_re, email_split, is_html_empty, groupby

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    website_url = fields.Char('Website URL')
