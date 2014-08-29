import urllib
import urllib2

class Request(object):
	"""Simple class to make HTTP GET and POST requests.

	This is a simple wrapper around urllib's and urllib2's fuctionality
	to encapsulate HTTP GET and POST requests, and includes basic HTTP
	authentication.

	Attributes:
		GET: A const-like var to indicate the request should be GET (used with self.send_request())
		POST: A const-like var to indicate the request should be POST (used with self.send_request())
		url: The destination of the request
		data: Data the destination server needs for the request
		auth: 2-element tuple of authentication data containing a username and password
	"""
	# Const-like vars to use with self.send_request() to dictate the type of request being sent
	GET = 0
	POST = 1

	def __init__(self, url, data, auth=()):
		"""Initialize this class with a url, data, and optional authentication data.

		Args:
			url: The url to make the request to
			data: Data the destination server needs for the request
			auth: 2-element tuple with username and password for basic authentication
		"""
		self.url = url
		self.data = data
		self.auth = auth

	def get_request(self, req_type, encoded_data):
		"""Return the urllbi2 Request object we need to send a request.

		This is fairly un-Pythonic, but it essentially creates an optimized
		switch-case statement (e.g. a hash) and returns the proper request
		based on the request type. This can be extended for other request types.

		Args:
			req_type: Currently only GET or POST; indicates the type of the request
			encoded_data: Data to be added to the request. The way urllib2 works, the
						  request type is decided based on how the extra data is passed in.

		Returns:
			A urllib2 Request object to make an HTTP request. If an invalid req_type was passed
			in, it will default to GET.
		"""
		requests = {self.GET : urllib2.Request(self.url + '?' + encoded_data),
					self.POST : urllib2.Request(self.url, encoded_data)}

		return requests.get(req_type, requests[0])

	def send_request(self, req_type=GET):
		"""Send an HTTP request.

		This currently only sends HTTP GET or POST requests. It will construct
		the request based on the req_type, conditionally add authentication, and
		send the request.

		Args:
			req_type: The type of request to make (e.g. GET or POST). Defaults to GET.

		Returns:
			False if urlopen throws an Exception, otherwise the HTTP response
		"""
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
		"""Sets up basic HTTP username/password authentication.

		Arguments:
			username: The username to use for the authentication
			password: The password to use for the authentication
		"""
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, self.url, username, password)
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(handler)

		# This is commented out because calling it results in an HTTP Error 405 exception.
		# It hasn't been removed because it initally worked and was part of the sample code
		# opener.open(self.url)

		urllib2.install_opener(opener)
