import logging
import pprint

from werkzeug import urls

from odoo import _, fields, models, api
from odoo.exceptions import UserError, ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_stripe import utils as stripe_utils
from odoo.addons.payment_stripe.const import STATUS_MAPPING, PAYMENT_METHOD_TYPES
from odoo.addons.payment_stripe.controllers.main import StripeController

_logger = logging.getLogger(__name__)

class PaymentTransactionInherit(models.Model):
    _inherit = 'payment.transaction'

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'stripe':
            return
        if self.operation == 'validation':
            status = notification_data.get('setup_intent', {}).get('status')
        elif self.operation == 'refund':
            self.provider_reference = notification_data['refund']['id']
            status = notification_data['refund']['status']
        else:  # 'online_redirect', 'online_token', 'offline'
            status = notification_data.get('payment_intent', {}).get('status')
            if status in ('succeeded',) and self.state == 'done':
                if self.invoice_ids:
                    orders = self.env['sale.order'].sudo().search([('invoice_ids', 'in', self.invoice_ids.ids)])
                    for order in orders:
                        order.payment_token_id = self.token_id


    def _stripe_tokenize_from_notification_data(self, notification_data):
        """ Create a new token based on the notification data.

        :param dict notification_data: The notification data built with Stripe objects.
                                       See `_process_notification_data`.
        :return: None
        """
        super()._stripe_tokenize_from_notification_data(notification_data)
        if self.invoice_ids:
            orders = self.env['sale.order'].sudo().search([('invoice_ids','in',self.invoice_ids.ids)])
            for order in orders:
                order.payment_token_id = self.token_id