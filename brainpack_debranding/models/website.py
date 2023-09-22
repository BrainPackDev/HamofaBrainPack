from odoo.modules.module import get_resource_path
from odoo import api, fields, models, tools, _, Command
import base64

class Website(models.Model):
    _inherit = "website"

    def init(self):
        websites = self.search([])
        for website in websites:
            img_path = get_resource_path('brainpack_debranding', 'static/description/brainPack_favicon/favicon-32x32.png')
            with tools.file_open(img_path, 'rb') as f:
                website.favicon =  base64.b64encode(f.read())

    def _default_favicon(self):
        img_path = get_resource_path('brainpack_debranding', 'static/description/brainPack_favicon/favicon-32x32.png')
        with tools.file_open(img_path, 'rb') as f:
            return base64.b64encode(f.read())

    favicon = fields.Binary(string="Website Favicon",
                            help="This field holds the image used to display a favicon on the website.",
                            default=_default_favicon)