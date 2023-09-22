/** @odoo-module **/

import { useRefToModel } from '@mail/component_hooks/use_ref_to_model';
import { useUpdateToModel } from '@mail/component_hooks/use_update_to_model';
import { registerMessagingComponent } from '@mail/utils/messaging_component';

const { Component } = owl;
import { registerPatch } from '@mail/model/model_core';
import { registerModel } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';
import { clear } from '@mail/model/model_field_command';


export class ThreadViewNav extends Component {

        setup() {
            super.setup();
        }
        mounted() {
            super.mounted()
           if(this.threadViewNav &&  this.threadViewNav.channel && this.threadViewNav.channel.correspondent && this.threadViewNav.channel.correspondent.persona.partner && this.threadViewNav.channel.correspondent.persona.partner.user){
                if(this.threadViewNav.isWaMsgs){
                    this.onClickWhatsapp()
                }
                else{
                    this.onClickLive()
                }
            }
            else{
                this.onClickWhatsapp();
            }
        }
        render(){
            super.render()
            if(this.threadViewNav &&  this.threadViewNav.channel && this.threadViewNav.channel.correspondent && this.threadViewNav.channel.correspondent.persona.partner && this.threadViewNav.channel.correspondent.persona.partner.user){
                if(this.threadViewNav.isWaMsgs){
                    this.onClickWhatsapp()
                }
                else{
                    this.onClickLive()
                }
            }
            else{
                this.onClickWhatsapp();
            }
            if(this.messaging && this.messaging.wa_thread_view && this.messaging.wa_thread_view.state.nav_active == 'partner'){
                this.messaging.wa_thread_view.tabPartner();
            }
            function test(){
                var tabsNewAnim = $('#navbarSupportedContent');
                var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
                var activeItemNewAnim = tabsNewAnim.find('.active');
                var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
                var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth() ;
                var itemPosNewAnimTop = activeItemNewAnim.position();
                var itemPosNewAnimLeft = activeItemNewAnim.position();
                if(itemPosNewAnimTop){
                      $(".hori-selector").css({
                        "top":itemPosNewAnimTop.top + "px",
                        "left":itemPosNewAnimLeft.left + "px",
                        "height": activeWidthNewAnimHeight + "px",
                        "width": activeWidthNewAnimWidth + "px"
                      });
                }

                  $("#navbarSupportedContent").on("click","li",function(e){
                    $('#navbarSupportedContent ul li').removeClass("active");
                    $(this).addClass('active');
                    var activeWidthNewAnimHeight = $(this).innerHeight();
                    var activeWidthNewAnimWidth = $(this).innerWidth();
                    var itemPosNewAnimTop = $(this).position();
                    var itemPosNewAnimLeft = $(this).position();
                    $(".hori-selector").css({
                      "top":itemPosNewAnimTop.top + "px",
                      "left":itemPosNewAnimLeft.left + "px",
                      "height": activeWidthNewAnimHeight + "px",
                      "width": activeWidthNewAnimWidth + "px"
                    });
                  });
            }
            $(document).ready(function(){
              setTimeout(function(){ test(); });
            });

            $(window).on('resize', function(){
              setTimeout(function(){ test(); }, 500);
            });
            $(".navbar-toggler").click(function(){
              setTimeout(function(){ test(); });
            });
        }

        onClickLive(){
            if(this.threadViewNav){
                this.threadViewNav.update({isWaMsgs:false})
//                this.threadViewNav.refresh();
                $('#navbarSupportedContent').click();

                setTimeout(function(){
                    if($('.o_ThreadView_messageList .o_MessageList_message') && $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1] &&$('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop){
                        $('.o_ThreadView_messageList').animate({
                            scrollTop: $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop + 100,
                        }, 500);
                    }
                    setTimeout(function(){
                        if($('.o_ThreadView_messageList .o_MessageList_message') && $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1] &&$('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop){
                            $('.o_ThreadView_messageList').animate({
                                scrollTop: $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop + 100,
                            }, 300);
                        }
                    }, 100);
                }, 400);

            }
        }
        onClickWhatsapp() {
            if(this.threadViewNav){
                this.threadViewNav.update({isWaMsgs:true})
                $('#navbarSupportedContent').click();

                setTimeout(function(){
                    if($('.o_ThreadView_messageList .o_MessageList_message') && $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1] &&$('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop){
                        $('.o_ThreadView_messageList').animate({
                            scrollTop: $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop +100 ,
                        }, 500);
                    }
                    setTimeout(function(){
                        if($('.o_ThreadView_messageList .o_MessageList_message') && $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1] &&$('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop){
                            $('.o_ThreadView_messageList').animate({
                                scrollTop: $('.o_ThreadView_messageList .o_MessageList_message')[$('.o_ThreadView_messageList .o_MessageList_message').length - 1].offsetTop + 100,
                            }, 300);
                        }
                    }, 100);
                }, 400);
            }
        }
        get threadViewNav() {
            var threads = this.messaging.models['Thread'].all().filter(thread => thread.localId==this.props.localId);
            return threads && threads[0];
        }
}

Object.assign(ThreadViewNav, {
    //props: { localId: String},
    props: { localId: String },
    template: 'brainpack_meta_whatsapp.ThreadViewNav',
});

registerMessagingComponent(ThreadViewNav);


registerPatch({
    name: 'ThreadView',
    recordMethods: {
        threadViewNav() {
            return this.messaging;
        },
    },
    fields: {
        hasThreadNav: attr({
            compute() {
                return Boolean(this && this.topbar && this.thread.localId);
            },
        }),
    },
});

