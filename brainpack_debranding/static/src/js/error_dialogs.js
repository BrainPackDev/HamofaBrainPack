/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import {ClientErrorDialog,ErrorDialog,NetworkErrorDialog,RPCErrorDialog} from "@web/core/errors/error_dialogs";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

patch(ErrorDialog.prototype, "brainpack_debranding.ErrorDialog", {
    setup() {
        this._super.apply(this, arguments);
        const app_system_name = session.app_system_name || "BrainPack Error";
        this.title = app_system_name;
        this.constructor.title = app_system_name;
        if(this.props && this.props.data && this.props.data.debug){
            this.props.data.debug=this.props.data.debug.replaceAll('odoo',app_system_name)
        }

    },
});

patch(ClientErrorDialog.prototype, "brainpack_debranding.ClientErrorDialog", {
    setup() {
        this._super.apply(this, arguments);
        const app_system_name = session.app_system_name || "BrainPack Error";
        this.title = app_system_name;
        this.constructor.title = app_system_name;
        if(this.props && this.props.data && this.props.data.debug){
            this.props.data.debug=this.props.data.debug.replaceAll('odoo',app_system_name)
        }

    },
});

patch(NetworkErrorDialog.prototype, "brainpack_debranding.NetworkErrorDialog", {
    setup() {
        this._super.apply(this, arguments);
        const app_system_name = session.app_system_name || "BrainPack Error";
        this.title = app_system_name;
        this.constructor.title = app_system_name;
        if(this.props && this.props.data && this.props.data.debug){
            this.props.data.debug=this.props.data.debug.replaceAll('odoo',app_system_name)
        }

    },
});

patch(RPCErrorDialog.prototype, "brainpack_debranding.RPCErrorDialog", {
    setup() {
        this._super.apply(this, arguments);
        const app_system_name = session.app_system_name || "BrainPack Error";
        this.title = app_system_name;
        this.constructor.title = app_system_name;
        if(this.props && this.props.data && this.props.data.debug){
            this.props.data.debug=this.props.data.debug.replaceAll('odoo',app_system_name)
        }

    },
});

