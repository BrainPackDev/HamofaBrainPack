/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';

registerPatch({
    name: 'ThreadViewer',
    fields: {
         discussStringifiedDomain: attr({ related: "discuss.stringifiedDomain" }),
         searchMessageId: attr({related: "discuss.searchMessageId"}),
        searchMessage: attr({related: "discuss.searchMessage"}),
        messageFilter: attr({related: "discuss.messageFilter"}),
        searchUpDown: attr({related: "discuss.searchUpDown"}),
        upDisable: attr({related: "discuss.upDisable"}),
        downDisable: attr({related: "discuss.downDisable"}),
        searchString: attr({related: "discuss.searchString"}),
        currentSearchCount: attr({related: "discuss.currentSearchCount"}),
        numberOfSearch: attr({related: "discuss.numberOfSearch"}),
        stringifiedDomain: attr({
            compute() {
                if (this.chatter) {
                return "";
              }
              if (this.chatWindow) {
                return "";
              }
              if (this.discuss) {
                return this.discuss.stringifiedDomain;
              }
              return this.stringifiedDomain;
            },
        }),
    },
     onChanges: [
        {
            dependencies: ['stringifiedDomain','messageFilter'],
            methodName: '_onChangeStringifiedDomain',
        },
    ],
    recordMethods: {
        _onComputeStringifiedDomain() {
          if (this.chatter) {
            return "";
          }
          if (this.chatWindow) {
            return "";
          }
          if (this.discuss) {
            return this.discuss.stringifiedDomain;
          }
          return this.stringifiedDomain;
        },
        _onChangeStringifiedDomain() {
          // clear obsolete hints
          if (this.threadView) {
            this._updateFetchMessagesParams();
            this.threadView._onChangeStringifiedDomain();
          }
        },
        _updateFetchMessagesParams() {
          var param = { ...this.thread.fetchMessagesParams };

          if (this.stringifiedDomain) {
            const stringifiedDomain = JSON.parse(this.stringifiedDomain);
            var param = { ...this.thread.fetchMessagesParams };
            param.stringifiedDomain = stringifiedDomain;
          } else {
            if (param.hasOwnProperty("stringifiedDomain")) {
              delete param.stringifiedDomain;
            }
          }
          this.thread.update({
            fetchMessagesParams: param,
          });
        },
//        saveThreadCacheScrollPositionsAsInitial(scrollTop, threadCache) {
//            debugger;
//            threadCache = threadCache || this.threadCache;
//            if (!threadCache) {
//                return;
//            }
//            if (this.chatter) {
//                // Initial scroll position is disabled for chatter because it is
//                // too complex to handle correctly and less important
//                // functionally.
//                return;
//            }
//            this.update({
//                threadCacheInitialScrollPositions: Object.assign({}, this.threadCacheInitialScrollPositions, {
//                    [threadCache.localId]: scrollTop,
//                }),
//            });
//
//            if(this.threadCache && this.threadCache.fetchedMessages && this.threadCache.fetchedMessages.length && this.discuss.stringifiedDomain){
//                this.discuss.update({
//                    numberOfSearch : this.threadCache.fetchedMessages.length
//                })
//            }
//            else{
//                this.discuss.update({
//                    numberOfSearch : 0
//                })
//            }
//        },
    },
});