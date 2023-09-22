# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WhatsAppMessagingScheduleDate(models.TransientModel):
    _name = 'whatsapp.messaging.schedule.date'
    _description = 'whatsapp.messaging Scheduling'

    schedule_date = fields.Datetime(string='Schedule in the Future')
    whatsapp_messaging_id = fields.Many2one('whatsapp.messaging', required=True)

    @api.constrains('schedule_date')
    def _check_schedule_date(self):
        for scheduler in self:
            if scheduler.schedule_date < fields.Datetime.now():
                raise ValidationError(_('Please select a date equal/or greater than the current date.'))

    def set_schedule_date(self):
        self.whatsapp_messaging_id.write({'schedule_date': self.schedule_date, 'state': 'in_queue'})