/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';
import { clear, FieldCommand, link, unlink, unlinkAll } from '@mail/model/model_field_command';

registerPatch({
    name: 'ThreadView',
    fields: {
        stringifiedDomain: attr({ related: "threadViewer.stringifiedDomain" }),
        searchMessageId: attr({related: "threadViewer.searchMessageId"}),
        searchMessage: attr({related: "threadViewer.searchMessage"}),
        messageFilter: attr({related: "threadViewer.messageFilter"}),
        searchUpDown: attr({related: "threadViewer.searchUpDown"}),
        upDisable: attr({related: "threadViewer.upDisable"}),
        downDisable: attr({related: "threadViewer.downDisable"}),
        searchString: attr({related: "threadViewer.searchString"}),
        currentSearchCount: attr({related: "threadViewer.currentSearchCount"}),
        numberOfSearch: attr({related: "threadViewer.numberOfSearch"}),
    },
    recordMethods: {
          _onChangeStringifiedDomain() {
              // clear obsolete hints
              this.update({ componentHintList: clear() });
              this.addComponentHint("change-of-thread-cache");
              if (this.threadCache) {
                this.threadCache.update({
                  isLoaded: false,
                  isCacheRefreshRequested: true,
                });
              }
              this.update({ lastVisibleMessage: unlink() });
            },

            receivedMessage() {
              if (this.stringifiedDomain != "[]") {
                this.threadCache.update({ isCacheRefreshRequested: true });
              }else{
                if(this.stringifiedDomain){
                    this.threadCache.update({ isCacheRefreshRequested: true });
                }
              }
            },
    },
});