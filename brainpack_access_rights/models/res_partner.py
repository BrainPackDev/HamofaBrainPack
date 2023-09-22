from odoo import api, http, fields, models, tools, modules
from odoo.http import request
class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if 'active_test' in self._context and not self._context.get('active_test'):
            pass
        if self._context.get('uid') and not self.env.user.has_group(
                'brainpack_access_rights.main_admin') and self.env.user.has_group('base.group_user'):
            args.append(
                ('id', 'not in', self.env.ref('brainpack_access_rights.main_admin').users.mapped('partner_id.id')))
        res = super(ResPartner, self)._search(args, offset, limit, order, count, access_rights_uid)
        return res