#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 


import tornado.web
import tornado.ioloop

import httplib2
import json

h = httplib2.Http("~/.cache/httplib2/")

class HomeHandler(tornado.web.RequestHandler):
        def get(self):
                self.render("home.html")

        def post(self):
                action_id = self.get_argument("action_id")
                inputurl = self.get_argument("inputurl")
                if not (inputurl.startswith("http://") or inputurl.startswith("https://")):
                        inputurl = "http://" + inputurl
                if action_id == "shorten":
                        result = get_short_url(inputurl)
                        if result is not None:
                                self.render("result.html", result_url = result)
                elif action_id == "long":
                        result = get_long_url(inputurl)
                        if result is not None:
                                self.render("result.html", result_url = result)
                
                self.set_status(500)


def get_long_url(shorturl):
        rsp, content = h.request("https://www.googleapis.com/urlshortener/v1/url?shortUrl=" + shorturl)
        if rsp.status == 200:
                j = json.loads(content.decode())
                if j["status"] == "OK":
                        return j["longUrl"]


def get_short_url(longurl):
        rsp, content = h.request("https://www.googleapis.com/urlshortener/v1/url", "POST", 
                        json.dumps({"longUrl":longurl}), {"Content-Type": "application/json"})
        if rsp.status == 200:
                j = json.loads(content.decode())
                return j["id"]



app = tornado.web.Application([
        (r"/", HomeHandler)
        ], template_path="template")


if __name__ == "__main__":
        app.listen(8888)
        tornado.ioloop.IOLoop.instance().start()



# vim: ai ts=8 sts=8 et sw=8
