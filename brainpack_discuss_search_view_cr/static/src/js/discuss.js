/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';

registerPatch({
    name: 'Discuss',
    fields: {
        searchMessageId: attr({default: false}),
        searchMessage: attr({default: false}),
        messageFilter:  attr({default: false}),
        searchUpDown: attr({default: false}),
        upDisable: attr({default: true}),
        downDisable: attr({default: true}),
        stringifiedDomain: attr(),
        searchString: attr({default:''}),
        currentSearchCount: attr({default: 0,}),
        numberOfSearch: attr({default: 0,}),
    },
});