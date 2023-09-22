/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';

registerPatch({
    name: 'Partner',
        recordMethods: {
            /**
             * @override
             */
            async getChat() {
                if (!this.user && !this.hasCheckedUser) {
                    await this.checkIsUser();
                    if (!this.exists()) {
                        return;
                    }
                }
                // prevent chatting with non-users

                if (!this.user) {
                    let chat = this.dmChatWithCurrentPartner;
                    if (!chat || !chat.thread.isPinned) {
                        // if chat is not pinned then it has to be pinned client-side
                        // and server-side, which is a side effect of following rpc
                        chat = await this.messaging.models['Channel'].performRpcCreateChat({
                            partnerIds: [this.id],
                        });
                        if (!this.exists()) {
                            return;
                        }
                    }
                    if (!chat) {
                        this.messaging.notify({
                        message: this.env._t("An unexpected error occurred during the creation of the chat."),
                        type: 'warning',
                    });
                        return;
                    }
                    return chat;
                }
                return this.user.getChat();
             },
      },
        fields: {
            send_template_req: attr(),
            isWhatsappUser: attr(),
            not_send_msgs_btn_in_chatter: attr(),
            not_wa_msgs_btn_in_chatter: attr(),
//            not_send_msgs_btn_in_chatter: many2many('ir.model', {
//            }),
//            not_wa_msgs_btn_in_chatter: many2many('ir.model', {
//            })
        },
});