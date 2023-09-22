/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";
import { attr, many, one } from '@mail/model/model_field';
import { clear, insert, link } from '@mail/model/model_field_command';

registerPatch({
    name: 'Chatter',
        fields: {
            isWaComposerView: attr({
                default: true,
            }),
            isShowSendMessage: attr({
                compute() {
                     if(this.messaging && this.messaging.currentUser){
                        var lst = this.messaging.currentPartner.not_send_msgs_btn_in_chatter.filter(r => r.model == this.threadModel)
                        if(lst.length > 0){
                            return false
                        }
                    }
                    return true
                },
            }),
            isShowWaSendMessage: attr({
                compute() {
                    if(this.messaging && this.messaging.currentUser){
                        var lst = this.messaging.currentPartner.not_wa_msgs_btn_in_chatter.filter(r => r.model == this.threadModel)
                        if(lst.length > 0){
                            return false
                        }
                    }
                    return true
                },
            }),
        },
        recordMethods: {
            _created() {
                this._super()
                this.onClickWaSendMessage = this.onClickWaSendMessage.bind(this);
            },
            onClickWaSendMessage(ev){
                if (this.composerView && !this.composerView.composer.isLog) {
                    this.update({ composerView: clear() });
                    this.thread.update({isWaMsgs:false})
                    this.thread.update({isChatterWa:false})
                } else {
                    this.showWaSendMessage();
                }
            },
            onClickSendMessage(ev) {
                this._super(ev)
                this.thread.update({isWaMsgs:false})
                this.thread.update({isChatterWa:false})
            },
            showWaSendMessage() {
                this.update({ composerView: {isWaComposerView:true} });
                this.composerView.composer.update({ isLog: false });
                this.thread.update({isWaMsgs:true})
                this.thread.update({isChatterWa:true})
                this.focus();
            },
            showSendMessage() {
                this.update({ composerView: {isWaComposerView:false} });
                this.composerView.composer.update({ isLog: false });
                this.thread.update({isWaMsgs:false})
                this.thread.update({isChatterWa:false})
                this.focus();
            },
            showLogNote() {
                this.update({ composerView: {isWaComposerView:false} });
                this.composerView.composer.update({ isLog: true });
                this.thread.update({isWaMsgs:false})
                this.thread.update({isChatterWa:false})
                this.focus();
            },
            _computeshowWaSendMessage(){
                if(this.messaging && this.messaging.currentUser){
                    var lst = this.messaging.currentPartner.not_wa_msgs_btn_in_chatter.filter(r => r.model == this.threadModel)
                    if(lst.length > 0){
                        return false
                    }
                }
                return true
            },
            _computeshowSendMessage(){
                 if(this.messaging && this.messaging.currentUser){
                    var lst = this.messaging.currentPartner.not_send_msgs_btn_in_chatter.filter(r => r.model == this.threadModel)
                    if(lst.length > 0){
                        return false
                    }
                }
                return true
            },
         },
});