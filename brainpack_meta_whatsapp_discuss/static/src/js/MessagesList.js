/** @odoo-module **/

const { Component, onWillUnmount, onWillUpdateProps, useState } = owl;
const rpc = require('web.rpc');
var session = require('web.session');
var ajax = require('web.ajax');

//<!-- Start Pre Send WhatsApp Templates-->
export class MessagesList extends Component {
    counter1 = useState({ value: 0 ,});

    constructor(WaThreadView) {
        super(...arguments);
        var self=this;
        this.WaThreadView = WaThreadView
        self.message_list = []
        var partner_id
        if(this.WaThreadView.WaThreadView.props.partnerId){
            partner_id = this.WaThreadView.WaThreadView.props.partnerId
        }
        rpc.query({
                model: 'wa.template',
                method: 'search_read',
                args: [[
                        ['model','=', 'res.partner'],
                        ['state', '=', 'added'],
                    ]],
                fields : ['id', 'name']
            }).then(function (result) {
//                var self=this;
                $('#main-button').addClass('o_hidden');
                self.message_list = result
                self.counter1.value++;
            });
    }

    _send_premessage(id){
      var self=this;
      var partner_id
      if(this.WaThreadView.WaThreadView.props.partnerId){
        partner_id = this.WaThreadView.WaThreadView.props.partnerId
      }
        ajax.jsonRpc('/send/pre/message', 'call', {
                'partner_id':partner_id,
                'template_id': id,
        }).then(function (result) {
            if(result){
                self.WaThreadView.WaThreadView.tab_message_templates()
            }
        });
    }
}
MessagesList.template = "MessagesList";
//<!-- End Pre Send WhatsApp Templates-->