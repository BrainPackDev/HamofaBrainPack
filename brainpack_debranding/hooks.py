from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from odoo.modules.module import get_module_resource
import base64
def pre_init_hook(cr):
    try:
        sql = "UPDATE ir_module_module SET website = '%s' WHERE license like '%s' and website <> ''" % ('https://www.brainpack.io', 'OEEL%')
        cr.execute(sql)
        cr.commit()
    except Exception as e:
        pass

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    payment_providers = env['payment.provider'].search([])
    for payment_provider in payment_providers:
        if payment_provider.name in ['Wire Transfer']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue',
                                       'payment_provider_custom_payment_method.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Stripe']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_worldlinesips.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Demo']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_demo.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['SEPA Direct Debit']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_sepadirectdebit.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Adyen']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_ayden.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Amazon Payment Services']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_amazonpay.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Asiapay']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_asiapay.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Authorize.net']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_authorize_net.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Buckaroo']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_buckaroo.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Flutterwave']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_flutterwave.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Mercado Pago']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_mercadopago.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Mollie']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_mollie.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['PayPal']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_paypal.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Razorpay']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_razorpay.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})
        if payment_provider.name in ['Sips']:
            path = get_module_resource('brainpack_debranding', 'static/description/blue', 'payment_provider_stripe.png')
            payment_provider.write({'image_128': base64.b64encode(open(path, 'rb').read())})

    moduless = env['ir.module.module'].search([])
    for module in moduless:
        module.icon_image = ''
        if module.id:
            path = modules.module.get_module_icon(module.name)
        else:
            path = ''
        if path:
            module.write({'icon': path})

