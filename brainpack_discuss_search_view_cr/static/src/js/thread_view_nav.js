 /** @odoo-module **/
import { ThreadViewNav } from '@brainpack_meta_whatsapp_discuss/js/components/thread_view_nav/thread_view_nav';
import { patch } from 'web.utils';

patch(ThreadViewNav.prototype, 'brainpack_discuss_search_view_cr.thread_view_nav', {
     onClickLive(){
            if(this.threadViewNav){
                this.threadViewNav.update({isWaMsgs:false})
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

                if(this.threadViewNav.threadViews){
                    for (const threadView of this.threadViewNav.threadViews) {
                        threadView.threadViewer.discuss.update(
                            {
                                searchMessageId:false,
                                searchMessage: false,
                                searchUpDown: false,
                                upDisable:true,
                                messageFilter: false,
                                downDisable:true,
                                stringifiedDomain: "",
                                currentSearchCount: 0,
                                numberOfSearch: 0,
                            }
                        )
                    }
                    $('.o_searchview_input_container .o_searchview_input').val('');
                }
            }
        },
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

                if(this.threadViewNav.threadViews){
                    for (const threadView of this.threadViewNav.threadViews) {
                        threadView.threadViewer.discuss.update(
                            {
                                searchMessageId:false,
                                searchMessage: false,
                                searchUpDown: false,
                                upDisable:true,
                                messageFilter: false,
                                downDisable:true,
                                stringifiedDomain: "",
                                currentSearchCount: 0,
                                numberOfSearch: 0,
                            }
                        )
                    }
                    $('.o_searchview_input_container .o_searchview_input').val('');
                }
            }
        }
});