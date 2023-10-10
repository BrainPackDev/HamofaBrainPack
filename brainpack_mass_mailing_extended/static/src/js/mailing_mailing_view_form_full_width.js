/** @odoo-module **/

var { patch } = require("web.utils");
import {MassMailingFullWidthViewController} from "@mass_mailing/js/mailing_mailing_view_form_full_width";

patch(MassMailingFullWidthViewController.prototype, "brainpack_mass_mailing_extended.MassMailingFullWidthViewController", {
    _repositionMailingEditorSidebar() {
        const windowHeight = $(window).height();
        if(this.$iframe){
            const $iframeDocument = this.$iframe.contents();
            const $sidebar = $iframeDocument.find('#oe_snippets');
            const isFullscreen =  this._isFullScreen();
            if (isFullscreen) {
                $sidebar.height(windowHeight);
                this.$iframe.height(windowHeight);
                $sidebar.css({
                    top: '',
                    bottom: '',
                });
            } else {
                const iframeTop = this.$iframe.offset().top;
                $sidebar.css({
                    height: '',
                    top: Math.max(0, $('.o_content').offset().top - iframeTop),
                    bottom: this.$iframe.height() - windowHeight + iframeTop,
                });
            }
        }
    }
});