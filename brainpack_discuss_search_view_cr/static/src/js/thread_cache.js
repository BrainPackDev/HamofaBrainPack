/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';
import { clear, FieldCommand, link, unlink, unlinkAll } from '@mail/model/model_field_command';

registerPatch({
    name: 'ThreadCache',
    fields: {
        messages: {
            compute() {
                const fetchMessagesParams = this.thread.fetchMessagesParams;
                  if (fetchMessagesParams.hasOwnProperty("stringifiedDomain") && fetchMessagesParams.stringifiedDomain != []) {
                    return [...this.fetchedMessages]
                  }
                if (!this.thread) {
                    return clear();
                }
                let newerMessages;
                if (!this.lastFetchedMessage) {
                    newerMessages = this.thread.messages;
                } else {
                    if(this.thread.messages){
                        newerMessages = this.thread.messages.filter(message =>
                            message.id > this.lastFetchedMessage.id
                        );
                    }
                }
                return [...this.fetchedMessages, ...this.temporaryMessages, ...newerMessages];
            },
        },
         SearchMessages: many('Message', {
            compute() {
                return this.fetchedMessages.sort((m1, m2) => m1.id < m2.id ? -1 : 1);
            },
        }),
        orderedFetchedMessages:{
            compute() {
                return this.fetchedMessages.sort((m1, m2) => m1.id < m2.id ? -1 : 1);
            },
        },
    },
    recordMethods: {
       async _loadMessages({ limit = 30, maxId, minId } = {}) {
//          const messages = await this._super(...arguments);
          this.update({ isLoading: true });
            let messages_list,messages,search_messages;
            try {
                messages_list = await this.messaging.models['Message'].performRpcMessageFetch(this.thread.fetchMessagesUrl, {
                    ...this.thread.fetchMessagesParams,
                    limit,
                    'max_id': maxId,
                    'min_id': minId,
                });
                messages = messages_list[0]
                search_messages = messages_list[1]

            } catch (e) {
                if (this.exists()) {
                    this.update({
                        hasLoadingFailed: true,
                        isLoading: false,
                    });
                }
                throw e;
            }
            if (!this.exists()) {
                return;
            }
            this.update({
                rawFetchedMessages: link(messages),
                hasLoadingFailed: false,
                isLoaded: true,
                isLoading: false,
            });
            if (!minId && messages.length < limit) {
                this.update({ isAllHistoryLoaded: true });
            }
            this.messaging.messagingBus.trigger('o-thread-cache-loaded-messages', {
                fetchedMessages: messages,
                threadCache: this,
            });

          const fetchMessagesParams = this.thread.fetchMessagesParams;
          let vals = {};
          if (fetchMessagesParams.hasOwnProperty("stringifiedDomain") && fetchMessagesParams.stringifiedDomain.length > 0) {
            vals = {
              hasLoadingFailed: false,
              isLoaded: true,
              isLoading: false,
            };

            if(this.thread && this.thread.isWaMsgs && !this.thread.isChatterWa){
                if(search_messages){
                    search_messages = search_messages.filter(message => !message.isEmpty && message.message_type=='wa_msgs');
                }
            }
            else{
                if(search_messages){
                    search_messages = search_messages.filter(message => !message.isEmpty && message.message_type!='wa_msgs');
                }
            }

            // maxId is only valid when called from load more

             for (const threadView of this.threadViews) {
                if(threadView.messageFilter){
                    if (maxId) {
                      vals.fetchedMessages = link(messages);
                    } else {
                      vals.fetchedMessages = messages;
                    }
                }
                else{
                    if (maxId) {
                        vals.fetchedMessages = link(messages);
                    } else {
                      vals.fetchedMessages = messages;
                    }
                }
             }
            if (maxId) {
              vals.SearchMessages = link(search_messages);
            } else {
              vals.SearchMessages = search_messages;
            }

          }
          if (!maxId && messages.length >= limit) {
            vals.isAllHistoryLoaded = false;
          }
          this.update(vals);
        return [messages,search_messages];
    },

     async loadMoreMessages() {
            var self = this
            if (this.isAllHistoryLoaded || this.isLoading) {
                return;
            }
            if (!this.isLoaded) {
                this.update({ isCacheRefreshRequested: true });
                return;
            }
            this.update({ isLoadingMore: true });
            const messageIds = this.fetchedMessages.map(message => message.id);
            var limit = 30;
            var minId = false
            for (const threadView of this.threadViews) {
                if(threadView.searchMessage && threadView.searchUpDown){
                    var msg_available = self.fetchedMessages.filter(a => a.id == threadView.searchMessageId)
                    if(msg_available.length == 0){
                        limit = 500
                        if((Math.min(...messageIds)-threadView.searchMessageId - 1) > 400){
                            minId = threadView.searchMessageId - 1
                        }
                    }
                }
            }
            let fetchedMessages;
            let fetchedMessagess;
            let fetchedSearchMessages;
            let success;

            try {
                if(minId){
                fetchedMessagess = await this._loadMessages({ limit, maxId: Math.min(...messageIds), minId:minId });
                }
                else{
                fetchedMessagess = await this._loadMessages({ limit, maxId: Math.min(...messageIds) });
                }

                fetchedMessages = fetchedMessagess[0]
                fetchedSearchMessages = fetchedMessagess[1]

                success = true;
            } catch (_e) {
                success = false;
            }

            if (!this.exists()) {
                return;
            }
            if (success) {
                if (fetchedMessages.length < limit) {
                    this.update({ isAllHistoryLoaded: true });
                }
                for (const threadView of this.threadViews) {
                    threadView.addComponentHint('more-messages-loaded', { fetchedMessages });
                }
            }
            this.update({ isLoadingMore: false });

            if(this.thread && this.thread.isWaMsgs && !this.thread.isChatterWa){
                if(fetchedSearchMessages){
                    fetchedSearchMessages = fetchedSearchMessages.filter(message => !message.isEmpty && message.message_type=='wa_msgs');
                }
            }
            else{
                if(fetchedSearchMessages){
                    fetchedSearchMessages = fetchedSearchMessages.filter(message => !message.isEmpty && message.message_type!='wa_msgs');
                }
            }

            this.update({ SearchMessages: fetchedSearchMessages });

            for (const threadView of this.threadViews) {
                if(threadView.searchMessage && threadView.searchUpDown){
                    var massage_available = this.fetchedMessages.filter(a => a.id == threadView.searchMessageId)
                    if(massage_available.length > 0){
                        setTimeout(function(){
                            if($('.o_Message[data-id='+threadView.searchMessageId+']').length > 0){
                                $('.o_ThreadView_messageList').animate({
                                    scrollTop: $('.o_Message[data-id='+threadView.searchMessageId+']')[0].offsetTop - 100 ,
                                }, 200);
                            }
                            threadView.update({'searchUpDown':false})
//                            $.unblockUI()
                            $('.o_ThreadView').unblock()
                        }, 200);
                    }
                    else{
                        setTimeout(function(){
                            if(self.fetchedMessages.length > 0 && $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']').length > 0){
                                $('.o_ThreadView_messageList').animate({
                                        scrollTop: $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']')[0].offsetTop + 1000,
                                }, 50);
                            }
                        }, 100);


                        setTimeout(async function(){
                            if($("body").find('.chatter_loader').length == 0){
//                                $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                                $('.o_ThreadView').block({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                            }
                            self.update({ isAllHistoryLoaded: false });
                            await self.loadMoreMessages();
                        }, 50);
                    }
                }

//                if(threadView.threadViewer && threadView.threadViewer.discuss && threadView.threadViewer.discuss.searchMessage && threadView.threadViewer.discuss.searchUpDown){
//                    var massage_available = this.fetchedMessages.filter(a => a.id == threadView.threadViewer.discuss.searchMessageId)
//                    if(massage_available.length > 0){
//                        setTimeout(function(){
//                            if($('.o_Message[data-id='+threadView.threadViewer.discuss.searchMessageId+']').length > 0){
//                                $('.o_ThreadView_messageList').animate({
//                                    scrollTop: $('.o_Message[data-id='+threadView.threadViewer.discuss.searchMessageId+']')[0].offsetTop - 100 ,
//                                }, 200);
//                            }
//                            threadView.threadViewer.discuss.update({'searchUpDown':false})
//                        }, 700);
//                    }
//                    else{
//                        setTimeout(function(){
//                            if(self.fetchedMessages.length > 0 && $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']').length > 0){
//                                $('.o_ThreadView_messageList').animate({
//                                        scrollTop: $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']')[0].offsetTop - 100 ,
//                                }, 400);
//                            }
//                        }, 700);
//                        await this.loadMoreMessages();
//                    }
//                }
//                if(threadView.threadViewer.discuss.searchMessageId == )
            }
        },

        async loadNewMessages() {
            if (this.isLoading) {
                return;
            }
            if (!this.isLoaded) {
                this.update({ isCacheRefreshRequested: true });
                return;
            }
            const messageIds = this.fetchedMessages.map(message => message.id);

            var fetchedMessagess = this._loadMessages({ minId: Math.max(...messageIds, 0) });
            var fetchedMessages = fetchedMessagess[0]
            var fetchedSearchMessages = fetchedMessagess[1]

            if (!fetchedMessages || fetchedMessages.length === 0) {
                return;
            }
            for (const threadView of this.threadViews) {
                threadView.addComponentHint('new-messages-loaded', { fetchedMessages });
            }

            return fetchedMessages;
        },

    async _onHasToLoadMessagesChanged() {
        var self = this
        if (!this.hasToLoadMessages) {
            return;
        }
//        var fetchedMessages = await this._loadMessages();
        var fetchedMessagess = await this._loadMessages();
        var fetchedMessages = fetchedMessagess[0]
        var fetchedSearchMessages = fetchedMessagess[1]
        if (!this.exists()) {
            return;
        }

        if(this.thread.isWaMsgs && !this.thread.isChatterWa){
            if(fetchedSearchMessages){
                fetchedSearchMessages = fetchedSearchMessages.filter(message => !message.isEmpty && message.message_type=='wa_msgs');
            }
        }
        else{
            if(fetchedSearchMessages){
                fetchedSearchMessages = fetchedSearchMessages.filter(message => !message.isEmpty && message.message_type!='wa_msgs');
            }
        }
        this.update({ SearchMessages: fetchedSearchMessages });


        for (const threadView of this.threadViews) {
            threadView.addComponentHint('messages-loaded', { fetchedMessages });
            if(threadView){
                if(threadView.searchMessage){
                    threadView.update({
                        numberOfSearch : fetchedSearchMessages.length
                    })

                    if(fetchedSearchMessages.length > 0){
                        if(threadView.searchMessageId && threadView.currentSearchCount == 1){
                            threadView.update({
                                currentSearchCount : 1,
                                searchMessageId : fetchedSearchMessages[0].id,
                                downDisable:true,
                            })
                        }
                        else if(threadView.searchMessageId && threadView.currentSearchCount == 0){
                            var index = fetchedSearchMessages.findIndex(t => t.id === threadView.searchMessageId);
                            let currentSearchCon = 0
                            if(index > -1){
                                currentSearchCon = index + 1
                            }

                            threadView.update({
                                currentSearchCount : currentSearchCon,
                                searchMessageId : threadView.searchMessageId,
                            })

                            if(fetchedSearchMessages.length > currentSearchCon){
                                threadView.update({
                                    downDisable:false,
                                })
                            }
                            else{
                                threadView.update({
                                    downDisable:true,
                                })
                            }
                        }
                        else{
                            threadView.update({
                                currentSearchCount : 1,
                                searchMessageId : fetchedSearchMessages[0].id,
                                downDisable:true,
                            })
                        }
                    }
                    else{
                        threadView.update({
                            currentSearchCount : 0,
                            searchMessageId : false,
                            downDisable:false,
                        })
                    }
                }
                else{
                    threadView.update({
                        currentSearchCount : 0
                    })
                    threadView.update({
                        numberOfSearch : 0
                    })
                }
                if(threadView.messageFilter){
                    threadView.update({
                        numberOfSearch : fetchedMessages.length
                    })
                }
            }
        }



//        for (const threadView of this.threadViews) {
//            threadView.addComponentHint('messages-loaded', { fetchedMessages });
//            if(threadView && threadView.threadViewer && threadView.threadViewer.discuss){
//                if(threadView.threadViewer && threadView.threadViewer.discuss && threadView.threadViewer.discuss.searchMessage){
//                    threadView.threadViewer.discuss.update({
//                        numberOfSearch : fetchedSearchMessages.length
//                    })
//
//                    if(fetchedSearchMessages.length > 0){
//                        if(threadView.threadViewer.discuss.searchMessageId && threadView.threadViewer.discuss.currentSearchCount == 1){
//                            threadView.threadViewer.discuss.update({
//                                currentSearchCount : 1,
//                                searchMessageId : fetchedSearchMessages[0].id,
//                                downDisable:true,
//                            })
//                        }
//                        else{
//                            threadView.threadViewer.discuss.update({
//                                currentSearchCount : 1,
//                                searchMessageId : fetchedSearchMessages[0].id,
//                                downDisable:true,
//                            })
//                        }
//                    }
//                    else{
//                        threadView.threadViewer.discuss.update({
//                            currentSearchCount : 0,
//                            searchMessageId : false,
//                            downDisable:false,
//                        })
//                    }
//                }
//                else{
//                    threadView.threadViewer.discuss.update({
//                        currentSearchCount : 0
//                    })
//                    threadView.threadViewer.discuss.update({
//                        numberOfSearch : 0
//                    })
//                }
//            }
//        }
        this.messaging.messagingBus.trigger('o-thread-loaded-messages', { thread: this.thread });

        for (const threadView of this.threadViews) {
            if(threadView.searchMessageId){
                var massage_available = this.fetchedMessages.filter(a => a.id == threadView.searchMessageId)
                if(massage_available.length > 0){
                    setTimeout(function(){
                        if($('.o_Message[data-id='+threadView.searchMessageId+']').length > 0){
                            $('.o_ThreadView_messageList').animate({
                                scrollTop: $('.o_Message[data-id='+threadView.searchMessageId+']')[0].offsetTop - 100 ,
                            }, 200);
                        }
                    }, 300);
                }
                else{
//                    setTimeout(function(){
//                        if(self.fetchedMessages.length > 0 && $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']').length > 0){
//                            $('.o_ThreadView_messageList').animate({
//                                    scrollTop: $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']')[0].offsetTop - 100 ,
//                            }, 400);
//                        }
//                    }, 300);
//                    console.log(">>>>>>>",this)
                    if(threadView.searchMessage){
//                        $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                           $('.o_ThreadView').block({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    }
                    threadView.update({searchUpDown:true})
                    await this.loadMoreMessages();
                }
            }
        }

//        for (const threadView of this.threadViews) {
//            if(threadView.threadViewer && threadView.threadViewer.discuss && threadView.threadViewer.discuss.searchMessageId){
//                var massage_available = this.fetchedMessages.filter(a => a.id == threadView.threadViewer.discuss.searchMessageId)
//                if(massage_available.length > 0){
//                    setTimeout(function(){
//                        if($('.o_Message[data-id='+threadView.threadViewer.discuss.searchMessageId+']').length > 0){
//                            $('.o_ThreadView_messageList').animate({
//                                scrollTop: $('.o_Message[data-id='+threadView.threadViewer.discuss.searchMessageId+']')[0].offsetTop - 100 ,
//                            }, 200);
//                        }
//                    }, 700);
//                }
//                else{
//                    setTimeout(function(){
//                        if(self.fetchedMessages.length > 0 && $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']').length > 0){
//                            $('.o_ThreadView_messageList').animate({
//                                    scrollTop: $('.o_Message[data-id='+self.fetchedMessages[self.fetchedMessages.length-1].id+']')[0].offsetTop - 100 ,
//                            }, 400);
//                        }
//                    }, 700);
//                    threadView.threadViewer.discuss.update({searchUpDown:true})
//                    await this.loadMoreMessages();
//                }
//            }
//        }
    },

    _computeHasToLoadMessages() {
      var res = this._super();
      if (res.hasToLoadMessages) {
        return res;
      }
      const fetchMessagesParams = this.thread.fetchMessagesParams;
      if (
        fetchMessagesParams.hasOwnProperty("stringifiedDomain") &&
        fetchMessagesParams.stringifiedDomain.length > 0 &&
        this.isCacheRefreshRequested
      ) {
        res.hasToLoadMessages = true;
      }
      return res;
    },
    },
});