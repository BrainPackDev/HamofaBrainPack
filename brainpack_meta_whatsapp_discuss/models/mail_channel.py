from odoo import _, api, fields, models, modules, Command

class Channel(models.Model):

    _inherit = 'mail.channel'

    @api.model
    def channel_get(self, partners_to, pin=True):
        """ Get the canonical private channel between some partners, create it if needed.
            To reuse an old channel (conversation), this one must be private, and contains
            only the given partners.
            :param partners_to : list of res.partner ids to add to the conversation
            :param pin : True if getting the channel should pin it for the current user
            :returns: channel_info of the created or existing channel
            :rtype: dict
        """
        partner_info = False
        if self.env.user.partner_id.id not in partners_to:
            partner_info = self.env['res.partner'].sudo().search([('id', 'in', partners_to)])
            partners_to.append(self.env.user.partner_id.id)
        # determine type according to the number of partner in the channel
        else:
            partner_info = self.env['res.partner'].sudo().search([('id', 'in', partners_to)])
        self.flush_model()
        self.env['mail.channel.member'].flush_model()
        provider_channel_id = partner_info.channel_provider_line_ids.filtered(lambda s: s.provider_id == self.env.user.provider_id)
        if provider_channel_id:
            if not all(x in provider_channel_id.channel_id.channel_partner_ids.ids for x in partners_to):
                provider_channel_id = False
        if not provider_channel_id:
            provider_channel_id = self.env.user.partner_id.channel_provider_line_ids.filtered(lambda s: s.provider_id == self.env.user.provider_id)
            if not all(x in provider_channel_id.channel_id.channel_partner_ids.ids for x in partners_to):
                provider_channel_id = False

        if provider_channel_id:
            # get the existing channel between the given partners
            channel = self.browse(provider_channel_id.channel_id.id)
            # pin up the channel for the current partner
            if pin:
                self.env['mail.channel.member'].search(
                    [('partner_id', '=', self.env.user.partner_id.id), ('channel_id', '=', channel.id)]).write(
                    {'is_pinned': True})
            channel._broadcast(self.env.user.partner_id.ids)
        else:
            self.env.cr.execute("""
                        SELECT M.channel_id
                        FROM mail_channel C, mail_channel_member M
                        WHERE M.channel_id = C.id
                            AND M.partner_id IN %s
                            AND C.channel_type LIKE 'chat'
                            AND NOT EXISTS (
                                SELECT 1
                                FROM mail_channel_member M2
                                WHERE M2.channel_id = C.id
                                    AND M2.partner_id NOT IN %s
                            )
                        GROUP BY M.channel_id
                        HAVING ARRAY_AGG(DISTINCT M.partner_id ORDER BY M.partner_id) = %s
                        LIMIT 1
                    """, (tuple(partners_to), tuple(partners_to), sorted(list(partners_to)),))
            result = self.env.cr.dictfetchall()
            if result:
                # get the existing channel between the given partners
                channel = self.browse(result[0].get('channel_id'))
                # pin up the channel for the current partner
                if pin:
                    self.env['mail.channel.member'].search(
                        [('partner_id', '=', self.env.user.partner_id.id), ('channel_id', '=', channel.id)]).write({
                        'is_pinned': True,
                        'last_interest_dt': fields.Datetime.now(),
                    })
                channel._broadcast(self.env.user.partner_id.ids)
                return channel.channel_info()[0]

            # create a new one
            channel = self.create({
                'channel_partner_ids': [(4, partner_id) for partner_id in partners_to],
                'channel_member_ids': [
                    Command.create({
                        'partner_id': partner_id,
                        # only pin for the current user, so the chat does not show up for the correspondent until a message has been sent
                        'is_pinned': partner_id == self.env.user.partner_id.id
                    }) for partner_id in partners_to
                ],
                'channel_type': 'chat',
                # 'email_send': False,
                'name': ', '.join(self.env['res.partner'].sudo().browse(partners_to).mapped('name')),
            })
            have_user = self.env['res.users'].search([('partner_id','in',partner_info.ids)])
            if not have_user:
                channel.whatsapp_channel = True
            if partner_info:
                # partner_info.channel_id = channel.id
                partner_info.write({'channel_provider_line_ids': [
                    (0, 0, {'channel_id': channel.id, 'provider_id': self.env.user.provider_id.id})]})
            mail_channel_partner = self.env['mail.channel.member'].sudo().search(
                [('channel_id', '=', channel.id), ('partner_id', '=', self.env.user.partner_id.id)])
            mail_channel_partner.write({'is_pinned': True})
            channel._broadcast(partners_to)
        return channel.channel_info()[0]

    def get_channel_agent(self, channel_id):
        if self.env.user:
            channel = self.env['mail.channel'].sudo().browse(int(channel_id))
            partner_lst = channel.channel_partner_ids.ids
            channel_users = self.env['res.users'].sudo().search_read([('partner_id.id', 'in', partner_lst)],
                                                                     ['id', 'name'])
            users = self.env['res.users'].sudo().search([('partner_id.id', 'not in', partner_lst)])
            users_lst = []
            for user in users:
                if user.has_group('brainpack_meta_whatsapp.whatsapp_group_user') and user.provider_id and user.provider_id == self.env.user.provider_id:
                    users_lst.append({'name': user.name, 'id': user.id})
            dict = {'channel_users': channel_users, 'users': users_lst}
            return dict

    def add_agent(self, user_id, channel_id):
        user = self.env['res.users'].sudo().browse(int(user_id))
        channel = self.env['mail.channel'].sudo().browse(int(channel_id))
        if channel.whatsapp_channel:
            channel.write({'channel_partner_ids': [(4, user.partner_id.id)]})
            mail_channel_partner = self.env['mail.channel.member'].sudo().search(
                [('channel_id', '=', channel_id),
                 ('partner_id', '=', user.partner_id.id)])
            mail_channel_partner.write({'is_pinned': True})
            return True

    def remove_agent(self, user_id, channel_id):
        user = self.env['res.users'].sudo().browse(int(user_id))
        channel = self.env['mail.channel'].sudo().browse(int(channel_id))
        if channel.whatsapp_channel:
            channel.write({'channel_partner_ids': [(3, user.partner_id.id)]})
            return True

    @api.constrains('channel_member_ids', 'channel_partner_ids')
    def _constraint_partners_chat(self):
        pass