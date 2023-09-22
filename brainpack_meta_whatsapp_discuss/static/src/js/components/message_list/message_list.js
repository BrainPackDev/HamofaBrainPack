/** @odoo-module **/

import { MessageList } from '@mail/components/message_list/message_list';
import { patch } from 'web.utils';

//patch(MessageList.prototype, 'brainpack_meta_whatsapp/static/src/js/components/message_list/message_list.js', {
//    get image_url(){
//        if(this.threadView && this.threadView.thread && this.threadView.thread.isWaMsgs &&  this.threadView.thread.model == 'mail.channel' && this.threadView.thread.env && this.threadView.thread.env.session.company_id){
//            return '/web/image/res.company/'+this.threadView.thread.env.session.company_id+'/back_image'
//        }
//        else{
//            return ""
//        }
//    }
//});