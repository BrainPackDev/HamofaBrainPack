/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';

registerPatch({
    name: 'Thread',
        fields: {
             messagefailed: many("MessageFailed", {
                inverse: 'thread',
            }),
        },
        recordMethods: {
         async refreshMessagefailed() {
            var id = this.id;
            var model = this.model;

            const messagefailedData = await this.messaging.rpc(
                {
                    model: "mail.message",
                    method: "get_failed_messsage_info",
                    args: [id, model],
                },
                {
                    shadow: true,
                }
            );

//            const messagefailedData = await this.async(() =>
//                this.env.services.rpc(
//                    {
//                        model: "mail.message",
//                        method: "get_failed_messsage_info",
//                        args: [id, model],
//                    },
//                    {
//                        shadow: true,
//                    }
//                )
//            );
            const messagefailed = this.messaging.models["MessageFailed"].insert(
                messagefailedData.map((messageData) =>
                    this.messaging.models["MessageFailed"].convertData(
                        messageData
                    )
                )
            );
            this.update({
                messagefailed: [["replace", messagefailed]],
            });
        },

        _computeFetchMessagesUrl() {
            switch (this) {
                case this.messaging.failedmsg:
                    return "/mail/failed/messages";
            }
            return this._super();
        },
        },
});
