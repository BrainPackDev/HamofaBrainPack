/** @odoo-module **/
var { patch } = require("web.utils");
//import {StudioSystray} from "@web_studio/systray_item/systray_item";;
import { FilterMenu } from "@web/search/filter_menu/filter_menu";
import { useSubEnv, useState, useRef, useEffect, onMounted } from "@odoo/owl";
import rpc from 'web.rpc';
import { session } from "@web/session";

patch(FilterMenu.prototype, "brainpack_access_rights.FilterMenu", {
    setup() {
        this._super();
        var self = this
        onMounted(() => {
            console.log(">>>>>",self.env.config && self.env.config.actionId,session.module_action_id)
            if(!session.main_admin && self.env.config && self.env.config.actionId == session.module_action_id){
                $('.o_filter_menu').remove()
            }
        });
    }
});

