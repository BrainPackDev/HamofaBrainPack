/** @odoo-module **/
var { patch } = require("web.utils");
import {SettingsFormController} from "@web/webclient/settings_form_view/settings_form_controller";
import {SettingsPage} from "@web/webclient/settings_form_view/settings/settings_page";
import rpc from 'web.rpc';
import { session } from "@web/session";

import { useSubEnv, useState, useRef, useEffect, onMounted } from "@odoo/owl";

//hide config fields after config form mounted
patch(SettingsFormController.prototype, "brainpack_access_rights.SettingsFormController", {
    setup() {
        this._super();
         onMounted(() => {
            if(!session.main_admin){
                if(session.field_lst.length > 0){
                    $('.o_field_widget').each(function() {
                        if(session.field_lst.includes($(this).attr("name"))){
                            $(this).closest('.o_setting_box').hide()
                        }
                    });
                }
                if(session.menu_lst.length > 0){
                    $('.settings_tab').find('.tab').each(function() {
                        if(session.menu_lst.includes($(this).data('key'))){
                            $(this).hide()
                        }
                    });
                }
                $('.o_widget_res_config_dev_tool').hide()
                $('.o_widget_iap_buy_more_credits').closest('.o_setting_box').hide()
            }

//            this.user.hasGroup("brainpack_access_rights.client_admin").then(function(result){
//                if(result){
//                    rpc.query({
//                        model: 'res.company',
//                        method: 'get_hide_some_fields_and_menu',
//                        args: [[]],
//                    }).then(function (res) {
//                        if(res[0].length > 0){
//                            $.blockUI()
//                             $('.o_field_widget').each(function() {
//                                if(res.includes($(this).attr("name"))){
//                                    $(this).closest('.o_setting_box').remove()
//                                }
//                            });
//
//                            $.unblockUI()
//                        }
//                        if(res[1].length){
//                            var key_lst = res[1]
//                            $('.settings_tab').find('.tab').each(function() {
//                                if(key_lst.includes($(this).data('key'))){
//                                    $(this).remove()
//                                }
//                            });
//                        }
//                    })
//
//                }
//            });
        });
     }

});

//hide config fields when on click on config menu bar
patch(SettingsPage.prototype, "brainpack_access_rights.SettingsPage", {
    onSettingTabClick(key) {
        var self = this
        if (this.settingsRef.el) {
            const { scrollTop } = this.settingsRef.el;
            this.scrollMap[this.state.selectedTab] = { scrollTop };
        }
        self.state.selectedTab = key;
        self.env.searchState.value = "";
//        debugger;

//        if(!session.main_admin){
//            if(session.field_lst.length > 0){
//                $('.o_field_widget').each(function() {
//                    if(session.field_lst.includes($(this).attr("name"))){
//                        $(this).closest('.o_setting_box').remove()
//                    }
//                });
//            }
//        }

        rpc.query({
                model: 'res.company',
                method: 'get_check_group_hide_some_fields',
                args: [[]],
            }).then(function (res) {
                if(res[0].length > 0){
                     $.blockUI()
                     $('.o_field_widget').each(function() {
                        if(res[0].includes($(this).attr("name"))){
                            $(this).closest('.o_setting_box').remove()
                        }
                    });
                    $.unblockUI()
                }
                if(!res[1]){
                    $('.o_widget_res_config_dev_tool').remove()
                    $('.o_widget_iap_buy_more_credits').closest('.o_setting_box').remove()
                }
            })
    }

});