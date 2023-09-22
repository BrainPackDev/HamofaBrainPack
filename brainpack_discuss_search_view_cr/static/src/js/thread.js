/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';

registerPatch({
    name: 'Thread',
    fields: {
        fetchMessagesParams: {
            compute() {
                let stringifiedDomain = "[]";
                let messageFilter = false
                for (const threadView of this.threadViews) {
                  if (threadView.stringifiedDomain && threadView.stringifiedDomain != "[]") {
                    stringifiedDomain = threadView.stringifiedDomain;
                    messageFilter = threadView.messageFilter;
                  }
                }
                if (stringifiedDomain != "[]") {
                  stringifiedDomain = JSON.parse(stringifiedDomain);
                }
                if (this.model === 'mail.channel') {
                    if(stringifiedDomain == "[]"){
                        return { 'channel_id': this.id };
                    }
                    return { 'channel_id': this.id ,'stringifiedDomain':stringifiedDomain,'messageFilter':messageFilter};
                }
                if (this.mailbox) {
                    if(stringifiedDomain != "[]"){
                        return {
                            'stringifiedDomain':stringifiedDomain,'messageFilter':messageFilter
                        };
                    }
                    return {}
                }
                if(stringifiedDomain != "[]"){
                    return {
                        'thread_id': this.id,
                        'thread_model': this.model,
                        'stringifiedDomain':stringifiedDomain,'messageFilter':messageFilter
                    };
                }
                return {
                    'thread_id': this.id,
                    'thread_model': this.model,
                };
            },
        },
    },
});