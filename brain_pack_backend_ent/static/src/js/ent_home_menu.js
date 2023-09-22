/** @odoo-module **/
import { HomeMenu } from "@web_enterprise/webclient/home_menu/home_menu";
var { patch } = require("web.utils");
var ajax = require('web.ajax');
import { session } from "@web/session";

patch(HomeMenu.prototype, "brain_pack_backend_ent.entHomeMenuJs", {
    setup() {
        $('body').addClass('d-none');
        this._super();
        console.log(">>>>>",session)
        this.company = session.company_id
        var apps = this.props.apps
        var rec_ids = []
        apps.map(app => rec_ids.push(app.id))
            ajax.jsonRpc('/get/irmenu/icondata','call', {
                'menu_ids':rec_ids,
            }).then(function(rec) {
            $.each(apps, function( key, value ) {
                var target_tag = '.container a.o_app[id=result_app_'+key+']'
                var $tagtarget = $(target_tag)
                $tagtarget.find('.app-image').empty()

                var current_record = rec[value.id][0]
                value.id = current_record.id
                value.use_icon = current_record.use_icon
                value.icon_class_name = current_record.icon_class_name
                value.icon_img = current_record.icon_img

                if (current_record.use_icon) {
                    if (current_record.icon_class_name) {
                        var icon_span = "<span class='ri "+current_record.icon_class_name+"'/>"
                        $tagtarget.find('.app-image').append($(icon_span))
                    } else if (current_record.icon_img) {
                        var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+current_record.id+"/icon_img' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    } else if (current_record.web_icon_data != false) {
                        var icon_data = current_record.web_icon.split('/icon.')
                        if (icon_data[1] == 'svg'){
                            var web_svg_icon = current_record.web_icon.replace(',', '/')
                            var icon_image = "<img class='img img-fluid' src='"+web_svg_icon+"' />"
                        } else{
                            var icon_image = "<img class='img img-fluid' src='data:image/"+icon_data[1]+";base64,"+current_record.web_icon_data+"' />"
                        }
                        $tagtarget.find('.app-image').append($(icon_image))
                    } else if(current_record.web_icon){
                        var icon_data = current_record.web_icon.split(',')
                        var icon_span = "<span class='"+icon_data[0]+"'style='background-color:"+icon_data[2]+"; color: "+icon_data[1]+" '/>"
                        $tagtarget.find('.app-image').append($(icon_span))
                    } else {
                        var icon_image = "<img class='img img-fluid' src='/brain_pack_backend_ent/static/description/bizople-icon.png' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    }
                } else {
                    if (current_record.icon_img) {
                        var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+current_record.id+"/icon_img' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    } else if (current_record.web_icon_data != false) {
                        var icon_data = current_record.web_icon.split('/icon.')
                        if (icon_data[1] == 'svg'){
                            var web_svg_icon = current_record.web_icon.replace(',', '/')
                            var icon_image = "<img class='img img-fluid' src='"+web_svg_icon+"' />"
                        } else{
                            var icon_image = "<img class='img img-fluid' src='data:image/"+icon_data[1]+";base64,"+current_record.web_icon_data+"' />"
                        }
                        $tagtarget.find('.app-image').append($(icon_image))
                    }  else if(current_record.web_icon){
                        var icon_data = current_record.web_icon.split(',')
                        var icon_span = "<span class='"+icon_data[0]+"'style='background-color:"+icon_data[2]+"; color: "+icon_data[1]+" '/>"
                        $tagtarget.find('.app-image').append($(icon_span))
                    } else {
                        var icon_image = "<img class='img img-fluid' src='/brain_pack_backend_ent/static/description/bizople-icon.png' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    }
                }

            })
            $('body').removeClass('d-none')
        });
    },
    onPatched() {
        this._super();
        var apps = this.props.apps
        $.each(apps, function( key, value ) {
                var target_tag = '.container a.o_app[id=result_app_'+key+']'
                var $tagtarget = $(target_tag)
                $tagtarget.find('.app-image').empty()
                if (value.use_icon) {
                    if (value.icon_class_name) {
                        var icon_span = "<span class='ri "+value.icon_class_name+"'/>"
                        $tagtarget.find('.app-image').append($(icon_span))
                    } else if (value.icon_img) {
                        var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value.id+"/icon_img' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    } else if (value.webIconData) {
                        var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value.id+"/web_icon_data' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    } else {
                        var icon_span = "<span class='"+value.webIcon.iconClass+"'style='background-color:"+value.webIcon.backgroundColor+"; color: "+value.webIcon.color+" '/>"
                        $tagtarget.find('.app-image').append($(icon_span))
                    }
                } else {
                    if (value.icon_img) {
                        var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value.id+"/icon_img' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    } else if (value.webIconData) {
                        var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value.id+"/web_icon_data' />"
                        $tagtarget.find('.app-image').append($(icon_image))
                    } else {
                        var icon_span = "<span class='"+value.webIcon.iconClass+"'style='background-color:"+value.webIcon.backgroundColor+"; color: "+value.webIcon.color+" '/>"
                        $tagtarget.find('.app-image').append($(icon_span))
                    }
                }
                $tagtarget.removeClass('d-none')
        });
    },
    willUnmount() {
        $('body').css("background-image", "")
    },
});