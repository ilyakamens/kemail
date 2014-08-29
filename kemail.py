import webapp2

from backend.emailer import *
from backend.user_data import *
from backend.email_validator import *
from google.appengine.api import users

# HTML page module names, used as parameters to get_client_response()
EMAIL_FORM = 'email_form'
SEND_SUCCESS = 'send_success'
SEND_FAIL = 'send_fail'
LIMIT_REACHED = 'limit_reached'
LOG_IN = 'log_in'
INVALID_EMAIL = 'invalid_email'

def get_client_response(module_name, optional_params=()):
    """Opens the HTML page and adds necessary data so it can be sent to the user.

    Adds the proper path to the HTML module name, inserts the proper data into the file,
    opens and reads the file so it can be sent to the user and displayed in their browser.
    Note that the number of elements in optional_params must match the number of replacements
    in the HTML file.

    Args:
        module_name: The module name of the desired HTML file. Possible options include:
                    EMAIL_FORM, SEND_SUCCESS, SEND_FAIL, LIMIT_REACHED, LOG_IN, INVALID_EMAIL
        optional_params: A tuple of data to be replaced in the HTML file

    Returns:
        The HTML file and inserted data as a string.
    """
    return open('./frontend/%s.html' % module_name, 'r').read() % optional_params

class DefaultHandler(webapp2.RequestHandler):
    """Default handler that serves HTTP GET requests at the root directory.

    Handles GET requests to the root directory and serves different responses
    based on the state of the user.

    Attributes:
        There are many... see Google's docs for more detail:
        (https://developers.google.com/appengine/docs/python/tools/webapp/requesthandlerclass)
    """

    def get(self):
        """Serves HTTP GET requests.

        Redirects for user authentication, displays a form to send an email, or informs the
        user they have reached their email limit for the day. This is the starting
        point for sending an email. This will also serve the email form with a cached email
        draft depending on the the user's state.
        """
        user = users.get_current_user()     

        if user:    # Make sure user is logged in
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
        """Get data for the email form (email_form.html) that users use to send emails.

        Get user data for the email form, including the number of emails
        the user can send, a personalized message, and possibly a cached draft
        email if the user previously tried to send an email to an invalid address.

        Args:
            user: A valid user object of the current user (https://developers.google.com/appengine/docs/python/users/userclass#User)
            user_data: A UserData object to get possibly cached data
            num_emails_left_day: The number of emails the user can send today

        Returns:
            A variable length tuple of data to be inserted into email_form.html
        """
        plural = 's' if num_emails_left_today != 1 else ''      # Hacky way to show 'email' vs. 'emails'
        form_data = (user.nickname(), num_emails_left_today, plural)
        data = user_data.get_request()

        if data:    # If there's a cached email draft, add it to the data going into the form
            form_data += (data.get('addressee_email', ''), data.get('subject', ''), data.get('message', ''))
        else:
            form_data += ('', '', '')

        return form_data

class EmailHandler(webapp2.RequestHandler):
    """Serves HTTP GET and POST requests at the /email directory.

    If a GET request is made here, redirect the user to the root
    directoy (the email form). If it's a POST, do some validation on the
    data and the user, and then attempt to send the email.

    Attributes:
        There are many... see Google's docs for more detail:
        (https://developers.google.com/appengine/docs/python/tools/webapp/requesthandlerclass)
    """

    def get(self):
        """Handle GET requests made to /email. Redirect the user to the root directory."""
        self.redirect('/')

    def post(self):
        """Handle POST requests made to /email.

        Do some validation on the user and the data, and then attempt to
        send the email. If the email addressee is email or the email fails
        to send, cache the email draft in case the user tries again.
        """
        user = users.get_current_user()
        if user:    # Make sure user is logged in
            user_data = UserData(user)
            if user_data.can_send_emails_today():
                email_validator = EmailValidator(self.request)
                valid_dest, dest, suggestion = email_validator.is_valid_email()
                if valid_dest:  # If 'to' email is valid
                    emailer = Emailer(self.request, user) 
                    if emailer.send_email():
                        message = get_client_response(SEND_SUCCESS)
                    else:
                        user_data.store_request(self.request)
                        message = get_client_response(SEND_FAIL, (user.nickname()))
                else:
                    user_data.store_request(self.request)
                    # This is hacky, but I'm not sure how to get around this 
                    # without adding a new .html file, which I don't think is much better
                    suggestion = "Did you mean '%s'?" % suggestion if suggestion else ""
                    message = get_client_response(INVALID_EMAIL, (dest, suggestion))
            else:
                message = get_client_response(LIMIT_REACHED, (user.nickname()))
        else:
            message = get_client_response(LOG_IN)

        self.response.write(message)

# Assign handler classes to their respective paths
application = webapp2.WSGIApplication([
    ('/', DefaultHandler),
    ('/email', EmailHandler)
], debug=True)
