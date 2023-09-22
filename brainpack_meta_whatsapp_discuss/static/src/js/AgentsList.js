/** @odoo-module **/

const { Component, onWillUnmount, onWillUpdateProps, useState } = owl;
const rpc = require('web.rpc');
var session = require('web.session');
var ajax = require('web.ajax');


export class AgentsList extends Component{
     counter1 = useState({ value: 0 ,});

    setup() {
        super.setup();
        var threads = this.env.services.messaging.modelManager.models['Thread'].all().filter(thread => thread.localId == this.env.services.messaging.modelManager.messaging.wa_thread_view.props.threadViewLocalId);
        this.WaThreadView.thread = threads[0];
    }

    constructor(WaThreadView) {
        super(...arguments);
        var self=this;
        this.WaThreadView = WaThreadView;

        self.users = []
        self.agents = []
        rpc.query({
                model: 'mail.channel',
                method: 'get_channel_agent',
                args: [[], this.WaThreadView.WaThreadView.waThreadView.id],
            }).then(function (result) {
                $('#main-button').addClass('o_hidden');

                self.users = result['users']
                self.agents = result['channel_users']
                self.counter1.value++;
            });
    }
    _addAgent(){
        var self = this;
        var user_id = $("#user").val()

        rpc.query({
                model: 'mail.channel',
                method: 'add_agent',
                args: [[], user_id, this.WaThreadView.WaThreadView.waThreadView.id],
            }).then(function (result) {
                if(result){
                    self.WaThreadView.WaThreadView.tab_agent()
                }
            });
    }

     _removeAgent(){
        var self = this
        var user_id = parseInt(event.currentTarget.dataset.id)

        rpc.query({
                model: 'mail.channel',
                method: 'remove_agent',
                args: [[], user_id, this.WaThreadView.WaThreadView.waThreadView.id],
            }).then(function (result) {
                if(result){
                    self.WaThreadView.WaThreadView.tab_agent()
                }
            });
     }
}
AgentsList.template = "AgentsList";

