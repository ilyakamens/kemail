import urllib
import urllib2

class Request(object):

	GET = 0
	POST = 1

	def __init__(self, url, data):
		self.url = url
		self.data = data

	def get_request(self, req_type, encoded_data):
		requests = {self.GET : urllib2.Request(self.url + '?' + encoded_data),
					self.POST : urllib2.Request(self.url, encoded_data)}

		return requests.get(req_type, requests[0])

	def send_request(self, req_type=GET):
		encoded_data = urllib.urlencode(self.data)
		request = self.get_request(req_type, encoded_data)

		try:
			response = urllib2.urlopen(request)
		except urllib2.HTTPError:
			return False
		return response
