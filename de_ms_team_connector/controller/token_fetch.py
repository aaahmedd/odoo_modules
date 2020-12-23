import json
import logging
import requests
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class Controller_for_token(http.Controller):
    @http.route('/token', type="http", auth="public", website=True)
    def token(self, **kw):
        company_creditionals = http.request.env['res.users'].sudo().search([], limit=1).company_id

        try:
            if kw.get('code'):
                company_creditionals.write({'authr_url': kw.get('code')})
                if company_creditionals:
                    app_id = company_creditionals.id_of_application
                    secrt_id = company_creditionals.client_secret
                    url_for_redirection = company_creditionals.redirect_uri
                    url_for_token = 'https://login.microsoftonline.com/common/oauth2/v2.0/token?scope=onlinemeetings.readwrite'
                    header = {"Content-type": "application/x-www-form-urlencoded"}
                    payload = {
                        'client_id': app_id,
                        'code': kw.get('code'),
                        'redirect_uri': url_for_redirection,
                        'grant_type': "authorization_code",
                        'client_secret': secrt_id
                    }

                    token_resp = requests.post(url_for_token, data=payload, headers=header)

                    print(token_resp.status_code)
                    print(kw.get('code'))
                    print(app_id)
                    print(secrt_id)
                    if token_resp.status_code == 200:
                        prd_res_tok = json.loads(token_resp.text.encode('utf8'))
                        company_creditionals.write({"access_token": prd_res_tok.get('access_token'),
                                        "refresh_token": prd_res_tok.get('refresh_token')})
                        url = "https://graph.microsoft.com/v1.0/me"
                        bearer = 'Bearer ' + prd_res_tok.get('access_token')
                        header = {
                            'Content-Type': "application/json",
                            'Authorization': bearer
                        }

                        requests_response = requests.request("GET", url, headers=header)
                        if requests_response.status_code == 200:
                            prd_respon = requests_response.json()
                            print(prd_respon.get('displayName'))

                        return request.render("de_ms_team_connector.sucess_message")
                    else:
                        return request.render("de_ms_team_connector.failed_message")

        except Exception as e:
            raise UserWarning(str(e))
