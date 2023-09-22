/** @odoo-module **/
var { patch } = require("web.utils");
import {FormController} from "@web/views/form/form_controller";
import {FormStatusIndicator} from "@web/views/form/form_status_indicator/form_status_indicator";
var session = require("@web/session");

import { Component, onWillStart, useEffect, useRef, onRendered, useState, onMounted } from "@odoo/owl";

//hide main admin seeting and access right groups and client admin group for client admin
patch(FormController.prototype, "brainpack_access_rights.FormController", {
     setup() {
        this._super();
        onMounted(() => {
            this.user.hasGroup("brainpack_access_rights.client_admin").then(function(result){
                if(result){
                    $('.o_horizontal_separator').each(function() {
                        if($(this).html() == 'Administration') {
                            $(this).parent().parent().remove()
                        }
                    });
                    $('.o_form_label').each(function() {
                        if($(this).html().trim().includes("Main Admin")){
                            $(this).parent().parent().parent().remove()
                        }
                        if($(this).html().trim().includes("Client Admin")){
                            $(this).parent().parent().parent().remove()
                        }
                    });
                }
            });
        });
     }
});
