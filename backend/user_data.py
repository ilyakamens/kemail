import time
import pickle

from google.appengine.api import memcache

class UserData(object):

	# Number of emails a user can send per day
	DAILY_LIMIT = 100

	def __init__(self, user):
		if not user:
			# This should never happen
			raise Exception('Invalid User object')
		else:
			self.user = user
	
	def get_daily_limit_key(self):
		## Key = user id concatenated with numeric day of the month
		return self.user.user_id() + '_' + time.strftime("%d")

	def get_num_emails_sent_today(self):
		result = memcache.get(self.get_daily_limit_key())
		# Handles the case memcache returns 'None'
		return result if result else 0

	def get_num_emails_left_today(self):
		return UserData.DAILY_LIMIT - self.get_num_emails_sent_today()

	def can_send_emails_today(self):
		return self.get_num_emails_left_today() > 0

	def increment_emails_sent_today(self):
		memcache.incr(self.get_daily_limit_key(), 1, None, 0)

	def get_request_key(self):
		## Key = user id concatenated with '_request'
		return self.user.user_id() + '_request'

	def store_request(self, request):
		data = {}
		data['addressee_email'] = request.get("addressee_email")
		data['subject'] = request.get("subject")
		data['message'] = request.get("message")
		memcache.set(self.get_request_key(), pickle.dumps(data), 86400)

	def get_request(self):
		data = memcache.get(self.get_request_key())
		return pickle.loads(data) if data else None

	def delete_request(self):
		memcache.delete(self.get_request_key())


