import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    logo = fields.Binary(related='company_id.logo', string="Company Logo",readonly=False)
    favicon = fields.Binary(related='company_id.favicon',string="Company Favicon",readonly=False)
    website = fields.Char(related='company_id.website', readonly=False)
    bot_user_id = fields.Many2one('res.users','Bot User',config_parameter='app_bot_user_id')
    bot_user = fields.Char('Bot User',related='bot_user_id.name',readonly=False)
    bot_user_login = fields.Char('Bot User login',related='bot_user_id.login',readonly=False)
    bot_logo = fields.Binary(string="Bot Image",related='bot_user_id.image_1920',readonly=False)
    app_system_name = fields.Char('System Name',related='company_id.app_system_name',readonly=False)
    app_show_debug = fields.Boolean('Show Quick Debug', config_parameter='app_show_debug')
    app_show_documentation = fields.Boolean('Show Documentation', config_parameter='app_show_documentation')
    app_show_support = fields.Boolean('Show Support', config_parameter='app_show_support')
    app_show_account = fields.Boolean('Show My Account', config_parameter='app_show_account')
    app_documentation_url = fields.Char('Documentation Url', config_parameter='app_documentation_url')
    app_support_url = fields.Char('Support Url', config_parameter='app_support_url')
    app_account_title = fields.Char('My Account Title', config_parameter='app_account_title')
    app_account_url = fields.Char('My Account Url', config_parameter='app_account_url')
