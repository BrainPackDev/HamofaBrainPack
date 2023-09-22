 /** @odoo-module **/

import { Discuss } from '@mail/components/discuss/discuss';
import { patch } from 'web.utils';

//patch(Discuss.prototype, 'brainpack_meta_whatsapp/static/src/js/components/discuss/discuss.js', {
//     willUnmount() {
//        if (this.discuss) {
//            window.location = window.location.origin + '/web'
//            this.discuss.close();
//        }
//    }
//});