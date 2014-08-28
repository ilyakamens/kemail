import webapp2

from backend.emailer import *
from backend.user_data import *
from backend.email_validator import *
from google.appengine.api import users

EMAIL_FORM = 'email_form'
SEND_SUCCESS = 'send_success'
SEND_FAIL = 'send_fail'
LIMIT_REACHED = 'limit_reached'
LOG_IN = 'log_in'
INVALID_EMAIL = 'invalid_email'

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
                data = self.get_form_data(user, user_data, num_emails_left_today)
                message = get_client_response(EMAIL_FORM, data)
            else:
                message = get_client_response(LIMIT_REACHED, (user.nickname()))

            self.response.write(message)
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get_form_data(self, user, user_data, num_emails_left_today):
        # Hacky way to show 'email' vs. 'emails'
        plural = 's' if num_emails_left_today != 1 else ''
        form_data = (user.nickname(), num_emails_left_today, plural)
        data = user_data.get_request()
        
        if data:
            form_data += (data.get('addressee_email', ''),
                        cgi.escape(data.get('subject', '')),
                        cgi.escape(data.get('message', '')))
        else:
            form_data += ('', '', '')

        return form_data

    def post(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            user_data = UserData(user)
            user_data.store_request(self.request)
            self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class EmailHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

    def post(self):
        user = users.get_current_user()
        if user:
            user_data = UserData(user)
            if user_data.can_send_emails_today():
                email_validator = EmailValidator(self.request)
                valid_dest, dest, suggestion = email_validator.is_valid_email()
                if valid_dest:
                    emailer = Emailer(self.request, user_data) 
                    if emailer.send_email():
                        message = get_client_response(SEND_SUCCESS)
                    else:
                        message = get_client_response(SEND_FAIL, (user.nickname()))
                else:
                    user_data.store_request(self.request)
                    suggestion = "Did you mean '%s'?" % suggestion if suggestion else ""
                    message = get_client_response(INVALID_EMAIL, (dest, suggestion))
            else:
                message = get_client_response(LIMIT_REACHED, (user.nickname()))
        else:
            message = get_client_response(LOG_IN)

        self.response.write(message)

application = webapp2.WSGIApplication([
    ('/', DefaultHandler),
    ('/email', EmailHandler)
], debug=True)
