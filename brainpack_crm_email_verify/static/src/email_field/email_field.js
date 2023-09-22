/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { EmailField } from "@web/views/fields/email/email_field";
import { Component, onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import rpc from 'web.rpc';

class VerifyEmailField extends EmailField {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            verify: false,
            email_field:this.props.value,
        });
        onMounted(() => {
            var sub_str = ''
            if((this.props.value.length - this.props.show_digit) > 0){
                for(var i = 0;i<this.props.value.length - this.props.show_digit;i++){
                    sub_str = sub_str + 'X'
                }
             }
            this.state.email_field = this.props.value.substring(0, this.props.show_digit) + sub_str
        });
    }
    openReasonWizard(){
        var self = this
        return this.env.model.actionService.doAction({
                type: 'ir.actions.act_window',
                name: 'Reason',
                res_model: 'verify.email.reason',
                views: [[false, 'form']],
                view_mode: 'form',
                target: 'new',
                context: {
                    'active_id': self.env.model.__bm_load_params__.res_id,
                    'default_email': this.props.value,
                }
            },{
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
VerifyEmailField.template = "web.VerifyEmailField";

VerifyEmailField.defaultProps= {
        ...EmailField.defaultProps,
        verifyButton: true,
        show_digit:5,
    };

VerifyEmailField.props = {
    ...standardFieldProps,
    placeholder: { type: String, optional: true },
    verifyButton: { type: Boolean, optional: true },
    show_digit: { type: Number, optional: true },
};

VerifyEmailField.extractProps = ({ attrs }) => {
    return {
       verifyButton: attrs.options.enable_verify,
       placeholder: attrs.placeholder,
       show_digit: attrs.options.show_digit,
    };
};

registry.category("fields").add("verifyemail", VerifyEmailField);
