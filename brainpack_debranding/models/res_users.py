from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
import xmlrpc.client

class ResUsers(models.Model):
    _inherit = 'res.users'

    def init(self):
        moduless = self.env['ir.module.module'].search([])
        for module in moduless:
            module.icon_image = ''
            if module.id:
                path = modules.module.get_module_icon(module.name)
            else:
                path = ''
            if path:
                module.write({'icon': path})


    notification_type = fields.Selection('_get_notification_type',
        'Notification', required=True, default='email',
        compute='_compute_notification_type', store=True, readonly=False,
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Company: notifications appear in your Company Inbox")

    @api.model
    def _get_notification_type(self):
        return [('email', 'Handle by Emails'),('inbox', 'Handle in Company')]
