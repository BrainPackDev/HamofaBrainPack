 /** @odoo-module **/
import { ThreadView } from '@mail/components/thread_view/thread_view';
import { patch } from 'web.utils';
const { Component, useRef, onMounted } = owl;

patch(ThreadView.prototype, 'brainpack_discuss_search_view_cr.thread_view_component', {
    setup() {
        onMounted(() => {
             this.threadView.update({
                searchMessageId: false,
                searchMessage: false,
                messageFilter:  false,
                searchUpDown: false,
                upDisable: true,
                downDisable: true,
                searchString: '',
                currentSearchCount: 0,
                numberOfSearch: 0,
            })
        });
    },
     async _onKeyUpSearch(ev) {
         const query = ev.target.value.trim().toLowerCase();
         var domain = ['|',['subject','ilike',query],['body','ilike',query]]

         var messageFilter = true
        if(query == ''){
            messageFilter = false
         }

         this.threadView.update({
          stringifiedDomain: JSON.stringify(domain),
          searchMessageId: false,
          searchMessage: false,
          searchUpDown: false,
          searchString: ev.target.value,
          upDisable:true,
          downDisable:true,
          messageFilter:messageFilter,
          currentSearchCount:0,
          numberOfSearch:0,
        });
        this.threadView._onChangeStringifiedDomain()
    },
    _onClickCancle(ev){
        $(ev.currentTarget).closest('.o_cp_searchview').find('.o_searchview_input').val("")
        var domain = ['|',['subject','ilike',''],['body','ilike','']]
        this.threadView.update({
          searchMessage: false,
          upDisable:true,
          downDisable:true,
          searchString:"",
          currentSearchCount : 0,
          messageFilter: false,
          numberOfSearch : 0,
        });
        this.threadView.update({
          stringifiedDomain: JSON.stringify(domain),
        });
        $('.o_ThreadView').unblock()
    },
    _onClickSearch(ev){
        const query = $(ev.currentTarget).closest('.o_cp_searchview').find('.o_searchview_input').val().trim().toLowerCase()
        var domain = ['|',['subject','ilike',query],['body','ilike',query]]

        if(query != ''){
            this.threadView.update({
              searchMessage: true,
              searchString: $(ev.currentTarget).closest('.o_cp_searchview').find('.o_searchview_input').val(),
              upDisable:false,
              messageFilter: false,
              downDisable:false,
            });
        }
        else{
            this.threadView.update({
              searchMessage: false,
              upDisable:true,
              downDisable:true,
              searchString: $(ev.currentTarget).closest('.o_cp_searchview').find('.o_searchview_input').val(),
            });
        }
        this.threadView.update({
          stringifiedDomain: JSON.stringify(domain),
        });
        this.threadView._onChangeStringifiedDomain()
    },
//    _onKeyUpSearch(ev) {
//        const query = ev.target.value.trim().toLowerCase()
//        var domain = ['|',['subject','ilike',query],['body','ilike',query]]
//
//        if(query != ''){
//            this.threadView.update({
//              searchMessage: true,
//              searchString: ev.target.value,
//              upDisable:false,
//              downDisable:false,
//            });
//        }
//        else{
//            this.threadView.update({
//              searchMessage: false,
//              upDisable:true,
//              downDisable:true,
//              searchString: ev.target.value,
//            });
//        }
//        this.threadView.update({
//          stringifiedDomain: JSON.stringify(domain),
//        });
//        this.threadView._onChangeStringifiedDomain()
//    },
    _onClickUp(){
        var self = this
        var nextMessage = 0
        if(this.threadView.numberOfSearch){
            nextMessage = this.threadView.currentSearchCount + 1
        }

        if(nextMessage >= this.threadView.numberOfSearch){
            this.threadView.update({
              upDisable: true,
              downDisable:false
            });
        }
        else if(nextMessage < this.threadView.numberOfSearch){
            this.threadView.update({
              downDisable: false,
            });
        }
        if(nextMessage > this.threadView.numberOfSearch){
            return false
        }

        this.threadView.update({
          currentSearchCount: nextMessage,
        });

        this.messaging.discuss.update({
          currentSearchCount: nextMessage,
        });

        if(nextMessage > 0){
            this.threadView.update({
              searchMessageId : this.threadView.threadViewer.threadCache.SearchMessages[nextMessage-1].id,
            });
        }
        else{
            this.threadView.update({
              searchMessageId : false,
            });
        }

        if(this.threadView.searchMessageId){
            setTimeout(function(){
                if($('.o_Message[data-id='+self.threadView.searchMessageId+']').length > 0){
                    $('.o_ThreadView_messageList').animate({
                        scrollTop: $('.o_Message[data-id='+self.threadView.searchMessageId+']')[0].offsetTop - 100 ,
                    }, 400);
                }
                else{
                    self.threadView.update({searchUpDown:true})
//                    $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:height: 150px;"/></h1>' })
                    $('.o_ThreadView').block({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                     self.threadView.threadViewer.threadCache.update({ isAllHistoryLoaded: false });
                    self.threadView.threadViewer.threadCache.loadMoreMessages();
                }
            }, 1000);
        }
    },
    _onClickDown(){
        var self = this
        var nextMessage = 0
        if(this.threadView.numberOfSearch){
            nextMessage = this.threadView.currentSearchCount - 1
            if(nextMessage == 0){
                return false
            }
            if(nextMessage == 1){
                this.threadView.update({
                  upDisable: false,
                  downDisable:true
                });
            }
            else if(nextMessage > 1){
                this.threadView.update({
                  upDisable: false,
                });
            }
        }
        this.threadView.update({
          currentSearchCount: nextMessage,
        });

        if(nextMessage > 0){
            this.threadView.update({
              searchMessageId : this.threadView.threadViewer.threadCache.SearchMessages[nextMessage-1].id,
            });
        }
        else{
            this.threadView.update({
              searchMessageId : false,
            });
        }
        if(this.threadView.searchMessageId){
            setTimeout(function(){
                if($('.o_Message[data-id='+self.threadView.searchMessageId+']').length > 0){
                    $('.o_ThreadView_messageList').animate({
                        scrollTop: $('.o_Message[data-id='+self.threadView.searchMessageId+']')[0].offsetTop - 100 ,
                    }, 200);
                }
                else{
                    self.threadView.update({searchUpDown:true})
//                    $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    $('.o_ThreadView').block({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    self.threadView.threadViewer.threadCache.update({ isAllHistoryLoaded: false });
                    self.threadView.threadViewer.threadCache.loadMoreMessages();
                }
            }, 700);
        }
    }
});