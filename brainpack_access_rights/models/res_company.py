from odoo import api, http, fields, models, tools
module_lst = ['brainpack_access_rights','brain_pack_backend_ent','brainpack_debranding','general_settings','crm','sale_management','website','account','project']
class Company(models.Model):
    _inherit = 'res.company'

    #add hide fields for config settings
    field_ids = fields.Many2many('ir.model.fields', string='Hide Fields',domain=[('model', '=', 'res.config.settings')])
    # add hide config menu option for config settings
    modules_ids = fields.Many2many('ir.module.module', string='Hide Configuration Menu Options',domain=[('name', 'in', module_lst)])
    support_url = fields.Char('Support Url')

    def get_hide_some_fields_and_menu(self):
        field_lst = self.env.company.sudo().field_ids.mapped('name')
        menu_lst = self.env.company.sudo().modules_ids.mapped('name')
        return field_lst,menu_lst

    def get_check_group_hide_some_fields(self):
        field_lst = []
        if not self.env.user.has_group('brainpack_access_rights.main_admin'):
            field_lst = self.env.company.sudo().field_ids.mapped('name')
        return field_lst,self.env.user.has_group('brainpack_access_rights.main_admin')

    def get_hide_studio(self):
        return self.env.user.has_group('brainpack_access_rights.main_admin')