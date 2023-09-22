/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';

registerPatch({
    name: 'MessagingNotificationHandler',
    recordMethods: {
        _notifyThreadViewsMessageReceived(message) {
          this._super(...arguments);
          for (const thread of message.threads) {
            for (const threadView of thread.threadViews) {
                threadView.receivedMessage(message);
            }
          }
        },
    },
});