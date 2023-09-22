odoo.define('brainpack_website_extended.portal', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var portal = require('portal.portal');

publicWidget.registry.PortalHomeCounters.include({
    async _updateCounters(elem) {
        const numberRpc = 3;
        const needed = Object.values(this.el.querySelectorAll('[data-placeholder_count]'))
                                .map(documentsCounterEl => documentsCounterEl.dataset['placeholder_count']);
        const counterByRpc = Math.ceil(needed.length / numberRpc);  // max counter, last can be less
        const countersAlwaysDisplayed = this._getCountersAlwaysDisplayed();

        const proms = [...Array(Math.min(numberRpc, needed.length)).keys()].map(async i => {
            const documentsCountersData = await this._rpc({
                route: "/my/counters",
                params: {
                    counters: needed.slice(i * counterByRpc, (i + 1) * counterByRpc)
                },
            });
            Object.keys(documentsCountersData).forEach(counterName => {
                const documentsCounterEl = this.el.querySelector(`[data-placeholder_count='${counterName}']`);
                documentsCounterEl.textContent = documentsCountersData[counterName];
                // The element is hidden by default, only show it if its counter is > 0 or if it's in the list of counters always shown
                if (documentsCountersData[counterName] !== 0) {
                    documentsCounterEl.parentElement.classList.remove('d-none');
                }
            });
            return documentsCountersData;
        });
        return Promise.all(proms).then((results) => {
            const counters = results.reduce((prev, current) => Object.assign({...prev, ...current}), {});
            this.el.querySelector('.o_portal_doc_spinner').remove();
            // Display a message when there are no documents available if there are no counters > 0 and no counters always shown
            if (!countersAlwaysDisplayed.length && !Object.values(counters).filter((val) => val > 0).length) {
                this.el.querySelector('.o_portal_no_doc_message').classList.remove('d-none');
            }
        });
    },
});

});