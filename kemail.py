import webapp2

from backend.emailer import *
from backend.user_data import *
from google.appengine.api import users

EMAIL_FORM = 'email_form'
SEND_SUCCESS = 'send_success'
SEND_FAIL = 'send_fail'
LIMIT_REACHED = 'limit_reached'
LOG_IN = 'log_in'

def get_client_response(file_name, optional_params=()):
    return open('./frontend/%s.html' % file_name, 'r').read() % optional_params

class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            user_data = UserData(user)
            num_emails_left_today = user_data.get_num_emails_left_today()

            if num_emails_left_today > 0:
                # Hacky way to show 'email' vs. 'emails'
                plural = 's' if num_emails_left_today != 1 else ''
                message = get_client_response(EMAIL_FORM, (user.nickname(), num_emails_left_today, plural))
            else:
                message = get_client_response(LIMIT_REACHED, (user.nickname()))

            self.response.write(message)
        else:
            self.redirect(users.create_login_url(self.request.uri))

class EmailHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

    def post(self):

        # validate data...
        # if validation passes...

        user = users.get_current_user()
        if user:
            user_data = UserData(user)
            if user_data.can_send_emails_today():
                emailer = Emailer(user_data) 
                if emailer.send_email(self.request):
                    message = get_client_response(SEND_SUCCESS)
                else:
                    message = get_client_response(SEND_FAIL, (user.nickname()))
            else:
                message = get_client_response(LIMIT_REACHED, (user.nickname()))
        else:
            message = get_client_response(LOG_IN)

        self.response.write(message)

application = webapp2.WSGIApplication([
    ('/', DefaultHandler),
    ('/email', EmailHandler)
], debug=True)
