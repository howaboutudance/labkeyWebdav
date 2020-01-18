
from typing import Any, MutableMapping

import requests


class ServerConfig:
	def __init__(self, server: str, verify: bool = True) -> None:
		self.server_url = server
		self.verify_ssl = verify

	def getOptions(self, params: MutableMapping[str, Any] = None) -> MutableMapping[str, Any]:
		opts = {"verify": self.verify_ssl}
		if self.authenication_method == "basic":
			opts.update({"auth": (self.username, self.password)})
		if self.authenication_method == "apikey":
			opts.update({"headers": {"apikey": self.api_key}})
		else:
			raise ValueError

		if params:
			opts.update({"params": params})

		return opts


	def getByUrl(self, url: str, params: MutableMapping[str, Any] = None):
		return requests.get(self.createURL(url), **self.getOptions(params))

	def lsFiles(self, folder_path: str) -> MutableMapping[str, str]:
		response = self.getByUrl(folder_path, params={"params": {"method": "JSON"}})
		files = response["files"]
		return response["files"]

	def createURL(self, folder_path):
		return self.server_url + folder_path

	def setBasicAuth(self, username: str, password: str) -> None:
		self.authenication_method = "basic"
		self.password = password
		self.username = username

	def setApiKey(self, key: str) -> None:
		self.authenication_method = "apikey"
		self.api_key = key

	def getCSRF(self):
		pass

