# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
import requests
import base64
from dateutil.parser import parse as duparse
from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError
import xmlrpc.client


_logger = logging.getLogger(__name__)


class Credetionals(models.Model):
    _inherit = "res.company"

    id_of_application = fields.Char("Application ID", help="The application ID you obtain from the microsoft team app.")
    client_secret = fields.Char("Client Secret", help="The client Secret key you obtain from the microsoft team.")
    authr_url = fields.Char("Authorization URL", help="")
    redirect_uri = fields.Char("Redirect URIs", help="", default="http://localhost:8069/token")
    auth_code = fields.Char("Auth Code", help="")
    access_token = fields.Char("Access Token", help="")
    refresh_token = fields.Char("Refresh Token", help="")

    def test_connection(self):
        if not self.id_of_application or not self.redirect_uri or not self.client_secret:
            raise UserError(_('Please Enter Credentials First!'))

        auth_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?'
        access_type = 'offline'
        id_of_client = self.id_of_application
        url_redirect = self.redirect_uri

        url = auth_url + 'client_id=' + id_of_client + '&response_type=code&redirect_uri=' + url_redirect + '&response_mode=query&scope=offline_access%20user.read%20mail.send%20onlinemeetings.readwrite&state=12345'

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }

    def genrate_ref_new_token(self):
        client_id = self.id_of_application
        client_secret = self.client_secret
        redirect_uri = self.redirect_uri
        refresh_token = self.refresh_token
        request_token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token?scope=offline_access%20user.read%20onlinemeetings.readwrite'
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        data = {
            'client_id': client_id,
            'refresh_token': refresh_token,
            'redirect_uri': redirect_uri,
            'grant_type': "refresh_token",
            'client_secret': client_secret
        }

        response = requests.post(request_token_url, data=data, headers=headers)

        if response.status_code == 200:
            parsed_response = response.json()
            self.access_token = parsed_response.get('access_token')

            context = dict(self._context)
            context['message'] = 'Operation Successful!'
            return self.message_wizard(context)

        elif response.status_code == 401:
            _logger.error("Access token/refresh token is expired")
            _logger.error("Token Expired!")
        else:
            raise Warning("We got a issue !!!! Desc : {}".format(response.text))


    def message_wizard(self, context):
        return {
            'name': ('Success'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }