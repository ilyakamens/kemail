import os, re, httplib

class Emailer(object):

	def __init__(self, request, user_data):
		self.request = request
		self.user_data = user_data

	def get_dynamic_inst_data(self):
		path = os.path.abspath(os.path.dirname(__file__))   
		file_names = os.listdir(path)
		regex = re.compile("_email\.py$", re.IGNORECASE)
		pruned_file_names = filter(regex.search, file_names)  
		module_names = self.get_mod_name(pruned_file_names)

		# Create list of (module name, module) pairs for dynamic class instantiation
		return [(module_name, __import__(module_name, globals(), locals(), ['object'], -1)) for module_name in module_names]

	def send_email(self):
		dynamic_inst_data = self.get_dynamic_inst_data()

		for module_name, module in dynamic_inst_data:
			if module_name != 'base_email':
				# Load class from imported module
				class_name = self.get_class_name(module_name)
				loaded_class = getattr(module, class_name)

				# Create an instance of the class
				instance = loaded_class(self.request)
				response = instance.send_email()
				if not response or response.code != httplib.OK:
					continue
				else:
					self.user_data.increment_emails_sent_today()
					self.user_data.delete_request()
					# print response.read()
					return True

		return False

	def get_mod_name(self, file_names):
		return [os.path.splitext(file_name)[0] for file_name in file_names]

	def get_class_name(self, mod_name):
	    # Return the class name from a plugin name
	    output = ''

	    # Split on the _ and ignore the 1st word plugin
	    words = mod_name.split('_')

	    # Capitalize the first letter of each word and add to string
	    for word in words:
	        output += word.title()
	    return output