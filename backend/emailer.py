import pkgutil, sys, os, re, httplib, urllib2

class Emailer(object):

	@staticmethod
	def get_dynamic_inst_data():
		path = os.path.abspath(os.path.dirname(__file__))   
		file_names = os.listdir(path)
		regex = re.compile("_email\.py$", re.IGNORECASE)
		pruned_file_names = filter(regex.search, file_names)  
		module_names = Emailer.get_mod_name(pruned_file_names)

		# Create list of (module name, module) pairs for dynamic class instantiation
		return [(module_name, __import__(module_name, globals(), locals(), ['object'], -1)) for module_name in module_names]

	@staticmethod
	def send_email(request):
		dynamic_inst_data = Emailer.get_dynamic_inst_data()

		for module_name, module in dynamic_inst_data:
			if module_name != 'base_email':
				# Load class from imported module
				class_name = Emailer.get_class_name(module_name)
				loaded_class = getattr(module, class_name)

				# Create an instance of the class
				instance = loaded_class(request)
				try:
					response = instance.send_email()
				except urllib2.HTTPError:
					continue

				if response.code == httplib.OK:
					return True

		return False

	@staticmethod
	def get_mod_name(file_names):
		return [os.path.splitext(file_name)[0] for file_name in file_names]

	@staticmethod
	def get_class_name(mod_name):
	    # Return the class name from a plugin name
	    output = ''

	    # Split on the _ and ignore the 1st word plugin
	    words = mod_name.split('_')

	    # Capitalize the first letter of each word and add to string
	    for word in words:
	        output += word.title()
	    return output