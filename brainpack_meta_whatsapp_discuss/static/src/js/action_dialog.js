
/** @odoo-module **/

import { ActionDialog } from "@web/webclient/actions/action_dialog";
import { patch } from "@web/core/utils/patch";
import { useComponent, Component, onMounted, onWillUnmount,onPatched, useEffect, useRef } from "@odoo/owl";
//import { Component, onMounted, onWillUnmount, useExternalListener, useState, xml } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { DebugMenu } from "@web/core/debug/debug_menu";
import { useOwnDebugContext } from "@web/core/debug/debug_context";
import { useLegacyRefs } from "@web/legacy/utils";
//import { WaThreadView } from "@brainpack_meta_whatsapp_discuss/js/wa_thread_view";
var Widget = require('web.Widget');
const LEGACY_SIZE_CLASSES = {
    "extra-large": "modal-xl",
    large: "modal-lg",
    small: "modal-sm",
};
var core = require('web.core');
var QWeb = core.qweb;
import { ClientActionAdapter, ViewAdapter } from "@web/legacy/action_adapters";
import { useUpdate } from '@mail/component_hooks/use_update';

patch(ActionDialog.prototype, 'brainpack_meta_whatsapp_discuss/static/src/js/action_dialog.js', {
    setup() {
//        super.setup();
        this._super();
        useOwnDebugContext();
        useEffect(
            () => {
                if (this.modalRef.el.querySelector(".modal-footer").childElementCount > 1) {
                    const defaultButton = this.modalRef.el.querySelector(
                        ".modal-footer button.o-default-button"
                    );
                    defaultButton.classList.add("d-none");
                }
            },
            () => []
        );
        onMounted(() => this._mounted());
    },

     _mounted(){
            if(this.props.actionProps.context.main_form || $('#main-form-view').length > 0){
//                if(typeof(this.props.actionProps.context.main_form) == 'undefined' ){
//                    $('.back_btn').removeClass('o_hidden')
//                }
                if(this.modalRef && this.modalRef.el){
                    $('#main-form-view').html($(this.modalRef.el).find('.modal-body'));
                    $('#main-buttons-view').html($(this.modalRef.el).find('.modal-footer'));
                    $(document.body).find('.o_dialog_container').hide();
//                $(document.body).find('.o_effects_manager').after('<div class="o_dialog_container"></div>');
                }

            }
        }
});
