/** @odoo-module **/

var config = require('web.config');
var core = require('web.core');
var session = require('@web/session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var { patch } = require("web.utils");
var { SwitchCompanyMenu } = require("@web/webclient/switch_company_menu/switch_company_menu");
var { registry } = require("@web/core/registry");
import { useSubEnv, useState, useRef, useEffect, onMounted } from "@odoo/owl";
import rpc from 'web.rpc';

var _t = core._t;

patch(SwitchCompanyMenu.prototype, "brain_pack_backend_ent.SwitchCompanyMenu", {
    setup() {
        this._super();
        this.isDebug = config.isDebug();
        this.isAssets = config.isDebug("assets");
        this.isTests = config.isDebug("tests");
        var self = this
        onMounted(() => {
            if(!session.session.main_admin){
                $('.debug_activator').remove()
                $('.o_debug_manager').remove()
                $('.dark_mode').remove()
            }
        });
    },
});

// show company menu even if company is count is 1 
const systrayItemSwitchCompanyMenu = {
    Component: SwitchCompanyMenu,
    isDisplayed(env) {
        const { availableCompanies } = env.services.company;
        return Object.keys(availableCompanies).length > 0;
    },
};

registry.category("systray").add("SwitchCompanyMenu", systrayItemSwitchCompanyMenu, { sequence: 1, force: true });