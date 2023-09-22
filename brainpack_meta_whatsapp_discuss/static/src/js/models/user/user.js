/** @odoo-module **/
import { registerPatch } from "@mail/model/model_core";
import { attr, many, one, many2many } from '@mail/model/model_field';
export const X2M_TYPES = ["one2many", "many2many"];
import { Many2ManyTagsField } from "@web/views/fields/many2many_tags/many2many_tags_field";

registerPatch({
    name: 'User',
        recordMethods: {
            /**
             * @override
             */
            async getChat() {
                if (!this.user && !this.hasCheckedUser) {
                    await this.partner.checkIsUser();
                    if (!this.exists()) {
                        return;
                    }
                }
                // prevent chatting with non-users

                if (!this.user) {
    ////                    var threads = this.messaging.models['Thread'].all().filter(thread => thread.localId==this.props.localId);
    //                    let chat = this.messaging.models['Thread'].all().filter(thread =>
    //                    thread.channel_type === 'chat' &&
    //                    thread.correspondent === this &&
    //                    thread.model === 'mail.channel' &&
    //                    thread.public === 'private'
    //                );
                    let chat = this.partner.dmChatWithCurrentPartner;
                    if (!chat || !chat.thread.isPinned) {
                        // if chat is not pinned then it has to be pinned client-side
                        // and server-side, which is a side effect of following rpc
                        chat = await this.messaging.models['Channel'].performRpcCreateChat({
                            partnerIds: [this.partner.id],
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
            isWhatsappUser: attr(),
            not_send_msgs_btn_in_chatter: attr(),
            not_wa_msgs_btn_in_chatter: attr(),
        },
});