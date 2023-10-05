# -*- coding: utf-8 -*-

import re
from odoo.exceptions import ValidationError
from odoo.tools import remove_accents
from odoo import _, api, exceptions, fields, models, tools

class AliasMail(models.Model):
    _name = 'alias.mail'
    _rec_name = 'domain_name'
    
    domain_name = fields.Char(string="Domain Name")
    company_id = fields.Many2one('res.company', string="Company")

class Alias(models.Model):
    _inherit = "mail.alias"
    
    def _custom_default_alias_domain(self):
        current_user = self.env['res.users'].browse(self._context.get('uid') or self._uid or self.env.user.id)
        alias = self.env["alias.mail"].sudo().search([('company_id','=',current_user.company_id.id)],limit=1)
        return alias
    
    alias_domain = fields.Many2one('alias.mail',default=lambda self:self._custom_default_alias_domain())
#     name = fields.Char(store=True)
    
    _sql_constraints = [
        ('alias_unique', 'Check(1=1)', 'Unfortunately this email alias is already used, please choose a unique one')
    ]
    
    @api.model
    def _clean_and_make_unique(self, name, alias_ids=False):
        # when an alias name appears to already be an email, we keep the local part only
        name = remove_accents(name).lower().split('@')[0]
        name = re.sub(r'[^\w+.]+', '-', name)
        return name
    
    def name_get(self):
        """Return the mail alias display alias_name, including the implicit
           mail catchall domain if exists from config otherwise "New Alias".
           e.g. `jobs@mail.odoo.com` or `jobs` or 'New Alias'
        """
        res = []
        for record in self:
            if record.alias_name and record.alias_domain:
                res.append((record['id'], "%s@%s" % (record.alias_name, record.alias_domain.domain_name)))
            elif record.alias_name:
                res.append((record['id'], "%s" % (record.alias_name)))
            else:
                res.append((record['id'], _("Inactive Alias")))
        return res
    
    
