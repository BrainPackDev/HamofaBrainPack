# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    def action_view_clicked(self):
        res = super().action_view_clicked()
        res.update({'view_mode':'tree,form'})
        return res