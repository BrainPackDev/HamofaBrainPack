/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

patch(Dialog.prototype, "brainpack_debranding.Dialog", {
    setup() {
        this._super.apply(this, arguments);
        const app_system_name = session.app_system_name || "BrainPack";
        this.title = app_system_name;
        this.props.title = app_system_name;
        owl.onMounted(() => {
            this.setDrag();
            var $dl = $('#' + this.id + ' .modal-dialog .modal-content');
            if($dl){
                if($('#' + this.id + ' .modal-dialog .modal-content').find('td[name="new_passwd"]').length > 0){
                    $('#' + this.id + ' .modal-dialog .modal-content').find('td[name="new_passwd"]').trigger('click');
                }
            }
        });
    },
    setDrag() {
        var $dl = $('#' + this.id + ' .modal-dialog .modal-content');
        if ($dl)
            $dl.draggable({
                handle: ".modal-header"
            });
    },
});

