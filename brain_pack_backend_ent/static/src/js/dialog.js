/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { useEffect } from "@odoo/owl";
var { patch } = require("web.utils");

patch(Dialog.prototype, "brain_pack_backend_ent.DialogJS", {
    setup() {
        this._super();
        // MAKE ANY MODAL DRAGGABLE
        useEffect(
            (el) => {
                if (el) {
                    let $modal = $(el);
                    $modal.draggable({
                        handle: ".modal-header",
                    });
                    var width = $modal.find('.modal-content').width();
                    var height = $modal.find('.modal-content').height();
                    $modal.find('.modal-content').resizable({
                        minWidth: width,
                        minHeight: height,
                    });
                }
            },
            () => [this.modalRef.el]
        );
    }
});
