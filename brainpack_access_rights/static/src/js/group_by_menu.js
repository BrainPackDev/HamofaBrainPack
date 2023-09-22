/** @odoo-module **/
var { patch } = require("web.utils");
//import {StudioSystray} from "@web_studio/systray_item/systray_item";;
import { GroupByMenu } from "@web/search/group_by_menu/group_by_menu";
import { useSubEnv, useState, useRef, useEffect, onMounted } from "@odoo/owl";
import rpc from 'web.rpc';
import { session } from "@web/session";

patch(GroupByMenu.prototype, "brainpack_access_rights.GroupByMenu", {
    setup() {
        this._super();
        var self = this
        onMounted(() => {
            if(!session.main_admin && self.env.config && self.env.config.actionId == session.module_action_id){
                $('.o_group_by_menu').remove()
            }
        });
    }
});

