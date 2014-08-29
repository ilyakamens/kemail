import os, re, httplib

from user_data import *

class Emailer(object):
	"""Top-level class to send emails.

	This is the top-level class to use to send emails. This class
	is the abstraction layer to send an email using an arbitrary
	email service's API.

	Attributes:
		request: The user's POST request that contains the email data (https://developers.google.com/appengine/docs/python/tools/webapp/requestclass)
		user: An instance of Google's User object (https://developers.google.com/appengine/docs/python/users/userclass) 
	"""

	def __init__(self, request, user):
		"""Initialize this object and assign the request and user objects.

		Args:
			request: The POST request from the user with the email data
			user: An instance of Google's User object (https://developers.google.com/appengine/docs/python/users/userclass) 
		"""
		self.request = request
		self.user = user

	def get_dynamic_inst_data(self):
		"""Get a list of module data for dynamic email class construction

		This will get a list of all the modules and module names in
		the /backend dir that end with 'dynamic_email.py'. The list
		is later used for dynamic class instantiation, so that other
		email services can be used without modifying any code in this file.

		Returns:
			A list of 2-element tuples containing the module name and
			corresponding loaded module. Example:

			[(sendgrid_dynamic_email.py, *sendgrid_module*), (mailgun_dynamic_email.py, *mailgun_module*)]
		"""
		path = os.path.abspath(os.path.dirname(__file__))   
		file_names = os.listdir(path)
		regex = re.compile("dynamic_email\.py$", re.IGNORECASE)
		pruned_file_names = filter(regex.search, file_names)  
		module_names = self.get_mod_name(pruned_file_names)

		# Create list of (module name, module) pairs for dynamic class instantiation
		return [(module_name, __import__(module_name, globals(), locals(), ['object'], -1)) for module_name in module_names]

	def send_email(self):
		"""Sends an email with the instance attributes.

		Specifically, this will iterate through the dynamic instance
		data, instantiate an email class, try to send an email with that
		instance, and either continue with the next module in the list if
		the email failed to send or stop and return the result if it succeeded.

		This also where the logic that keeps track of the number of emails sent
		for each user occurs. 

		Returns:
			- True if one of the email classes successfully sent an email, False otherwise
		"""
		dynamic_inst_data = self.get_dynamic_inst_data()

		for module_name, module in dynamic_inst_data:
			# All the class parsing, loading, and instantiate logic
			class_name = self.get_class_name(module_name)
			loaded_class = getattr(module, class_name)
			instance = loaded_class(self.request, self.user)
			response = instance.send_email()

			# If the email failed to send, continue through the list and try another class
			if not response or response.code != httplib.OK:
				continue
			else:
				user_data = UserData(self.user)
				user_data.increment_emails_sent_today()
				# We do this here in case a draft was saved elsewhere,
				# otherwise the user could try to send another email
				# and the old draft (which just successfully sent) would appear
				user_data.delete_request()
				# print response.read()
				return True

		return False

	def get_mod_name(self, file_names):
		"""Returns a list of correspoding module names from a list of file names

		Args:
			file_names: The list of file_names we're constructing the list of module names from
		"""
		return [os.path.splitext(file_name)[0] for file_name in file_names]

	def get_class_name(self, mod_name):
		"""Returns a class name from a module name

		Args:
			mod_name: The module name we're transforming into a class name

		Returns:
			A corresponding class name. Example:

				mod_name = some_example_module
				output = SomeExampleModule
		"""
	    output = ''
	    words = mod_name.split('_')

	    for word in words:
	        output += word.title()
	    return output