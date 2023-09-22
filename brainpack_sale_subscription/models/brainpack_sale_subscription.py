from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from xmlrpc import client as xmlrpclib
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class BrainpackSaleSubscription(models.Model):
    _name = "brainpack.sale.subscription"

    url = fields.Char("URL")
    db_name = fields.Char("DB Name")
    username = fields.Char("Username")
    password = fields.Char("Password")
    creation_date_db = fields.Datetime("DB Creation Date")
    expiration_date_db = fields.Datetime("DB Expiration Date")
    db_expiration_reason = fields.Text("DB Expiration Reason")
    db_enterprise_code = fields.Text("DB Enterprise Code")

    def get_config_parameters(self):
        # Method to fetch database creation,expiry data from system parameters This method will be called when clicked on "GET DB PARAMETERS" button shown on header of brainpack.sale.subscription model form view.
        for rec in self:
            db_creation_date = False
            db_expiration_date = False
            db_expiration_reason = False
            db_enterprise_code = False
            try:
                url = rec.url
                db = rec.db_name
                username = rec.username
                password = rec.password

                common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
                models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
                uid = common.login(db, username, password)

                db_creation_date = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                     [[['key', '=', 'database.create_date']]],
                                                     {'fields': ['value']})
                db_expiration_date = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                     [[['key', '=', 'database.expiration_date']]],
                                                     {'fields': ['value']})
                db_expiration_reason = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                     [[['key', '=', 'database.expiration_reason']]],
                                                     {'fields': ['value']})
                db_enterprise_code = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                     [[['key', '=', 'database.enterprise_code']]],
                                                     {'fields': ['value']})

            except Exception as e:
                # Show error popup if any exception occurs
                _logger.error(e)
                raise ValidationError(_("Error accessing db"))

            # Update the record with newly fetched data
            rec.write({
                'creation_date_db': datetime.strptime(db_creation_date[0].get('value'), '%Y-%m-%d %H:%M:%S') if db_creation_date and db_creation_date[0].get('value') else False,
                'expiration_date_db': datetime.strptime(db_expiration_date[0].get('value'), '%Y-%m-%d %H:%M:%S') if db_expiration_date and db_expiration_date[0].get('value') else False,
                'db_expiration_reason':db_expiration_reason and db_expiration_reason[0].get('value') or False,
                'db_enterprise_code':db_enterprise_code and db_enterprise_code[0].get('value') or False,
            })
            _logger.info('record with id: %s updated successfully' %rec.id)

