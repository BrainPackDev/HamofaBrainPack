 /** @odoo-module **/
import { Message } from '@mail/components/message/message';
import { patch } from 'web.utils';

patch(Message.prototype, 'brainpack_discuss_search_view_cr.message_component', {
    _getStyle(){
        for (const thread of this.props.record.message.threads) {
            for (const threadView of thread.threadViews) {
                if(threadView.messageFilter){
                    return "cursor: pointer;"
                }
                else{
                    return ""
                }
            }
        }
    },
    _onClickMessage(ev){
        for (const thread of this.props.record.message.threads) {
            for (const threadView of thread.threadViews) {
                if(threadView.messageFilter){
                    const query = threadView.searchString.trim().toLowerCase()
                    var domain = ['|',['subject','ilike',query],['body','ilike',query]]

                    if(query != ''){
                        threadView.update({
                          searchMessage: true,
                          searchString: threadView.searchString,
                          upDisable:false,
                          messageFilter: false,
                          downDisable:false,
                          searchMessageId:this.props.record.message.id,
                        });
                    }
                    else{
                        threadView.update({
                          searchMessage: false,
                          upDisable:true,
                          downDisable:true,
                          messageFilter: false,
                          searchString: threadView.searchString,
                          searchMessageId:this.props.record.message.id
                        });
                    }
                    threadView.update({
                      stringifiedDomain: JSON.stringify(domain),
                    });
                    threadView._onChangeStringifiedDomain()
                }
            }
        }
        return true
    },
});