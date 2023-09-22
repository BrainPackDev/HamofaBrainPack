odoo.define('brain_pack_backend_ent.BrainPackPageTitle', function (require) {
"use strict";

    var ajax = require('web.ajax');
    var { WebClient } = require("@web/webclient/webclient");
    var { patch } = require("web.utils");

    patch(WebClient.prototype, "brain_pack_backend_ent.BrainPackPageTitle", {
        setup() {
            this._super();
            var self = this
            ajax.rpc('/get/tab/title/').then(function(rec) {
                var new_title = rec
                self.title.setParts({ zopenerp: new_title })
            })
        },
    });
});