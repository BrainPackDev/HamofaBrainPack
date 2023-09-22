/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { PhoneField } from "@web/views/fields/phone/phone_field";
import { Component, onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import rpc from 'web.rpc';

class VerifyPhoneField extends PhoneField {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            verify: false,
            phone_field:this.props.value,
        });
        onMounted(() => {
            var sub_str = ''
            if((this.props.value.length - this.props.show_digit) > 0){
                for(var i = 0;i<this.props.value.length - this.props.show_digit;i++){
                    sub_str = sub_str + 'X'
                }
             }
            this.state.phone_field = this.props.value.substring(0, this.props.show_digit) + sub_str
        });
    }
    async openReasonWizard(){
        var self = this
        await this.env.model.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Reason',
            res_model: 'verify.phone.reason',
            views: [[false, 'form']],
            view_mode: 'form',
            target: 'new',
            context: {
                'active_id': self.env.model.__bm_load_params__.res_id,
                'default_phone': this.props.value,
            }
            }, {
                props: {
                    onSave: (record, params) => {
                        self.env.model.root.save();
                        self.env.model.root.load();
                        self.state.verify = true
                    }
                }
            }
        );
    }
}
VerifyPhoneField.template = "web.VerifyPhoneField";

VerifyPhoneField.defaultProps= {
        ...PhoneField.defaultProps,
        verifyButton: true,
        show_digit:5,
    };

VerifyPhoneField.props = {
    ...standardFieldProps,
    placeholder: { type: String, optional: true },
    enableButton: { type: Boolean, optional: true },
    verifyButton: { type: Boolean, optional: true },
    show_digit: { type: Number, optional: true },
};

VerifyPhoneField.extractProps = ({ attrs }) => {
    return {
       verifyButton: attrs.options.enable_verify,
       enableButton: attrs.options.enable_sms,
       placeholder: attrs.placeholder,
       show_digit: attrs.options.show_digit,
    };
};

registry.category("fields").add("verifyphone", VerifyPhoneField);
