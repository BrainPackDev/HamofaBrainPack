/** @odoo-module **/

import { Composer } from '@mail/components/composer/composer';
import { patch } from 'web.utils';
const rpc = require('web.rpc');
const { Component, onWillUnmount, onWillUpdateProps, useState } = owl;

patch(Composer.prototype, 'brainpack_meta_whatsapp/static/src/js/components/composer/composer.js', {
    setup() {
        this._super();
        this.state = useState({ send_template_req: true ,});
    },
    render(){
        this._super();
        var self = this
        if(self && self.composerView && self.composerView.localId && self.composerView.composer && self.composerView.composer.thread && self.composerView.composer.thread.isWaMsgs && self.composerView.composer.thread.id && self.composerView.composer.thread.model){
            rpc.query({
                    model: 'mail.thread',
                    method: 'get_template_req_val',
                    args: [[], this.composerView.composer.thread.id,this.composerView.composer.thread.model],
                }).then(function (result) {
                    self.state.send_template_req = result
                });
        }
    }
});