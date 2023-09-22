/** @odoo-module **/

import { attr, many, one } from '@mail/model/model_field';
import { registerPatch } from '@mail/model/model_core';

registerPatch({
    name: 'Message',
        fields: {
            partner_trackings: attr(),
        },
        modelMethods: {
             convertData(data) {
                const data2 = this._super(data);
                if ("partner_trackings" in data) {
                    data2.partner_trackings = data.partner_trackings;
                }
                return data2;
            },
        },
        recordMethods: {
              hasPartnerTrackings() {
                return _.some(this.partner_trackings);
            },

            hasEmailCc() {
                return _.some(this._emailCc);
            },

            getPartnerTrackings: function () {
                if (!this.hasPartnerTrackings()) {
                    return [];
                }
                return this.partner_trackings;
            },
        },
});




//registerInstancePatchModel(
//    "mail.model",
//    "mail_tracking/static/src/js/mail_tracking.js",
//    {
//        hasPartnerTrackings() {
//            return _.some(this.__values.partner_trackings);
//        },
//
//        hasEmailCc() {
//            return _.some(this._emailCc);
//        },
//
//        getPartnerTrackings: function () {
//            if (!this.hasPartnerTrackings()) {
//                return [];
//            }
//            return this.__values.partner_trackings;
//        },
//    }
//);
