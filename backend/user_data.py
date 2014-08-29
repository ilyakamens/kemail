import time
import pickle

from google.appengine.api import memcache

class UserData(object):
	"""Memcache wrapper for caching user data.

	This memcache wrapper keeps track of the number
	of emails the user sends in a given today, and can
	be used to cache draft emails.

	Attributes:
		DAILY_LIMIT: Maximum number of emails a user can send in a day
	"""
	# Number of emails a user can send per day
	DAILY_LIMIT = 100

	def __init__(self, user):
		"""Initialize the UserData and store the user.

		Args:
			user: An instance of Google's User class (https://developers.google.com/appengine/docs/python/users/userclass)

		Raises:
			An exception if the user isn't a valid User object
		"""
		if not user:
			# This should never happen
			raise Exception('Invalid User object')
		else:
			self.user = user
	
	def get_daily_limit_key(self):
		"""Dynamically construct and return the user's daily email key
		based on the user's id and the numeric day of the month."""
		return self.user.user_id() + '_' + time.strftime("%d")

	def get_num_emails_sent_today(self):
		"""Return the number of emails the current user has sent today."""
		result = memcache.get(self.get_daily_limit_key())
		return result if result else 0 # Handles the case memcache returns 'None'

	def get_num_emails_left_today(self):
		"""Return the remaining number of emails the user can send today."""
		return UserData.DAILY_LIMIT - self.get_num_emails_sent_today()

	def can_send_emails_today(self):
		"""Return True if the user can send more emails today, and False otherwise."""
		return self.get_num_emails_left_today() > 0

	def increment_emails_sent_today(self):
		"""Increment the number of emails the user has sent today by one."""
		memcache.incr(self.get_daily_limit_key(), 1, None, 0)

	def get_request_key(self):
		"""Dynamically construct and return the user's email draft
		key based on the user's id."""
		return self.user.user_id() + '_request'

	def store_request(self, request):
		"""Cache the email the user was attempting to send. This data
		is stored for a maximum of one day.

		Args:
			request: An instance of Google's Request class that has the email data
					(https://developers.google.com/appengine/docs/python/tools/webapp/requestclass)

		"""
		data = {}
		data['addressee_email'] = request.get("addressee_email")
		data['subject'] = request.get("subject")
		data['message'] = request.get("message")
		memcache.set(self.get_request_key(), pickle.dumps(data), 86400)

	def get_request(self):
		"""Return the cached email draft if it's there, or None if not."""
		data = memcache.get(self.get_request_key())
		return pickle.loads(data) if data else None

	def delete_request(self):
		"""Clear the cached email draft if it's cached."""
		memcache.delete(self.get_request_key())


