from odoo.modules import module
get_module_resource = module.get_resource_path

def get_module_icon(module):
    iconpath = ['static', 'description', 'icon.png']
    if module in ['account_accountant']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'accounting.png']
    elif module == 'sale_subscription':
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'subscription.png']
    elif module in ['appointment']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'appointment.png']
    elif module in ['hr_appraisal']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'appraisals.png']
    elif module in ['approvals']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'approvals.png']
    elif module in ['hr_attendance']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'attendance.png']
    elif module in ['stock_barcode']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'barcode.png']
    elif module in ['website_blog']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'blogs.png']
    elif module in ['calendar']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'calender.png']
    elif module in ['account_consolidation']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'consolidation.png']
    elif module in ['contacts']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'contacts.png']
    elif module in ['crm']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'crm.png']
    elif module in ['data_recycle','data_merge','data_cleaning']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'data-recycle.png']
    elif module in ['mail','mail_bot']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'discuss.png']
    elif module in ['documents']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'documents.png']
    elif module in ['website_sale','website_sale_digital','website_sale_loyalty']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'eCommerce.png']
    elif module in ['website_slides']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'eLearning.png']
    elif module in ['mass_mailing']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'emailAutomation.png']
    elif module in ['hr_contract']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'employee-contract.png']
    elif module in ['hr']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'employees.png']
    elif module in ['website_event','event']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'events.png']
    elif module in ['hr_expense']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'expenses.png']
    elif module in ['industry_fsm','industry_fsm_sale','industry_fsm_stock']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'field-service.png']
    elif module in ['fleet']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'fleet.png']
    elif module in ['website_helpdesk_forum','website_forum']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'forum.png']
    elif module in ['helpdesk','website_helpdesk_slides','helpdesk_account','helpdesk_fsm','helpdesk_sale_loyalty','helpdesk_stock','helpdesk_timesheet','helpdesk_mgmt']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'helpdesk.png']
    elif module in ['iot']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'internet-of-things.png']
    elif module in ['stock']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'inventory.png']
    elif module in ['account']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'invoicing.png']
    elif module in ['knowledge']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'knowledge.png']
    elif module in ['im_livechat','website_helpdesk_livechat','website_livechat']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'liveChat.png']
    elif module in ['lunch']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'lunch.png']
    elif module in ['maintenance']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'maintanance.png']
    elif module in ['mrp']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'manufacturing.png']
    elif module in ['marketing_automation','social']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'marketingAutomation.png']
    elif module in ['note']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'notes.png']
    elif module in ['website_hr_recruitment']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'online-jib.png']
    elif module in ['hr_payroll']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payroll.png']
    elif module in ['planning','project_forecast']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'planning.png']
    elif module in ['mrp_plm']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'plm.png']
    elif module in ['point_of_sale']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'pointOfSale.png']
    elif module in ['project']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'project.png']
    elif module in ['purchase','iap']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'purchases.png']
    elif module in ['quality_control']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'quality.png']
    elif module in ['hr_recruitment']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'recruitment.png']
    elif module in ['hr_referral']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'refferals.png']
    elif module in ['sale_renting']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'rental.png']
    elif module in ['repair','helpdesk_repair']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'repair.png']
    elif module in ['sale','sale_management']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'sales.png']
    elif module in ['sign']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'signs.png']
    elif module in ['hr_skills']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'skill-management.png']
    elif module in ['mass_mailing_sms','sms']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'smsMarketing.png']
    elif module in ['web_studio']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'studio.png']
    elif module in ['survey']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'surveys.png']
    elif module in ['hr_holidays']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'timeOff.png']
    elif module in ['timesheet_grid','hr_timesheet','sale_timesheet']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'timeSheet.png']
    elif module in ['voip','voip_onsip']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'VoIP.png']
    elif module in ['website']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'website-builder.png']
    elif module in ['sale_amazon']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'amazon_connector.png']
    elif module in ['delivery_bpost']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'bpost.png']
    elif module in ['board','spreadsheet_dashboard']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'dashboard.png']
    elif module in ['delivery_dhl']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'DHL.png']
    elif module in ['delivery_easypost']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'easypost.png']
    elif module in ['sale_ebay']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'ebay_connector.png']
    elif module in ['delivery_fedex']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'fedex.png']
    elif module in ['delivery_sendcloud']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'sendcloud.png']
    elif module in ['delivery_ups']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'UPS.png']
    elif module in ['delivery_usps']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'usps.png']
    elif module in ['account_auto_transfer']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'account_automatic_transfers.png']
    elif module in ['account_asset']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'asset_management.png']
    elif module in ['website_crm']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'contac_form.png']
    elif module in ['google_gmail']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'gmail.png']
    elif module in ['google_calendar']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'google_calender.png']
    elif module in ['hr_expense_extract']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'hr_expense_extract.png']
    elif module in ['account_bank_statement_import_ofx']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'import_OFX_bank_statement.png']
    elif module in ['account_bank_statement_import_qif']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'import_QIF_bank_statement.png']
    elif module in ['iap']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'in_app_purchase.png']
    elif module in ['mrp_maintenance']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'maintanance_mrp.png']
    elif module in ['membership']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'member.png']
    elif module in ['microsoft_outlook']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'outlook_calender.png']
    elif module in ['microsoft_calendar']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'outlook_calender.png']
    elif module in ['partner_autocomplete']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'partner_autocomplete.png']
    elif module in ['payment']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_engine.png']
    elif module in ['product']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'product_and_pricelist.png']
    elif module in ['sale_timesheet']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'sales_timesheet.png']
    elif module in ['hr_work_entry_contract']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'work_entries_contract.png']
    elif module in ['payment_demo']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_demo.png']
    elif module in ['payment_flutterwave']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_flutterwave.png']
    elif module in ['payment_mercado_pago']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_mercadopago.png']
    elif module in ['payment_mollie']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_mollie.png']
    elif module in ['payment_ogone']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_ogone.png']
    elif module in ['payment_paypal']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_paypal.png']
    elif module in ['payment_payumoney',]:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_payUmoney.png']
    elif module in ['payment_payulatam']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_payUmoney_latam.png']
    elif module in ['payment_razorpay']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_razorpay.png']
    elif module in ['payment_sepa_direct_debit']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_sepadirectdebit.png']
    elif module in ['payment_sips']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_stripe.png']
    elif module in ['payment_stripe']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_worldlinesips.png']

    elif module in ['website_event_track']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'advanced_events.png']
    elif module in ['website_customer']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'customer_references.png']
    elif module in ['website_sale_delivery']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'ecommerce_delivery.png']
    elif module in ['website_google_map']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'google_maps.png']
    elif module in ['website_links', 'link_tracker']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'link_tracker.png']
    elif module in ['website_mass_mailing']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'newsletter_subscribe_button.png']
    elif module in ['website_event_sale']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'online_event_ticketing.png']
    elif module in ['website_membership']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'online_member_directory.png']
    elif module in ['website_form_project']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'online_task_submission.png']
    elif module in ['payment_alipay']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_alipay.png']
    elif module in ['payment_aps']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_amazonpay.png']
    elif module in ['payment_asiapay']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_asiapay.png']
    elif module in ['payment_authorize']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_authorize_net.png']
    elif module in ['payment_adyen']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_ayden.png']
    elif module in ['payment_buckaroo']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_buckaroo.png']
    elif module in ['payment_custom']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_custom_payment_method.png']
    elif module in ['website_sale_stock']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'product_availibility.png']
    elif module in ['website_sale_comparison']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'product_comparison.png']
    elif module in ['website_event_questions']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'questions_on_event.png']
    elif module in ['website_crm_partner_assign']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'resellers.png']
    elif module in ['website_sale_wishlist']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'shoppers_wishlist.png']
    elif module in ['snailmail']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'snail_mail.png']
    elif module in ['social_facebook']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'social_facebook.png']
    elif module in ['social_instagram']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'social_instagram.png']
    elif module in ['social_youtube']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'social_youtube.png']
    elif module in ['social_twitter']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'social_twitteer.png']
    elif module in ['spreadsheet_dashboard']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'spreadsheet_dashboard.png']
    elif module in ['test_exceptions']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'test_exception.png']
    elif module in ['transifex']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'transifex_integration.png']
    elif module in ['website_twitter']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'twitter_snippet.png']
    elif module in ['website_twitter_wall']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'twitter_wall.png']
    elif module in ['web_unsplash']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'unsplash_image_library.png']
    elif module in ['website_payment']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'website_payment.png']
    elif module in ['website_enterprise']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'website_enterprise.png']
    elif module in ['utm']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'utm_tracker.png']
    elif module in ['social_linkedin']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'social_linkedin.png']
    elif module in ['website_partner']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'website_planner.png']
    elif module in ['gamification']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'gamify.png']
    elif module in ['account_sepa']:
        module = 'brainpack_debranding'
        iconpath = ['static', 'description/blue', 'payment_provider_sepadirectdebit.png']

    if get_module_resource(module, *iconpath):
        return ('/' + module + '/') + '/'.join(iconpath)
    return '/base/'  + '/'.join(iconpath)

module.get_module_icon = get_module_icon
