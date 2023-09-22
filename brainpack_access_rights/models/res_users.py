from odoo import api, http, fields, models, tools, modules
from lxml import etree, html
from odoo.http import request

class HideMenuUser(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        if self.user_has_groups('brainpack_access_rights.client_admin'):
            if 'list' in res['views'] and res['views'].get('list'):
                list_xml = res['views'].get('list')
                root = etree.fromstring(list_xml['arch'])
                root.set('create', 'false')
                root.set('delete', 'false')
                root.set('no_open', 'false')
                if list_xml.get('toolbar'):
                    list_xml['toolbar']['print'] = []
                    list_xml['toolbar']['action'] = []
                list_xml['arch'] = etree.tostring(root)
            if 'form' in res['views'] and res['views'].get('form'):
                form_xml = res['views'].get('form')
                root = etree.fromstring(form_xml['arch'])
                root.set('create', 'false')
                root.set('delete', 'false')
                root.set('no_open', 'false')
                if form_xml.get('toolbar'):
                    form_xml['toolbar']['print'] = []
                    form_xml['toolbar']['action'] = []
                form_xml['arch'] = etree.tostring(root)
        return res

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if 'active_test' in self._context and not self._context.get('active_test'):
            pass
        elif self._context.get('uid') and not self.env.user.has_group(
                'brainpack_access_rights.main_admin') and self.env.user.has_group('base.group_user'):
            args.append(
                ('id', 'not in', self.env.ref('brainpack_access_rights.main_admin').users.ids))
        res = super(HideMenuUser, self)._search(args, offset, limit, order, count, access_rights_uid)
        return res