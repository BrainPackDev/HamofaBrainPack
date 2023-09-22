odoo.define('brainpack_website_extended.s_website_form', function (require) {
    "use strict";

    var s_website_form = require('website.s_website_form');
    var core = require('web.core');
    var time = require('web.time');
    const {ReCaptcha} = require('google_recaptcha.ReCaptchaV3');
    const session = require('web.session');
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    const dom = require('web.dom');
    const concurrency = require('web.concurrency');

    var _t = core._t;
    var qweb = core.qweb;

    publicWidget.registry.s_website_form.include({
        send: async function (e) {
            debugger;
            e.preventDefault(); // Prevent the default submit behavior
             // Prevent users from crazy clicking
            const $button = this.$target.find('.s_website_form_send, .o_website_form_send');
            $button.addClass('disabled') // !compatibility
                   .attr('disabled', 'disabled');
            this.restoreBtnLoading = dom.addButtonLoadingEffect($button[0]);

            var self = this;

            self.$target.find('#s_website_form_result, #o_website_form_result').empty(); // !compatibility
            if (!self.check_error_fields({})) {
                self.update_status('error', _t("Please fill in the form correctly."));
                return false;
            }

            // Prepare form inputs
            this.form_fields = this.$target.serializeArray();
            $.each(this.$target.find('input[type=file]:not([disabled])'), (outer_index, input) => {
                $.each($(input).prop('files'), function (index, file) {
                    // Index field name as ajax won't accept arrays of files
                    // when aggregating multiple files into a single field value
                    self.form_fields.push({
                        name: input.name + '[' + outer_index + '][' + index + ']',
                        value: file
                    });
                });
            });

            // Serialize form inputs into a single object
            // Aggregate multiple values into arrays
            var form_values = {};
            _.each(this.form_fields, function (input) {
                if (input.name in form_values) {
                    // If a value already exists for this field,
                    // we are facing a x2many field, so we store
                    // the values in an array.
                    if (Array.isArray(form_values[input.name])) {
                        form_values[input.name].push(input.value);
                    } else {
                        form_values[input.name] = [form_values[input.name], input.value];
                    }
                } else {
                    if (input.value !== '') {
                        form_values[input.name] = input.value;
                    }
                }
            });

            // force server date format usage for existing fields
            this.$target.find('.s_website_form_field:not(.s_website_form_custom)')
            .find('.s_website_form_date, .s_website_form_datetime').each(function () {
                var date = $(this).datetimepicker('viewDate').clone().locale('en');
                var format = 'YYYY-MM-DD';
                if ($(this).hasClass('s_website_form_datetime')) {
                    date = date.utc();
                    format = 'YYYY-MM-DD HH:mm:ss';
                }
                form_values[$(this).find('input').attr('name')] = date.format(format);
            });

            if (this._recaptchaLoaded) {
                const tokenObj = await this._recaptcha.getToken('website_form');
                if (tokenObj.token) {
                    form_values['recaptcha_token_response'] = tokenObj.token;
                } else if (tokenObj.error) {
                    self.update_status('error', tokenObj.error);
                    return false;
                }
            }
            if(this.$target.data('model_name') == 'crm.lead'){
                form_values['website_url'] = window.location.href
            }
            // Post form and handle result
            ajax.post(this.$target.attr('action') + (this.$target.data('force_action') || this.$target.data('model_name')), form_values)
            .then(async function (result_data) {
                // Restore send button behavior
                self.$target.find('.s_website_form_send, .o_website_form_send')
                    .removeAttr('disabled')
                    .removeClass('disabled'); // !compatibility
                result_data = JSON.parse(result_data);
                if (!result_data.id) {
                    // Failure, the server didn't return the created record ID
                    self.update_status('error', result_data.error ? result_data.error : false);
                    if (result_data.error_fields) {
                        // If the server return a list of bad fields, show these fields for users
                        self.check_error_fields(result_data.error_fields);
                    }
                } else {
                    // Success, redirect or update status
                    let successMode = self.$target[0].dataset.successMode;
                    let successPage = self.$target[0].dataset.successPage;
                    if (!successMode) {
                        successPage = self.$target.attr('data-success_page'); // Compatibility
                        successMode = successPage ? 'redirect' : 'nothing';
                    }
                    switch (successMode) {
                        case 'redirect': {
                            let hashIndex = successPage.indexOf("#");
                            if (hashIndex > 0) {
                                // URL containing an anchor detected: extract
                                // the anchor from the URL if the URL is the
                                // same as the current page URL so we can scroll
                                // directly to the element (if found) later
                                // instead of redirecting.
                                // Note that both currentUrlPath and successPage
                                // can exist with or without a trailing slash
                                // before the hash (e.g. "domain.com#footer" or
                                // "domain.com/#footer"). Therefore, if they are
                                // not present, we add them to be able to
                                // compare the two variables correctly.
                                let currentUrlPath = window.location.pathname;
                                if (!currentUrlPath.endsWith("/")) {
                                    currentUrlPath = currentUrlPath + "/";
                                }
                                if (!successPage.includes("/#")) {
                                    successPage = successPage.replace("#", "/#");
                                    hashIndex++;
                                }
                                if ([successPage, "/" + session.lang_url_code + successPage].some(link => link.startsWith(currentUrlPath + '#'))) {
                                    successPage = successPage.substring(hashIndex);
                                }
                            }
                            if (successPage.charAt(0) === "#") {
                                const successAnchorEl = document.getElementById(successPage.substring(1));
                                if (successAnchorEl) {
                                    await dom.scrollTo(successAnchorEl, {
                                        duration: 500,
                                        extraOffset: 0,
                                    });
                                }
                                break;
                            }
                            $(window.location).attr('href', successPage);
                            return;
                        }
                        case 'message': {
                            // Prevent double-clicking on the send button and
                            // add a upload loading effect (delay before success
                            // message)
                            await concurrency.delay(dom.DEBOUNCE);

                            self.$target[0].classList.add('d-none');
                            self.$target[0].parentElement.querySelector('.s_website_form_end_message').classList.remove('d-none');
                            break;
                        }
                        default: {
                            // Prevent double-clicking on the send button and
                            // add a upload loading effect (delay before success
                            // message)
                            await concurrency.delay(dom.DEBOUNCE);

                            self.update_status('success');
                            break;
                        }
                    }

                    self.$target[0].reset();
                    self.restoreBtnLoading();
                }
            })
            .guardedCatch(error => {
                this.update_status(
                    'error',
                    error.status && error.status === 413 ? _t("Uploaded file is too large.") : "",
                );
            });
        },
    })
});