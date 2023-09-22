from odoo import models, fields, api


class Components(models.Model):
    _inherit = 'components'
    _description = 'Whatsapp Components'

    type = fields.Selection(selection_add=[('buttons', 'BUTTONS')])
    button_type = fields.Selection([('none', 'None'),
                                    ('call_to_action', 'Call To Action'),
                                    ('quick_reply', 'Quick Reply')],
                                   'Button Type', default="none")
    type_of_action = fields.Selection([('PHONE_NUMBER', 'Call Phone Number'),
                                       ('URL', 'Visit Website')], 'Type of Action',
                                      default="PHONE_NUMBER")
    button_text = fields.Char(string="Button Text", size=20)
    button_text_2 = fields.Char(string="Button Text", size=20)
    button_text_3 = fields.Char(string="Button Text", size=20)
    phone_number = fields.Char(string="Phone Number", size=20)
    phone_number_2 = fields.Char(string="Phone Number", size=20)
    url_type = fields.Selection([('static', 'Static'),
                                 ('dynamic', 'Dynamic')], 'URL Type', default="static")
    url_type_2 = fields.Selection([('static', 'Static'),
                                   ('dynamic', 'Dynamic')], 'URL Type', default="static")
    name = fields.Char(string='Name', default="a")
    static_website_url = fields.Char(string="Website URL")
    static_website_url_2 = fields.Char(string="Website URL")
    dynamic_website_url = fields.Char(string='URL')
    dynamic_website_url_2 = fields.Char(string='URL')
    quick_reply_type = fields.Selection([('custom', 'Custom')], string="Type", default="custom")
    quick_reply_type_2 = fields.Selection([('custom', 'Custom')], string="Type", default="custom")
    quick_reply_type_3 = fields.Selection([('custom', 'Custom')], string="Type", default="custom")
    footer_text = fields.Char(string="Footer Text", default="Not interested? Tap Stop promotions")
    type_of_action_2 = fields.Selection([('PHONE_NUMBER', 'Call Phone Number'),
                                         ('URL', 'Visit Website')], 'Type of Action', default="URL")
    is_button_clicked = fields.Boolean(string="Is Button Clicked", default=True)
    is_second_button_clicked = fields.Boolean(string="Is Button Clicked", default=True)

    def add_another_button(self):
        self.is_button_clicked = False

    def delete_button(self):
        self.is_button_clicked = True

    def delete_button_2(self):
        self.is_second_button_clicked = True

    def add_third_button(self):
        self.is_second_button_clicked = False
