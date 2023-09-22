/** @odoo-module **/
var { patch } = require("web.utils");
//import {StudioSystray} from "@web_studio/systray_item/systray_item";
var { systrayItem } = require("@web_studio/systray_item/systray_item");
import { useSubEnv, useState, useRef, useEffect, onMounted } from "@odoo/owl";
import rpc from 'web.rpc';
import { session } from "@web/session";

patch(systrayItem.Component.prototype, "brainpack_access_rights.StudioSystray", {
    setup() {
        this._super();
        var self = this
        onMounted(() => {
             if(!session.main_admin){
                $(self.rootRef.el).remove()
             }
//          rpc.query({
//                model: 'res.company',
//                method: 'get_hide_studio',
//                args: [[]],
//            }).then(function (res) {
//                if(!res){
//                    $(self.rootRef.el).remove()
//                }
//            });
        });
    }
});

