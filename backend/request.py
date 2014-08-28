import urllib
import urllib2

class Request(object):

	GET = 0
	POST = 1

	def __init__(self, url, data, auth=()):
		self.url = url
		self.data = data
		self.auth = auth

	def get_request(self, req_type, encoded_data):
		requests = {self.GET : urllib2.Request(self.url + '?' + encoded_data),
					self.POST : urllib2.Request(self.url, encoded_data)}

		return requests.get(req_type, requests[0])

	def send_request(self, req_type=GET):
		if len(self.auth) == 2:
			self.set_up_auth(self.auth[0], self.auth[1])

		encoded_data = urllib.urlencode(self.data)
		request = self.get_request(req_type, encoded_data)

		try:
			response = urllib2.urlopen(request)
		except urllib2.HTTPError, e:
			# print e.read()
			return False
		return response

	def set_up_auth(self, username, password):
		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

		# Add the username and password.
		password_mgr.add_password(None, self.url, username, password)
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)

		# Create "opener" (OpenerDirector instance)
		opener = urllib2.build_opener(handler)

		# Use the opener to fetch a URL
		# This is commented out because calling it results in an HTTP Error 405
		# opener.open(self.url)

		# Install the opener.
		urllib2.install_opener(opener)
