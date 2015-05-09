#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from io import BytesIO

import tornado.ioloop
import tornado.web

import misaka
import xhtml2pdf.pisa as pisa

#解决中文字体
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('msyh', './msyh.ttf'))
from xhtml2pdf import default
default.DEFAULT_FONT["helvetica"]="msyh"

class BaseHandler(tornado.web.RequestHandler):
    """docstring for BaseHandler"""
    def get(self):
        # raise HTTPError(404)
        self.write_error(404)
        
    def write_error(self, status_code, **kwargs):
        # self.finish('404 NOT FOUND!!' + str(status_code))
        msg = '404 NOT FOUND!!'
        self.render('error.html',msg=msg)

class root(BaseHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        file = self.request.files['filedata'][0]
        filedata = file['body']
        print file['content_type']
        reload(sys)
        sys.setdefaultencoding('utf-8')
        try:
            html = misaka.html(filedata)
            buffer = BytesIO()
            pdf = pisa.CreatePDF(html,buffer)
            pdf = buffer.getvalue()
            buffer.close()
            saved_file_name = 'attachment; filename=' + file['filename'] + '.pdf'

            self.set_header("Content-Type", "application/pdf")
            self.set_header('Content-Disposition', saved_file_name)
            self.write(pdf)
        except Exception, e:
            msg = "The File is not written using markdown!"
            self.render("error.html",msg=msg)



settings = {
    'debug': True,
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'gzip': True,
}

handlers = [
    (r'/', root),
    (r'/.*', BaseHandler),
]

application = tornado.web.Application(handlers, **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()