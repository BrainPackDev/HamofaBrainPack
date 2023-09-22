from odoo.addons.website.controllers.main import Website
from odoo.addons.web.controllers.utils import _get_login_redirect_url
from odoo import http, models, fields, _

class WebsiteInherit(Website):

    @http.route('/', type='http', auth="user", website=True, sitemap=True)
    def index(self, **kw):
        return super().index()
    def _login_redirect(self, uid, redirect=None):
        if redirect == '/' or redirect == '/?':
            redirect = '/web'
        return _get_login_redirect_url(uid, redirect)