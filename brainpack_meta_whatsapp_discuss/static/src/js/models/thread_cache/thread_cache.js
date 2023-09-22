/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";
import { attr, many, one } from '@mail/model/model_field';


registerPatch({
    name: 'ThreadCache',
    fields: {
        orderedNonEmptyMessages: {
            compute() {
                if(this.thread.isWaMsgs && !this.thread.isChatterWa){
                    return this.orderedMessages.filter(message => !message.isEmpty && message.message_type=='wa_msgs');
                }
                else{
                    return this.orderedMessages.filter(message => !message.isEmpty && message.message_type!='wa_msgs');
                }
            }
            },
        }
});