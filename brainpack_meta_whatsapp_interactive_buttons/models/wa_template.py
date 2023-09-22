from odoo import models, fields, api

import json
from odoo.exceptions import UserError


class WATemplate(models.Model):
    _inherit = "wa.template"

    template_type = fields.Selection([('template', 'Template'),
                                      ('interactive', 'Interactive')], string="Template Type")

    def add_whatsapp_template(self):
        components = []
        for component in self.components_ids:
            dict = {}
            if component.type == 'header':
                if component.formate == 'media':
                    IrConfigParam = self.env['ir.config_parameter'].sudo()
                    base_url = IrConfigParam.get_param('web.base.url', False)

                    if component.media_type == 'document':
                        attachment = self.env['ir.attachment'].sudo().search([('name', '=', 'demo-wa-pdf')])
                        if attachment:
                            dict.update({"example": {
                                "header_handle": [
                                    base_url + "/web/content/" + str(attachment.id)
                                ]
                            }, 'type': component.type.upper(), 'format': component.media_type.upper(), })
                        components.append(dict)

                    if component.media_type == 'video':
                        attachment = self.env['ir.attachment'].sudo().search([('name', '=', 'demo-wa-video')])
                        if attachment:
                            dict.update({"example": {
                                "header_handle": [
                                    base_url + "/web/content/" + str(attachment.id)
                                ]
                            }, 'type': component.type.upper(), 'format': component.media_type.upper(), })
                        components.append(dict)

                    if component.media_type == 'image':
                        attachment = self.env['ir.attachment'].sudo().search([('name', '=', 'demo-wa-image')])
                        if attachment:
                            dict.update({"example": {
                                "header_handle": [
                                    base_url + "/web/image/ir.attachment/" + str(attachment.id) + "/datas"
                                ]
                            }, 'type': component.type.upper(), 'format': component.media_type.upper(), })
                        components.append(dict)

                else:
                    body_text = []
                    for variable in component.variables_ids:
                        body_text.append('Test')
                    if body_text:
                        dict.update({"example": {
                            "body_text": [body_text
                                          ]}})
                    if component.text:
                        dict.update({'text': component.text, 'type': component.type.upper(),
                                     'format': component.formate.upper()})
                        components.append(dict)

            elif component.type == 'buttons':
                if component.button_type == 'call_to_action':
                    if component.type_of_action == 'PHONE_NUMBER' and component.is_button_clicked == True:
                        dict.update({"type": component.type.upper(),
                                     "buttons": [
                                         {'type': component.type_of_action, 'text': component.button_text,
                                          'phone_number': component.phone_number
                                          }
                                     ]
                                     })
                        components.append(dict)
                    elif component.type_of_action == 'PHONE_NUMBER' and component.is_button_clicked == False:
                        if component.type_of_action_2 == 'URL':
                            if component.url_type_2 == 'static':
                                dict.update({"type": component.type.upper(),
                                             "buttons": [
                                                 {'type': component.type_of_action, 'text': component.button_text,
                                                  'phone_number': component.phone_number
                                                  },
                                                 {'type': component.type_of_action_2, 'text': component.button_text_2,
                                                  'url': component.static_website_url_2
                                                  }
                                             ]
                                             })
                                components.append(dict)

                            else:
                                dict.update({"type": component.type.upper(),
                                             "buttons": [
                                                 {'type': component.type_of_action, 'text': component.button_text,
                                                  'phone_number': component.phone_number
                                                  },
                                                 {'type': component.type_of_action_2, 'text': component.button_text_2,
                                                  'url': component.dynamic_website_url_2
                                                  }
                                             ]
                                             })
                                components.append(dict)

                elif component.button_type == 'quick_reply':
                    if component.quick_reply_type == 'custom' and component.is_button_clicked == True and component.is_second_button_clicked == True:
                        if component.quick_reply_type == 'custom':
                            dict.update({"type": component.type.upper(),
                                         "buttons": [
                                             {'type': component.button_type.upper(), 'text': component.button_text,
                                              },
                                         ]
                                         })
                            components.append(dict)

                    elif component.quick_reply_type == 'custom' and component.is_button_clicked == False and component.is_second_button_clicked == True:
                        if component.quick_reply_type_2 == 'custom':
                            dict.update({"type": component.type.upper(),
                                         "buttons": [
                                             {'type': component.button_type.upper(), 'text': component.button_text,
                                              },
                                             {'type': component.button_type.upper(),
                                              'text': component.button_text_2,
                                              }
                                         ]
                                         })
                            components.append(dict)

                    elif component.quick_reply_type == 'custom' and component.is_button_clicked == True and component.is_second_button_clicked == False:
                        if component.quick_reply_type_3 == 'custom':
                            dict.update({"type": component.type.upper(),
                                         "buttons": [
                                             {'type': component.button_type.upper(), 'text': component.button_text,
                                              },
                                             {'type': component.button_type.upper(),
                                              'text': component.button_text_3,
                                              }
                                         ]
                                         })
                            components.append(dict)
                    else:
                        if component.quick_reply_type == 'custom':
                            if component.quick_reply_type_2 == 'custom':
                                if component.quick_reply_type_3 == 'custom':
                                    dict.update({"type": component.type.upper(),
                                                 "buttons": [
                                                     {'type': component.button_type.upper(),
                                                      'text': component.button_text,
                                                      },
                                                     {'type': component.button_type.upper(),
                                                      'text': component.button_text_2,
                                                      },
                                                     {'type': component.button_type.upper(),
                                                      'text': component.button_text_3,
                                                      }
                                                 ]
                                                 })
                                    components.append(dict)

            else:
                body_text = []
                for variable in component.variables_ids:
                    body_text.append('Test')
                if body_text:
                    dict.update({"example": {
                        "body_text": [body_text
                                      ]}})
                if component.text:
                    dict.update({'text': component.text, 'type': component.type.upper(), })
                    components.append(dict)

        if components:

            answer = self.provider_id.add_template(self.name, self.lang.iso_code, self.category.upper(), components)
            if answer.status_code == 200:
                dict = json.loads(answer.text)
                if self.provider_id.provider == 'chat_api':
                    if 'message' in dict:
                        raise UserError(
                            (dict.get('message')))
                    if 'error' in dict:
                        raise UserError(
                            (dict.get('error').get('message')))
                    else:
                        if 'status' in dict and dict.get('status') == 'submitted':
                            self.state = 'added'
                            self.namespace = dict.get('namespace')

                if self.provider_id.provider == 'graph_api':
                    if 'message' in dict:
                        raise UserError(
                            (dict.get('message')))
                    if 'error' in dict:
                        raise UserError(
                            (dict.get('error').get('message')))
                    else:
                        if 'id' in dict:
                            self.state = 'added'
                            self.graph_message_template_id = dict.get('id')
        else:
            raise UserError(
                ("please add components!"))

