import unittest
from mock import patch
import simplejson as json

from .context import app


app.config['TWILIO_ACCOUNT_SID'] = 'ACxxxxxx'
app.config['TWILIO_AUTH_TOKEN'] = 'yyyyyyyyy'
app.config['TWILIO_CALLER_ID'] = '+15558675309'
app.config['NYTIMES_API_KEY'] = '###'


class TwiMLTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def assertTwiML(self, response):
        self.assertTrue("<Response>" in response.data, "Did not find " \
                "<Response>: %s" % response.data)
        self.assertTrue("</Response>" in response.data, "Did not find " \
                "</Response>: %s" % response.data)
        self.assertEqual("200 OK", response.status)

    def sms(self, body, url='/sms', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309', extra_params=None):
        params = {
            'SmsSid': 'SMtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to,
            'From': from_,
            'Body': body,
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        if extra_params:
            params = dict(params.items() + extra_params.items())
        return self.app.post(url, data=params)

    def call(self, url='/voice', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309', digits=None, extra_params=None):
        params = {
            'CallSid': 'CAtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to,
            'From': from_,
            'CallStatus': 'ringing',
            'Direction': 'inbound',
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        if digits:
            params['Digits'] = digits
        if extra_params:
            params = dict(params.items() + extra_params.items())
        return self.app.post(url, data=params)


class ConferenceTests(TwiMLTest):
    def test_voice(self):
        response = self.call(url="/conference/conference_test")
        self.assertTwiML(response)
        self.assertTrue('<Conference' in response.data, "Could not find " \
                "<Conference> in response: %s" % response.data)


class WaitTests(TwiMLTest):
    @patch('requests.get')
    def test_waitUrl(self, MockRequests):
        mock_request = MockRequests()
        mock_request.status_code = 200
        mock_good_json = json.loads(
                open('./tests/test_assets/good.json').read())
        mock_request.json.return_value = mock_good_json

        response = self.call(url="/wait")

        self.assertTwiML(response)
        self.assertTrue("<Say voice=\"alice\">" in response.data,
                "Could not find <Say> verb in response: %s" % response.data)

    @patch('requests.get')
    def test_waitUrlAuthError(self, MockRequests):
        mock_request = MockRequests()
        mock_request.status_code = 403

        response = self.call(url="/wait")

        self.assertTwiML(response)
        self.assertTrue("<Redirect>" in response.data, "Could not find hold " \
                "music in failed response: %s" % response.data)

    @patch('requests.get')
    def test_waitUrlBadJson(self, MockRequests):
        mock_request = MockRequests()
        mock_request.status_code = 200
        mock_request.json.return_value = None

        response = self.call(url="/wait")

        self.assertTwiML(response)
        self.assertTrue("<Redirect>" in response.data, "Could not find hold " \
                "music in failed response: %s" % response.data)

    def test_waitUrlNoKey(self):
        app.config['NYTIMES_API_KEY'] = None

        response = self.call(url="/wait")

        self.assertTwiML(response)
        self.assertTrue("Configuration error" in response.data, "Could not " \
                "find configuration error message in response: %s" %
                response.data)
        self.assertTrue("<Redirect>" in response.data, "Could not find hold " \
                "music in failed response: %s" % response.data)

    def test_music(self):
        response = self.call(url="/music")

        self.assertTwiML(response)
        self.assertTrue("<Play>" in response.data, "Could not find music in " \
                "response: %s" % response.data)
