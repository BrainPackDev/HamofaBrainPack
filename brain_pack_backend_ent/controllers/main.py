# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
# Developed by Bizople Solutions Pvt. Ltd.

import datetime
import pytz
from odoo import http, models, fields, api, tools
from odoo.http import request


class BackendConfigration(http.Controller):

    @http.route(['/color/pallet/'], type='json', auth='public')
    def get_selected_pallet(self, **kw):
        config_vals = {}
        current_user = request.env.user
        app_light_bg_image = kw.get('app_light_bg_image')

        if app_light_bg_image:
            if 'data:image/' in str(app_light_bg_image):
                light_bg_file = str(app_light_bg_image).split(',')
                app_light_bg_file_mimetype = light_bg_file[0]
                app_light_bg_image = light_bg_file[1]
            else:
                light_bg_file = str(app_light_bg_image).split("'")
                app_light_bg_image = light_bg_file[1]
        else:
            app_light_bg_image = False

        config_vals.update({
            'light_primary_bg_color': kw.get('light_primary_bg_color'),
            'light_primary_text_color': kw.get('light_primary_text_color'),
            'light_bg_image': app_light_bg_image,
            'apply_light_bg_img': kw.get('apply_light_bg_img'),
            'tree_form_split_view': kw.get('tree_form_split_view'),
            'attachment_in_tree_view': kw.get('attachment_in_tree_view'),
            'separator': kw.get('selected_separator'),
            'tab': kw.get('selected_tab'),
            'checkbox': kw.get('selected_checkbox'),
            'radio': kw.get('selected_radio'),
            'popup': kw.get('selected_popup'),
            'use_custom_colors': kw.get('custom_color_pallet'),
            'color_pallet': kw.get('selected_color_pallet'),
            'appdrawer_custom_bg_color': kw.get('custom_drawer_bg'),
            'appdrawer_custom_text_color': kw.get('custom_drawer_text'),
            'use_custom_drawer_color': kw.get('custom_drawer_color_pallet'),
            'drawer_color_pallet': kw.get('selected_drawer_color_pallet'),
            'loader_style': kw.get('selected_loader'),
            'font_family': kw.get('selected_fonts'),
            'font_size': kw.get('selected_fontsize'),
            'chatter_position': kw.get('selected_chatter_position'),
            'top_menu_position': kw.get('selected_top_menu_position'),
            'theme_style': kw.get('selected_theme_style'),
            'list_view_density': kw.get('selected_list_view_density'),
            'list_view_sticky_header': kw.get('selected_list_view_sticky_header'),
        })

        if current_user.backend_theme_config:
            current_user.backend_theme_config.sudo().update(config_vals)
        else:
            backend_config_record = request.env['backend.config'].sudo().create(
                config_vals)
            current_user.sudo().write({
                'backend_theme_config': backend_config_record.id
            })

        return True

    @http.route(['/color/pallet/data/'], type='http', auth='public', sitemap=False)
    def selected_pallet_data(self, **kw):
        company = request.env.company
        user = request.env.user
        admin_users = request.env['res.users'].sudo().search([
            ('groups_id', 'in', request.env.ref('base.user_admin').id),
            ('backend_theme_config', '!=', False),
        ], order="id asc", limit=1)

        admin_config = False
        if admin_users:
            admin_config = admin_users.backend_theme_config

        if company.backend_theme_level == 'user_level':
            if user.backend_theme_config:
                config_vals = user.backend_theme_config
            elif admin_config:
                config_vals = admin_config
            else:
                config_vals = request.env['backend.config'].sudo().search(
                    [], order="id asc", limit=1)
        else:
            if admin_config:
                config_vals = admin_config
            else:
                config_vals = request.env['backend.config'].sudo().search(
                    [], order="id asc", limit=1)

        values = {}
        separator_selection_dict = dict(
            config_vals._fields['separator'].selection)
        tab_selection_dict = dict(config_vals._fields['tab'].selection)
        checkbox_selection_dict = dict(
            config_vals._fields['checkbox'].selection)
        radio_selection_dict = dict(config_vals._fields['radio'].selection)
        popup_selection_dict = dict(config_vals._fields['popup'].selection)
        light_bg_image = config_vals.light_bg_image
        values.update({
            'config_vals': config_vals,
            'separator_selection_dict': separator_selection_dict,
            'tab_selection_dict': tab_selection_dict,
            'checkbox_selection_dict': checkbox_selection_dict,
            'radio_selection_dict': radio_selection_dict,
            'popup_selection_dict': popup_selection_dict,
            'app_background_image': light_bg_image,
        })

        response = request.render(
            "brain_pack_backend_ent.template_backend_config_data", values)

        return response

    @http.route(['/get/model/record'], type='json', auth='public')
    def get_record_data(self, **kw):
        company = request.env.company
        user = request.env.user
        admin_group_id = request.env.ref('base.user_admin').id
        is_admin = False
        if admin_group_id in user.groups_id.ids:
            is_admin = True
        admin_users = request.env['res.users'].sudo().search([
            ('groups_id', 'in', request.env.ref('base.user_admin').id),
            ('backend_theme_config', '!=', False),
        ], order="id asc", limit=1)
        admin_users_ids = admin_users.ids
        admin_config = False
        if admin_users:
            admin_config = admin_users.backend_theme_config
        show_edit_mode = True
        for admin in admin_users:
            if admin.backend_theme_config:
                admin_config = admin.backend_theme_config
                break
            else:
                continue

        if company.backend_theme_level == 'user_level':
            if user.backend_theme_config:
                record_vals = user.backend_theme_config
            elif admin_config:
                record_vals = admin_config
            else:
                record_vals = request.env['backend.config'].sudo().search(
                    [], order="id asc", limit=1)
        else:
            if not user.id in admin_users_ids:
                show_edit_mode = False
            if admin_config:
                record_vals = admin_config
            else:
                record_vals = request.env['backend.config'].sudo().search(
                    [], order="id asc", limit=1)

        prod_obj = request.env['backend.config']
        record_dict = record_vals.read(set(prod_obj._fields))
        if user.dark_mode:
            darkmode = "dark_mode"
        else:
            darkmode = False
        if user.vertical_sidebar_pinned:
            pinned_sidebar = "pinned"
        else:
            pinned_sidebar = False

        if company.prevent_auto_save:
            prevent_auto_save = "prevent_auto_save"
        else:
            prevent_auto_save = False

        if user.enable_todo_list:
            todo_list_enable = "enable_todo_list"
        else:
            todo_list_enable = False

        record_val = {
            'record_dict': record_dict,
            'darkmode': darkmode,
            'pinned_sidebar': pinned_sidebar,
            'show_edit_mode': show_edit_mode,
            'is_admin': is_admin,
            'prevent_auto_save': prevent_auto_save,
            'todo_list_enable': todo_list_enable,
        }
        return record_val

    @http.route(['/get-favorite-apps'], type='json', auth='public')
    def get_favorite_apps(self, **kw):
        user_id = request.env.user
        app_list = []
        if user_id.app_ids:
            for app in user_id.app_ids:
                irmenu = request.env['ir.ui.menu'].sudo().search(
                    [('id', '=', app.app_id)])
                if irmenu:
                    app_dict = {
                        'name': app.name,
                        'app_id': app.app_id,
                        'app_xmlid': app.app_xmlid,
                        'app_actionid': app.app_actionid,
                        'line_id': app.id,
                        'use_icon': irmenu.use_icon,
                        'icon_class_name': irmenu.icon_class_name,
                        'icon_img': irmenu.icon_img,
                        'web_icon': irmenu.web_icon,
                        'web_icon_data': irmenu.web_icon_data,
                    }
                    app_list.append(app_dict)
            record_val = {
                'app_list': app_list,
            }
            return record_val
        else:
            return False

    @http.route(['/update-user-fav-apps'], type='json', auth='public')
    def update_favorite_apps(self, **kw):
        user_id = request.env.user
        user_id.sudo().write({
            'app_ids': [(0, 0, {
                'name': kw.get('app_name'),
                'app_id': kw.get('app_id'),
            })]
        })
        return True

    @http.route(['/remove-user-fav-apps'], type='json', auth='public')
    def remove_favorite_apps(self, **kw):
        user_id = request.env.user

        for line in user_id.app_ids:
            if line.app_id == str(kw.get('app_id')):
                user_id.sudo().write({
                    'app_ids': [(3, line.id)]
                })
        return True

    @http.route(['/get/active/menu'], type='json', auth='public')
    def get_active_menu_data(self, **kw):
        menu_items = []
        menu_records = request.env['ir.ui.menu'].search(
            [('parent_id', '=', False)])
        for menu in menu_records:
            menu_items.append({
                'menu_name': menu.complete_name,
                'menu_id': menu.id
            })
        return menu_items

    @http.route(['/get/appsearch/data'], type='json', auth='public')
    def get_appsearch_data(self, menuOption=None, **kw):
        menu_items = []
        menu_records = request.env['ir.ui.menu'].search(
            [('name', 'ilike', kw.get('searchvals'))], order='id asc')
        if menuOption:
            for record in menu_records:
                if record.parent_path:
                    parent_record = record.parent_path.split('/')
                    parent_record_id = parent_record[0]
                    if parent_record_id == menuOption:
                        if not record.child_id:
                            menu_items.append({
                                'name': record.complete_name,
                                'menu_id': record.id
                            })
        else:
            for record in menu_records:
                if not record.child_id:
                    menu_items.append({
                        'name': record.complete_name,
                        'menu_id': record.id,
                        'previous_menu_id': record.parent_id.id,
                        'action_id': record.action.id if record.action else None,
                    })
        return menu_items

    @http.route(['/get/tab/title/'], type='json', auth='public')
    def get_tab_title(self, **kw):
        company_id = request.env.company
        new_name = company_id.tab_name
        return new_name

    @http.route(['/get/active/lang'], type='json', auth='public')
    def get_active_lang(self, **kw):
        lang_records = request.env['res.lang'].sudo().search(
            [('active', '=', 'True')])
        lang_list = []
        for lang in lang_records:
            lang_list.append({
                'lang_name': lang.name,
                'lang_code': lang.code,
            })

        return lang_list

    @http.route(['/change/active/lang'], type='json', auth='public')
    def biz_change_active_lang(self, **kw):
        request.env.user.lang = kw.get('lang')
        return True

    @http.route(['/active/dark/mode'], type='json', auth='public')
    def active_dark_mode(self, **kw):
        dark_mode = kw.get('dark_mode')
        backend_theme_config = request.env['backend.config'].sudo().search([])
        user = request.env.user
        if dark_mode == 'on':
            user.update({
                'dark_mode': True,
            })
            dark_mode = user.dark_mode
            return dark_mode
        elif dark_mode == 'off':
            user.update({
                'dark_mode': False,
            })
            dark_mode = user.dark_mode
            return dark_mode

    @http.route(['/sidebar/behavior/update'], type='json', auth='public')
    def sidebar_behavior(self, **kw):
        user = request.env.user
        sidebar_pinned = kw.get('sidebar_pinned')
        user.update({
            'vertical_sidebar_pinned': sidebar_pinned,
        })
        return True

    @http.route(['/get/dark/mode/data'], type='json', auth='public')
    def dark_mode_on(self, **kw):
        user = request.env.user
        dark_mode_value = user.dark_mode

        return dark_mode_value

    # SPIFFY MULTI TAB START
    @http.route(['/add/mutli/tab'], type='json', auth='public')
    def add_multi_tab(self, **kw):
        user = request.env.user
        # user.sudo().write({
        #     'multi_tab_ids': False,
        # })
        multi_tab_ids = user.multi_tab_ids.filtered(
            lambda mt: mt.name == kw.get('name'))
        if not multi_tab_ids:
            user.sudo().write({
                'multi_tab_ids': [(0, 0, {
                    'name': kw.get('name'),
                    'url': kw.get('url'),
                    'actionId': kw.get('actionId'),
                    'menuId': kw.get('menuId'),
                    'menu_xmlid': kw.get('menu_xmlid'),
                })]
            })

        return True

    @http.route(['/get/mutli/tab'], type='json', auth='public')
    def get_multi_tab(self, **kw):
        obj = request.env['biz.multi.tab']
        user = request.env.user
        if user.multi_tab_ids:
            record_dict = user.multi_tab_ids.sudo().read(set(obj._fields))
            return record_dict
        else:
            return False

    @http.route(['/remove/multi/tab'], type='json', auth='public')
    def remove_multi_tab(self, **kw):
        multi_tab = request.env['biz.multi.tab'].sudo().search(
            [('id', '=', kw.get('multi_tab_id'))])
        multi_tab.unlink()
        user = request.env.user
        multi_tab_count = len(user.multi_tab_ids)
        values = {
            'removeTab': True,
            'multi_tab_count': multi_tab_count,
        }
        return values

    @http.route(['/update/tab/details'], type='json', auth='public')
    def update_tabaction(self, **kw):
        tabId = kw.get('tabId')
        TabTitle = kw.get('TabTitle')
        url = kw.get('url')
        ActionId = kw.get('ActionId')
        menu_xmlid = kw.get('menu_xmlid')

        multi_tab = request.env['biz.multi.tab'].sudo().search(
            [('id', '=', tabId)])
        if multi_tab:
            multi_tab.sudo().write({
                'name': TabTitle or multi_tab.name,
                'url': url or multi_tab.url,
                'actionId': ActionId or multi_tab.ActionId,
                'menu_xmlid': menu_xmlid or multi_tab.menu_xmlid,
            })
        return True

    # SPIFFY MULTI TAB END

    @http.route(['/add/bookmark/link'], type='json', auth='public')
    def add_bookmark_link(self, **kw):
        user = request.env.user
        bookmark_ids = user.bookmark_ids.filtered(
            lambda b: b.name == kw.get('name'))
        if not bookmark_ids:
            user.sudo().write({
                'bookmark_ids': [(0, 0, {
                    'name': kw.get('name'),
                    'url': kw.get('url'),
                    'title': kw.get('title'),
                })]
            })

        return True

    @http.route(['/update/bookmark/link'], type='json', auth='public')
    def update_bookmark_link(self, **kw):
        bookmark = request.env['bookmark.link'].sudo().search(
            [('id', '=', kw.get('bookmark_id'))])
        updated_bookmark = bookmark.update({
            'name': kw.get('bookmark_name'),
            'title': kw.get('bookmark_title'),
        })
        return True

    @http.route(['/remove/bookmark/link'], type='json', auth='public')
    def remove_bookmark_link(self, **kw):
        bookmark = request.env['bookmark.link'].sudo().search(
            [('id', '=', kw.get('bookmark_id'))])
        bookmark.unlink()
        return True

    @http.route(['/get/bookmark/link'], type='json', auth='public')
    def get_bookmark_link(self, **kw):
        obj = request.env['bookmark.link']
        user = request.env.user
        record_dict = user.bookmark_ids.sudo().read(set(obj._fields))
        return record_dict

    @http.route(['/get/attachment/data'], type='json', auth='public')
    def get_attachment_data(self, **kw):
        rec_ids = kw.get('rec_ids')
        for rec in rec_ids:
            if isinstance(rec, str):
                rec_ids.remove(rec)
        if kw.get('model') and rec_ids:
            # FOR DATA SPEED ISSUE; SEARCH ATTACHMENT DATA WITH SQL QUERY
            attachments = request.env['ir.attachment'].search([
                ('res_model', '=', kw.get('model'))
            ])
            attachment_data = []
            attachment_res_id_set = set()
            for attachment in attachments:
                attachment_res_id_set.add(attachment.res_id)
            dict = {}
            for res_id in attachment_res_id_set:
                filtered_attachment_record = attachments.filtered(
                    lambda attachment: attachment.res_id == res_id)
                for fac in filtered_attachment_record:
                    if dict.get(res_id):
                        dict[res_id].append({
                            'attachment_id': fac.id,
                            'attachment_mimetype': fac.mimetype,
                            'attachment_name': fac.name,
                        })
                    else:
                        dict[res_id] = [{
                            'attachment_id': fac.id,
                            'attachment_mimetype': fac.mimetype,
                            'attachment_name': fac.name,
                        }]
            attachment_data.append(dict)
            return attachment_data

    @http.route(['/get/irmenu/icondata'], type='json', auth='public')
    def get_irmenu_icondata(self, **kw):
        irmenuobj = request.env['ir.ui.menu']
        irmenu = request.env['ir.ui.menu'].sudo().search(
            [('id', 'in', kw.get('menu_ids'))])

        app_menu_dict = {}
        for menu in irmenu:
            try:
                if request.env.ref('sale.sale_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/sales.png'})
            except:
                pass
            try:
                if request.env.ref('purchase.menu_purchase_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/purchases.png'})
            except:
                pass
            try:
                if request.env.ref('crm.crm_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/crm.png'})
            except:
                pass
            try:
                if request.env.ref('stock.menu_stock_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/inventory.png'})
            except:
                pass
            try:
                if request.env.ref('account.account_account_menu') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/accounting.png'})
            except:
                pass
            try:
                if request.env.ref('account_accountant.menu_accounting') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/accounting.png'})
            except:
                pass

            # try:
            #     if request.env.ref('sale.sale_menu_root') == menu:
            #         menu.write({'web_icon':'brainpack_debranding,static/description/blue/appointment.png'})
            # except:
            #     pass
            try:
                if request.env.ref('approvals.approvals_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/approvals.png'})
            except:
                pass
            # try:
            #     if request.env.ref('sale.sale_menu_root') == menu:
            #         menu.write({'web_icon':'brainpack_debranding,static/description/blue/blogs.png'})
            # except:
            #     pass
            try:
                if request.env.ref('mail.menu_root_discuss') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/discuss.png'})
            except:
                pass
            try:
                if request.env.ref('documents.menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/documents.png'})
            except:
                pass
            # try:
            #     if request.env.ref('sale.sale_menu_root') == menu:
            #         menu.write({'web_icon':'brainpack_debranding,static/description/blue/eCommerce.png'})
            # except:
            #     pass
            try:
                if request.env.ref('website_slides.website_slides_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/eLearning.png'})
            except:
                pass
            # try:
            #     if request.env.ref('sale.sale_menu_root') == menu:
            #         menu.write({'web_icon':'brainpack_debranding,static/description/blue/emailAutomation.png'})
            # except:
            #     pass
            try:
                if request.env.ref('hr.menu_hr_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/employees.png'})
            except:
                pass
            try:
                if request.env.ref('event.event_main_menu') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/events.png'})
            except:
                pass
            try:
                if request.env.ref('hr_expense.menu_hr_expense_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/expenses.png'})
            except:
                pass
            # try:
            #     if request.env.ref('sale.sale_menu_root') == menu:
            #         menu.write({'web_icon':'brainpack_debranding,static/description/blue/forum.png'})
            # except:
            #     pass


            try:
                if request.env.ref('helpdesk_mgmt.helpdesk_ticket_main_menu') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/helpdesk.png'})
            except:
                pass
            try:
                if request.env.ref('helpdesk.menu_helpdesk_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/helpdesk.png'})
            except:
                pass
            try:
                if request.env.ref('account.menu_finance') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/invoicing.png'})
            except:
                pass
            try:
                if request.env.ref('knowledge.knowledge_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/knowledge.png'})
            except:
                pass
            try:
                if request.env.ref('im_livechat.menu_livechat_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/liveChat.png'})
            except:
                pass
            try:
                if request.env.ref('maintenance.menu_maintenance_title') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/maintainance.png'})
            except:
                pass
            try:
                if request.env.ref('mrp.menu_mrp_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/manufacturing.png'})
            except:
                pass
            try:
                if request.env.ref('marketing_automation.marketing_automation_menu') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/marketingAutomation.png'})
            except:
                pass
            try:
                if request.env.ref('planning.planning_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/planning.png'})
            except:
                pass
            try:
                if request.env.ref('mrp_plm.menu_mrp_plm_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/plm.png'})
            except:
                pass
            try:
                if request.env.ref('point_of_sale.menu_point_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/pointOfSale.png'})
            except:
                pass
            try:
                if request.env.ref('project.menu_main_pm') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/project.png'})
            except:
                pass
            try:
                if request.env.ref('quality_control.menu_quality_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/quality.png'})
            except:
                pass
            try:
                if request.env.ref('hr_recruitment.menu_hr_recruitment_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/recruitment.png'})
            except:
                pass
            try:
                if request.env.ref('hr_referral.menu_hr_referral_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/refferals.png'})
            except:
                pass
            try:
                if request.env.ref('mass_mailing_sms.mass_mailing_sms_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/smsMarketing.png'})
            except:
                pass
            try:
                if request.env.ref('sale_subscription.menu_sale_subscription_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/subscription.png'})
            except:
                pass
            try:
                if request.env.ref('survey.menu_surveys') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/surveys.png'})
            except:
                pass
            try:
                if request.env.ref('hr_holidays.menu_hr_holidays_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/timeOff.png'})
            except:
                pass
            try:
                if request.env.ref('hr_timesheet.timesheet_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/timeSheet.png'})
            except:
                pass
            try:
                if request.env.ref('iot.iot_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/internet-of-things.png'})
            except:
                pass
            try:
                if request.env.ref('hr_appraisal.menu_hr_appraisal_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/appraisals.png'})
            except:
                pass
            try:
                if request.env.ref('hr_payroll.menu_hr_payroll_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/payroll.png'})
            except:
                pass
            try:
                if request.env.ref('fleet.menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/fleet.png'})
            except:
                pass
            try:
                if request.env.ref('sale_renting.rental_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/rental.png'})
            except:
                pass
            try:
                if request.env.ref('contacts.menu_contacts') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/contacts.png'})
            except:
                pass

            try:
                if request.env.ref('account_consolidation.menu_consolidation') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/consolidation.png'})
            except:
                pass
            try:
                if request.env.ref('lunch.menu_lunch') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/lunch.png'})
            except:
                pass
            try:
                if request.env.ref('stock_barcode.stock_barcode_menu') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/barcode.png'})
            except:
                pass
            try:
                if request.env.ref('hr_attendance.menu_hr_attendance_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/attendance.png'})
            except:
                pass
            try:
                if request.env.ref('industry_fsm.fsm_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/field-service.png'})
            except:
                pass
            try:
                if request.env.ref('repair.menu_repair_order') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/repair.png'})
            except:
                pass
            try:
                if request.env.ref('calendar.mail_menu_calendar') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/calender.png'})
            except:
                pass
            try:
                if request.env.ref('note.menu_note_notes') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/notes.png'})
            except:
                pass
            try:
                if request.env.ref('base.menu_management') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/apps.png'})
            except:
                pass
            try:
                if request.env.ref('base.menu_board_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/dashboard.png'})
            except:
                pass
            try:
                if request.env.ref('spreadsheet_dashboard.spreadsheet_dashboard_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/spreadsheet_dashboard.png'})
            except:
                pass
            try:
                if request.env.ref('base.menu_administration') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/seetings.png'})
            except:
                pass
            try:
                if request.env.ref('website.menu_website_configuration') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/website-builder.png'})
            except:
                pass

            try:
                if request.env.ref('membership.menu_association') == menu:
                    menu.write({'web_icon': 'membership,static/description/blue/member.png'})
            except:
                pass

            try:
                if request.env.ref('utm.menu_link_tracker_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/link_tracker.png'})
            except:
                pass

            try:
                if request.env.ref('mass_mailing.mass_mailing_menu_root') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/emailAutomation.png'})
            except:
                pass

            try:
                if request.env.ref('social.menu_social_global') == menu:
                    menu.write({'web_icon': 'brainpack_debranding,static/description/blue/marketingAutomation.png'})
            except:
                pass



            # try:
            #     if request.env.ref('sale.sale_menu_root') == menu:
            #         menu.write({'web_icon':'brainpack_debranding,static/description/blue/VoIP.png'})
            # except:
            #     pass
            # try:
            #     if request.env.ref('sale.sale_menu_root') == menu:
            #         menu.write({'web_icon':'brainpack_debranding,static/description/blue/website-builder.png'})
            # except:
            #     pass

            menu_dict = menu.read(set(irmenuobj._fields))
            app_menu_dict[menu.id] = menu_dict
        return app_menu_dict

    # TO DO LIST CONTROLLERS
    @http.route(['/show/user/todo/list/'], type='http', auth='public', sitemap=False)
    def show_user_todo_list(self, **kw):
        company = request.env.company
        user = request.env.user

        values = {}
        user_tz_offset = user.tz_offset
        user_tz_offset_time = datetime.datetime.strptime(user_tz_offset, '%z').utcoffset()
        today_date = datetime.datetime.now()
        today_date_with_offset = datetime.datetime.now() + user_tz_offset_time

        values.update({
            'user': user.sudo(),
            'today_date': today_date_with_offset,
            'user_tz_offset_time': user_tz_offset_time,
        })

        response = request.render("brain_pack_backend_ent.to_do_list_template", values)

        return response

    @http.route(['/create/todo'], type='json', auth='public')
    def create_todo(self, **kw):
        user_id = kw.get('user_id', None)
        note_title = kw.get('note_title', None)
        note_description = kw.get('note_description', None)
        is_update = kw.get('is_update')
        note_id = kw.get('note_id', None)
        note_pallet = kw.get('note_pallet', None)

        user = request.env.user

        if user_id and (note_title or note_description):
            user_tz_offset = user.tz_offset
            user_tz_offset_time = datetime.datetime.strptime(user_tz_offset, '%z')

            todo_obj = request.env['todo.list'].sudo()

            if is_update:
                todo_record = todo_obj.browse(int(note_id))
                todo_record.update({
                    'name': note_title,
                    'description': note_description,
                    'note_color_pallet': note_pallet,
                })
            else:
                todo_record = todo_obj.create({
                    'user_id': int(user_id),
                    'name': note_title,
                    'description': note_description,
                    'note_color_pallet': note_pallet,
                })

            user_tz_offset = user.tz_offset
            user_tz_offset_time = datetime.datetime.strptime(user_tz_offset, '%z').utcoffset()
            today_date = datetime.datetime.now()
            today_date_with_offset = datetime.datetime.now() + user_tz_offset_time

            note_content = request.env['ir.ui.view']._render_template(
                "brain_pack_backend_ent.to_do_list_content_template", {
                    'note': todo_record,
                    'today_date': today_date_with_offset,
                    'user_tz_offset_time': user_tz_offset_time,
                }
            )

            return note_content

    @http.route(['/delete/todo'], type='json', auth='public')
    def delete_todo(self, **kw):
        note_id = kw.get('noteID', None)
        if note_id:
            todo_obj = request.env['todo.list'].sudo()
            todo_record = todo_obj.browse(note_id)
            todo_record.unlink()
            return True
        else:
            return False
