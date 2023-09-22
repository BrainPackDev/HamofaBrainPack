from odoo import api, http, fields, models, tools, modules
from odoo.http import request
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('uid') and not self.env.user.has_group('brainpack_access_rights.main_admin'):
            args.append(('id','not in',self.env.ref('brainpack_access_rights.main_admin').users.mapped('employee_id.id')))
        res = super(HrEmployee, self)._search(args, offset, limit, order, count, access_rights_uid)
        return res