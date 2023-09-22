/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { registerModel } from '@mail/model/model_core';
import { registerMessagingComponent } from '@mail/utils/messaging_component';
const { Component, onWillUnmount, onWillUpdateProps, useState,onMounted, useEffect } = owl;
import Dialog from 'web.Dialog';
import OwlDialog from 'web.OwlDialog';
import core from 'web.core';
import { AgentsList } from '@brainpack_meta_whatsapp_discuss/js/AgentsList';
import { MessagesList } from '@brainpack_meta_whatsapp_discuss/js/MessagesList';
const { ComponentWrapper, WidgetAdapterMixin } = require('web.OwlCompatibility');
import { attr, one } from '@mail/model/model_field';
import { clear } from '@mail/model/model_field_command';


export class WaThreadView extends Component {
    setup() {
        super.setup();
        this.messaging.wa_thread_view = this
        this.state = useState({
            nav_active:'partner'
        });
        onMounted(() => this._mounted());
    }
    _mounted(){
         if(this.state.nav_active == 'partner'){
            this.tabPartner();
        }
    }
    render(){
        super.render();
        if(this.state.nav_active == 'partner'){
            this.tabPartner();
        }
    }

    onClickBack(){
        if(this.state.nav_active == 'partner'){
            this.tabPartner();
        }
    }

    tabPartner(){
        var self= this
        this.state.nav_active = 'partner'
        if(self.waThreadView){
            if(self.messaging.discuss.thread.channel.correspondent.persona.partner){
                var partner = this.env.services['action'].doAction({
                    name: 'Partner',
                    type: 'ir.actions.act_window',
                    res_model: 'res.partner',
                    res_id: self.messaging.discuss.thread.channel.correspondent.persona.partner.id,
                    views: [[false, 'form']],
//                    main_form: true,
                    target: 'new',
                    context: {main_form: true, create: false},
                    flags: {mode: 'edit'},
                    options: {main_form: true,}
                });
            }
        }
        $('.main-button').removeClass('o_hidden');
        $('.back_btn').addClass('o_hidden');
    }

    tab_agent(){
        var self= this
        this.state.nav_active = 'agent'
        $('.main-button').addClass('o_hidden');
        $('#main-form-view').replaceWith("<div id='main-form-view'></div>")
        const AgentsListComponent = new ComponentWrapper(this, AgentsList, {'WaThreadView': this});
        AgentsListComponent.mount($('#main-form-view')[0]);
    }

    tab_message_templates(){
        var self= this
        this.state.nav_active = 'message_templates'
        $('.main-button').addClass('o_hidden');
        $('#main-form-view').replaceWith("<div id='main-form-view'></div>")
        const MessageWaListComponent = new ComponentWrapper(this, MessagesList, {'WaThreadView': this});
        MessageWaListComponent.mount($('#main-form-view')[0]);
    }

    get waThreadView() {
        var threads = this.messaging.models['Thread'].all().filter(thread => thread.localId == this.props.threadViewLocalId);
        return threads && threads[0];
    }

}

Object.assign(WaThreadView, {
    props: { threadViewLocalId: String, partnerId: Number, },
    template: 'brainpack_meta_whatsapp_discuss.WaThreadView',
});

registerMessagingComponent(WaThreadView);

registerPatch({
    name: 'Discuss',
    recordMethods: {
        waThreadView() {
            return this.messaging;
        },
    },
    fields: {
        hasWAThreadNav: attr({
            compute() {
                return Boolean(this.messaging.discuss.thread && this.messaging.discuss.thread.channel && this.messaging.discuss.thread.channel.channel_type && this.messaging.discuss.thread.channel.channel_type == 'chat');
            },
        }),
    },
});