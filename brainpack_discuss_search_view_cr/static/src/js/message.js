/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";
import { attr, many, one } from '@mail/model/model_field';
import { clear, insert, link } from '@mail/model/model_field_command';
import { addLink, htmlToTextContentInline, parseAndTransform } from '@mail/js/utils';

registerPatch({
    name: 'Message',
        fields: {
            prettyBody: {
                compute() {
                    if (!this.body) {
                        // body null in db, body will be false instead of empty string
                        return clear();
                    }
                    var newText = this.body

                    for (const thread of this.threads) {
                        for (const threadView of thread.threadViews) {
                            if(threadView.threadViewer && threadView.threadViewer.threadCache && threadView.threadViewer.threadCache.SearchMessages){
                                if(threadView.messageFilter){
                                    var searchText = threadView.searchString;
                                    newText = $(this.body).mark(threadView.searchString,{"accuracy": "partially",
                                                "iframes": true,
                                                "ignoreJoiners": true,
                                                "acrossElements": true,
                                                "separateWordSearch": true,
                                                "diacritics": false,
                                                })[0].outerHTML
                                    if(threadView.searchMessageId && threadView.searchMessageId == this.id){
                                        newText = newText.replaceAll('<mark data-markjs="true">','<mark data-markjs="true" class="highlight search_message active">')
                                    }
                                    else{
                                        newText = newText.replaceAll('<mark data-markjs="true">','<mark data-markjs="true" class="highlight search_message">')
                                    }
                                }
                                var message = threadView.threadViewer.threadCache.SearchMessages.filter(x => x.id == this.id)

                                if(message.length > 0){

                                    if(threadView.searchMessage){
                                        var searchText = threadView.searchString;
                                        newText = $(this.body).mark(threadView.searchString,{"accuracy": "partially",
                                                    "iframes": true,
                                                    "ignoreJoiners": true,
                                                    "acrossElements": true,
                                                    "separateWordSearch": true,
                                                    "diacritics": false,
                                                    })[0].outerHTML
                                        if(threadView.searchMessageId && threadView.searchMessageId == this.id){
                                            newText = newText.replaceAll('<mark data-markjs="true">','<mark data-markjs="true" class="highlight search_message active">')
                                        }
                                        else{
                                            newText = newText.replaceAll('<mark data-markjs="true">','<mark data-markjs="true" class="highlight search_message">')
                                        }
                                    }
                                }
                            }
                        }
                    }


//                    if(this.messaging && this.messaging.discuss && this.messaging.discuss.threadViewer && this.messaging.discuss.threadViewer.threadCache && this.messaging.discuss.threadViewer.threadCache.SearchMessages){
//                        var message = this.messaging.discuss.threadViewer.threadCache.SearchMessages.filter(x => x.id == this.id)
//
//                        if(message.length > 0){
//                            if(this.messaging.discuss.searchMessage){
//                                var searchText = this.messaging.discuss.searchString;
//                                newText = $(this.body).mark(this.messaging.discuss.searchString,{separateWordSearch:true,diacritics:true})[0].outerHTML
//                                if(this.messaging.discuss.searchMessageId && this.messaging.discuss.searchMessageId == this.id){
//                                    newText = newText.replaceAll('<mark data-markjs="true">','<mark data-markjs="true" class="highlight search_message active">')
//                                }
//                                else{
//                                    newText = newText.replaceAll('<mark data-markjs="true">','<mark data-markjs="true" class="highlight search_message">')
//                                }
//                            }
//                        }
//                    }
                    // add anchor tags to urls
                    return parseAndTransform(newText, addLink);
    //                return parseAndTransform(this.body.replace(this.messaging.discuss.searchString,'<span style="background-color:#eb9834;">'+this.messaging.discuss.searchString+'</span>'), addLink);
                },
            },
        },
        modelMethods: {
            async performRpcMessageFetch(route, params) {
                const messagesData1 = await this.messaging.rpc({ route, params }, { shadow: true });

                const messagesData = messagesData1[0]
                const searchMessageData = messagesData1[1]

                if (!this.messaging) {
                    return;
                }
                const messages = this.messaging.models['Message'].insert(messagesData.map(
                    messageData => this.messaging.models['Message'].convertData(messageData)
                ));

                const searchMessages = this.messaging.models['Message'].insert(searchMessageData.map(
                    searchMessageData => this.messaging.models['Message'].convertData(searchMessageData)
                ));
                // compute seen indicators (if applicable)
                for (const message of messages) {
                    for (const thread of message.threads) {
                        if (!thread.channel || thread.channel.channel_type === 'channel') {
                            // disabled on non-channel threads and
                            // on `channel` channels for performance reasons
                            continue;
                        }
                        this.messaging.models['MessageSeenIndicator'].insert({
                            thread,
                            message,
                        });
                    }
                }
                return [messages,searchMessages];
            },
         },
});