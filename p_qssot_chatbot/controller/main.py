from odoo.addons.mail.controllers.bus import MailChatController
from odoo.addons.im_livechat.controllers.main import LivechatController
from odoo import http, _
from odoo import SUPERUSER_ID, tools
from odoo.http import request, route
from odoo.addons.p_qssot_chatbot import bot_testing


class MailChatController_bot(MailChatController):

    @route('/mail/chat_post', type="json", auth="public", cors="*")
    def mail_chat_post(self, uuid, message_content, **kwargs):
        mail_channel = request.env["mail.channel"].sudo().search([('uuid', '=', uuid)], limit=1)
        if mail_channel and not mail_channel.channel_current_stage:
            mail_channel.sudo().write({
                'channel_current_stage': 'setting_1'
            })

        call_super = super(MailChatController_bot, self).mail_chat_post(uuid, message_content, **kwargs)
        if not mail_channel:
            return call_super

        chatbot_end_str_1 = request.env['ir.config_parameter'].sudo().get_param('p_qssot_chatbot.chatbot_end_str_1')
        chatbot_end_str_2 = request.env['ir.config_parameter'].sudo().get_param('p_qssot_chatbot.chatbot_end_str_2')
        chatbot_selection_2 = request.env['ir.config_parameter'].sudo().get_param(
            'p_qssot_chatbot.chatbot_selection_2')
        chatbot_selection_1 = request.env['ir.config_parameter'].sudo().get_param(
            'p_qssot_chatbot.chatbot_selection_1')
        print(uuid)
        print(message_content)
        print(chatbot_end_str_1)
        print(chatbot_end_str_2)
        if mail_channel.channel_current_stage == 'setting_1':

            if chatbot_selection_1 == 'chatbot':
                bot_reply = bot_testing.get_bot_output(message_content)
                if bot_reply:
                    body = tools.plaintext2html(bot_reply)
                    mail_channel.with_context(mail_create_nosubscribe=True).message_post(
                        author_id=mail_channel.livechat_operator_id.id,
                        body=body,
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment')
                else:
                    body = tools.plaintext2html(
                        "Type '%s' to connect with %s" % (chatbot_end_str_1, chatbot_selection_2))
                    mail_channel.with_context(mail_create_nosubscribe=True).message_post(
                        author_id=mail_channel.livechat_operator_id.id,
                        body=body,
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment')

        elif mail_channel.channel_current_stage == 'setting_2':

            if chatbot_selection_2 == 'chatbot':
                bot_reply = bot_testing.get_bot_output(message_content)
                if bot_reply:
                    body = tools.plaintext2html(bot_reply)
                    mail_channel.with_context(mail_create_nosubscribe=True).message_post(
                        author_id=mail_channel.livechat_operator_id.id,
                        body=body,
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment')
                else:
                    body = tools.plaintext2html(
                        "Type '%s' to connect with %s" % (chatbot_end_str_2, chatbot_selection_1))
                    mail_channel.with_context(mail_create_nosubscribe=True).message_post(
                        author_id=mail_channel.livechat_operator_id.id,
                        body=body,
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment')

        if str(message_content) == str(chatbot_end_str_1):
            mail_channel.write({
                'channel_current_stage': 'setting_2'
            })

        elif str(message_content) == str(chatbot_end_str_2):
            mail_channel.write({
                'channel_current_stage': 'setting_1'
            })

        return call_super


class LivechatController_bot(LivechatController):

    @http.route('/im_livechat/get_session', type="json", auth='public', cors="*")
    def get_session(self, channel_id, anonymous_name, previous_operator_id=None, **kwargs):
        return super(LivechatController_bot, self).get_session(channel_id, anonymous_name,
                                                               previous_operator_id=previous_operator_id, **kwargs)
