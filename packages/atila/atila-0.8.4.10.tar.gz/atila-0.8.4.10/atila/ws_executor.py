from . import wsgi_executor
from aquests.protocols.http import respcodes
from skitai.backbone.http_response import catch

class Executor (wsgi_executor.Executor):
	def __call__ (self):
		self.was = self.env ["skitai.was"]
		current_app, wsfunc = self.env.get ("websocket.handler")
		self.was.subapp = current_app
		try:
			content = wsfunc (self.was, **self.env.get ("websocket.params", {}))
		except:
			content = self.was.app.debug and "[ERROR] " + catch (0) or "[ERROR]"
		self.was.subapp = None
		return content
