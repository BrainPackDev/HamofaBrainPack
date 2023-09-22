/** @odoo-module **/
import { registerPatch } from "@mail/model/model_core";
import { attr, many, one } from '@mail/model/model_field';
import { clear, link } from '@mail/model/model_field_command';
import { addLink, escapeAndCompactTextContent, parseAndTransform } from '@mail/js/utils';
const { Component, onWillUnmount, onWillUpdateProps, useState } = owl;
import { sprintf } from '@web/core/utils/strings';

registerPatch({
    name: 'ComposerView',
        recordMethods: {

            async openFullComposer() {
                var action;
//                if(this.composer.composerViews && this.composer.composerViews[0].chatter && this.composer.composerViews[0].chatter.isWaComposerView){
                if(this.composer && this.composer.thread && this.composer.thread.isWaMsgs){
                    const attachmentIds = this.composer.attachments.map(attachment => attachment.id);
                    const context = {
                        default_attachment_ids: attachmentIds,
                        default_model: this.composer.activeThread.model,
                        default_partner_ids: this.composer.recipients.map(partner => partner.id),
                        default_res_id: this.composer.activeThread.id,
                    };

                    action = {
                        type: 'ir.actions.act_window',
                        res_model: 'wa.compose.message',
                        view_mode: 'form',
                        views: [[false, 'form']],
                        target: 'new',
                        context: context,
                    };
                }
                else{
                    const attachmentIds = this.composer.attachments.map(attachment => attachment.id);
                    const context = {
                        default_attachment_ids: attachmentIds,
                        default_body: escapeAndCompactTextContent(this.composer.textInputContent),
                        default_is_log: this.composer.isLog,
                        default_model: this.composer.activeThread.model,
                        default_partner_ids: this.composer.recipients.map(partner => partner.id),
                        default_res_id: this.composer.activeThread.id,
                        mail_post_autofollow: this.composer.activeThread.hasWriteAccess,
                    };


                    action = {
                        type: 'ir.actions.act_window',
                        res_model: 'mail.compose.message',
                        view_mode: 'form',
                        views: [[false, 'form']],
                        target: 'new',
                        context: context,
                    };
                }
                const composer = this.composer;
                const options = {
                    onClose: () => {
                        if (!composer.exists()) {
                            return;
                        }
                        composer._reset();
                        if (composer.activeThread) {
                            composer.activeThread.fetchData(['messages']);
                        }
                    },
                };
                await this.env.services.action.doAction(action, options);
            },

            async postMessage() {
                const composer = this.composer;
                const postData1 = this._getMessageData();
                const escapedAndCompactContent = escapeAndCompactTextContent(composer.textInputContent);
                let body = escapedAndCompactContent.replace(/&nbsp;/g, ' ').trim();
                // This message will be received from the mail composer as html content
                // subtype but the urls will not be linkified. If the mail composer
                // takes the responsibility to linkify the urls we end up with double
                // linkification a bit everywhere. Ideally we want to keep the content
                // as text internally and only make html enrichment at display time but
                // the current design makes this quite hard to do.
                body = this._generateMentionsLinks(body);
                body = parseAndTransform(body, addLink);
                body = this._generateEmojisOnHtml(body);
                let postData;
                debugger;
                if(composer.thread.isWaMsgs && this.isInDiscuss == false && this.isInChatWindow == false){
                    postData = {
                        attachment_ids: composer.attachments.map(attachment => attachment.id),
                        body,
                        message_type: 'wa_msgs',
                        partner_ids: composer.recipients.map(partner => partner.id),
                    };
                }
                else if(composer.thread.isWaMsgs && this.isInDiscuss == true && composer.thread.channel && composer.thread.channel.channel_type === 'chat'){
                    postData = {
                        attachment_ids: composer.attachments.map(attachment => attachment.id),
                        body,
                        message_type: 'wa_msgs',
                        partner_ids: composer.recipients.map(partner => partner.id),
                    };
                }
                else if(composer.thread.isWaMsgs && this.isInChatWindow == true && composer.thread.channel && composer.thread.channel.channel_type === 'chat'){
                    postData = {
                        attachment_ids: composer.attachments.map(attachment => attachment.id),
                        body,
                        message_type: 'wa_msgs',
                        partner_ids: composer.recipients.map(partner => partner.id),
                    };
                }
                else if(composer.thread.isWaMsgs && this.isInChatWindow == true && composer.thread.channel && composer.thread.channel.channel_type === 'channel'){
                    postData = {
                        attachment_ids: composer.attachments.map(attachment => attachment.id),
                        body,
                        message_type: 'comment',
                        partner_ids: composer.recipients.map(partner => partner.id),
                    };
                }
                else{
                    postData = {
                        attachment_ids: composer.attachments.map(attachment => attachment.id),
                        body,
                        message_type: 'comment',
                        partner_ids: composer.recipients.map(partner => partner.id),
                    };
                }
                const params = {
                    'post_data': postData,
                    'thread_id': composer.thread.id,
                    'thread_model': composer.thread.model,
                };
                try {
                    composer.update({ isPostingMessage: true });
                    if (composer.thread.model === 'mail.channel') {
                        Object.assign(postData, {
                            subtype_xmlid: 'mail.mt_comment',
                        });
                    } else {
                        Object.assign(postData, {
                            subtype_xmlid: composer.isLog ? 'mail.mt_note' : 'mail.mt_comment',
                        });
                        if (!composer.isLog) {
                            params.context = { mail_post_autofollow: this.composer.activeThread.hasWriteAccess };
                        }
                    }
                    if (this.threadView && this.threadView.replyingToMessageView && this.threadView.thread !== this.messaging.inbox.thread) {
                        postData.parent_id = this.threadView.replyingToMessageView.message.id;
                    }
                    if(postData.message_type == 'wa_msgs'){
                        params.context = { mail_post_autofollow: this.composer.activeThread.hasWriteAccess };
                    }
                    const { threadView = {} } = this;
                    const chatter = this.chatter;
                    const { thread: chatterThread } = this.chatter || {};
                    const { thread: threadViewThread } = threadView;
                    // Keep a reference to messaging: composer could be
                    // unmounted while awaiting the prc promise. In this
                    // case, this would be undefined.
                    const messaging = this.messaging;
                    const messageData = await this.messaging.rpc({ route: `/mail/message/post`, params });
                    if (!messaging.exists()) {
                        return;
                    }
                    const message = messaging.models['Message'].insert(
                        messaging.models['Message'].convertData(messageData)
                    );
                    if (messaging.hasLinkPreviewFeature && !message.isBodyEmpty) {
                        messaging.rpc({
                            route: `/mail/link_preview`,
                            params: {
                                message_id: message.id
                            }
                        }, { shadow: true });
                    }
                    for (const threadView of message.originThread.threadViews) {
                        // Reset auto scroll to be able to see the newly posted message.
                        threadView.update({ hasAutoScrollOnMessageReceived: true });
                        threadView.addComponentHint('message-posted', { message });
                    }
                    if (chatter && chatter.exists() && chatter.hasParentReloadOnMessagePosted) {
                        chatter.reloadParentView();
                    }
                    if (chatterThread) {
                        if (this.exists()) {
                            this.delete();
                        }
                        if (chatterThread.exists()) {
                            // Load new messages to fetch potential new messages from other users (useful due to lack of auto-sync in chatter).
                            chatterThread.fetchData(['followers', 'messages', 'suggestedRecipients']);
                        }
                    }
                    if (threadViewThread) {
                        if (threadViewThread === messaging.inbox.thread) {
                            messaging.notify({
                                message: sprintf(messaging.env._t(`Message posted on "%s"`), message.originThread.displayName),
                                type: 'info',
                            });
                            if (this.exists()) {
                                this.delete();
                            }
                        }
                        if (threadView && threadView.exists()) {
                            threadView.update({ replyingToMessageView: clear() });
                        }
                    }
                    if (composer.exists()) {
                        composer._reset();
                    }
                } finally {
                    if (composer.exists()) {
                        composer.update({ isPostingMessage: false });
                    }
                }
            },

        },
});

/**
 * Here we have registerPatch for Composer to solved message undefined issue in Chat & discuss in odoo v16
 * also, add custom placeholder for both send message and whatsapp message button at sidebar
 */
registerPatch({
    name: 'Composer',
        fields: {
            placeholder: {
                compute() {
                    if (!this.thread) {
                        return "";
                    }
                    if (this.thread.channel) {
                        if (this.thread.channel.correspondent) {
                            return sprintf(this.env._t("Message %s..."), this.thread.channel.correspondent.persona.partner.nameOrDisplayName);
                        }
                        return sprintf(this.env._t("Message #%s..."), this.thread.displayName);
                    }
                    if (this.isLog) {
                        return this.env._t("Log an internal note...");
                    }
                    if (this.thread.isWaMsgs) {
                        return this.env._t("Send a WhatsApp Message...");
                    }
                    return this.env._t("Send a message to followers...");
                },
            },
        },
});