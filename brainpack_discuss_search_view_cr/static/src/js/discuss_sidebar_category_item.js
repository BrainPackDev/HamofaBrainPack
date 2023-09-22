/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';
import { clear, FieldCommand, link, unlink, unlinkAll } from '@mail/model/model_field_command';

registerPatch({
    name: 'DiscussSidebarCategoryItem',
        recordMethods: {
            onClick(ev) {
                if (this.thread.channel.channel_type == 'chat') {
                    this.thread.open();
                    if(this.channel && this.channel.correspondent && this.channel.correspondent.persona && this.channel.correspondent.persona.partner && this.channel.correspondent.persona.partner.user){
                        this.thread.update({isWaMsgs:false});
                    }
                    else{
                        this.thread.update({isWaMsgs:true}); // WhatsApp Tab will Open By Default when we click on DiscussSidebarCategoryItem
                    }
                    if(this.thread.messaging && this.thread.messaging.wa_thread_view && this.thread.messaging.wa_thread_view.state.nav_active == 'partner'){
                        this.thread.messaging.wa_thread_view.tabPartner(); // TabPartner will open when we click on DiscussSidebarCategoryItem
                    }
                }
                else {
                    this.thread.open();
                }
                if(this.thread.threadViews){
                    for (const threadView of this.thread.threadViews) {
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
            },
        },
});