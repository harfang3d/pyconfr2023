import sys
from urllib.parse import urlencode
import asyncio
import platform
import json


class RequestHandler:
    """
    WASM compatible request handler
    auto-detects emscripten environment and sends requests using JavaScript Fetch API
    """
    GET = 'GET'
    POST = 'POST'
    _js_code = ""
    _init = False

    def __init__(self):
        self.is_emscripten = True if sys.platform == 'emscripten' else False
        if not self._init:
            self.init()
        self.debug = True
        self.result = None
        if not self.is_emscripten:
            try:
                import requests
                self.requests = requests
            except ImportError:
                pass

    def init(self):
        if self.is_emscripten:
            self._js_code = """
            // generator functions for async fetch API
            // script is meant to be run at runtime in an emscripten environment

            // Fetch API allows data to be posted along with a POST request
            window.POST = function * POST (url, data)
            {
                // post info about the request
                console.log("POST: " + url + "\nData: " + data);
                var request = new Request(url, {method: 'POST', body: JSON.stringify(data)})
                var content = 'undefined';
                fetch(request)
               .then(resp => resp.text())
               .then((resp) => {
                    console.log(resp);
                    content = resp;
               })
               .catch(err => {
                     // handle errors
                     console.log("An Error Occurred:")
                     console.log(err);
                });

                while(content == 'undefined'){
                    yield content;
                }
            }

            // Only URL to be passed 
            // when called from python code, use urllib.parse.urlencode to get the query string
            window.GET = function * GET (url)
            {
                console.log("GET: " + url);
                var request = new Request(url, { method: 'GET' })
                var content = 'undefined';
                fetch(request)
               .then(resp => resp.text())
               .then((resp) => {
                    console.log(resp);
                    content = resp;
               })
               .catch(err => {
                     // handle errors
                     console.log("An Error Occurred:");
                     console.log(err);
                });

                while(content == 'undefined'){
                    // generator
                    yield content;
                }
            }
            """
            try:
                platform.window.eval(self._js_code)
            except AttributeError:
                self.is_emscripten = False

    @staticmethod
    def read_file(file):
        # synchronous reading of file intended for evaluating on initialization
        # use async functions during runtime
        with open(file, 'r') as f:
            data = f.read()
        return data

    @staticmethod
    def print(*args, default=True):
        try:
            for i in args:
                platform.window.console.log(i)
        except AttributeError:
            pass
        except Exception as e:
            return e
        if default:
            print(*args)

    async def get(self, url, params=None, doseq=False):
        # await asyncio.sleep(5)
        if params is None:
            params = {}
        if self.is_emscripten:
            query_string = urlencode(params, doseq=doseq)
            await asyncio.sleep(0)
            content = await platform.jsiter(platform.window.GET(url + "?" + query_string))
            if self.debug:
                self.print(content)
            self.result = content
        else:
            self.result = self.requests.get(url, params).text
        return self.result

    # def get(self, url, params=None, doseq=False):
    #     return await self._get(url, params, doseq)

    async def post(self, url, data=None):
        if data is None:
            data = {}
        if self.is_emscripten:
            await asyncio.sleep(0)
            content = await platform.jsiter(platform.window.POST(url, json.dumps(data)))
            if self.debug:
                self.print(content)
            self.result = content
        else:
            self.result = self.requests.post(url, data).text
        return self.result

    # def post(self, url, data=None):
    #     return await self._post(url, data)
