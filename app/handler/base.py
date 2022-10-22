# -*- coding: utf-8 -*-

import time
import uuid
import datetime
import tornado.web

from app.config import CONF
DEBUG = CONF.getboolean('general', 'debug')
SELF = CONF.get('general', 'self')

class BaseHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ('GET', 'POST', 'OPTIONS')


    def on_finish(self):
        pass

    def write_log(self):
        pass

    def check(self):
        pass

    def get_cors_allow_origin(self, origin=None):
        return origin or '*'

    def initialize(self, *args, **kargs):
        now = datetime.datetime.now()
        self.request.uuid = now.strftime('%y%m%d%H%M%S') + '-' +  uuid.uuid4().hex[:8].upper()

    def options(self, *args, **kargs):
        pass

    def prepare(self):
        #local timezone
        self.set_header('X-SERVER-LOCALTIME', time.strftime('%Y-%m-%d %H:%M:%S %z'))

        #cors
        headers = self.request.headers
        origin = headers.get('Origin', None) or None
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Methods', headers.get('Access-Control-Request-Method', ''));
        self.set_header('Access-Control-Allow-Headers', headers.get('Access-Control-Request-Headers', ''))
        self.set_header('Access-Control-Allow-Origin', self.get_cors_allow_origin(origin))

        if headers.get('Content-Type', '').startswith('multipart/form-data'):
            self.p = ObjectDict({})
        else:
            self.p = self.all_arguments()

        self.check()
        if self._finished: return


    def render_string(self, template_name, **kwargs):
        # If no template_path is specified, use the path of the calling file
        RequestHandler = tornado.web.RequestHandler

        template_path = self.get_template_path()
        if not template_path:
            frame = sys._getframe(0)
            web_file = frame.f_code.co_filename
            while frame.f_code.co_filename == web_file:
                frame = frame.f_back
            template_path = os.path.dirname(frame.f_code.co_filename)
        with RequestHandler._template_loader_lock:
            if template_path not in RequestHandler._template_loaders:
                loader = self.create_template_loader(template_path)
                RequestHandler._template_loaders[template_path] = loader
            else:
                loader = RequestHandler._template_loaders[template_path]

        t = loader.load(template_name)
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url,
            template_name=template_name, #ZYS
        )
        args.update(kwargs)
        return t.generate(**args)

    def get_error_html(self, status_code, **kargs):
        if not getattr(self, 'uuid', None): self.uuid = ''

        try:
            return self.render_string('%s.html' % status_code, uuid=self.uuid)
        except:
            return 'ERROR, %s, %s'.format(status_code, self.uuid)

    def get_argument_int(self, key, default=None, min=0):
        v = str(self.get_argument(key, default))
        return int(v) if v and v.isdigit() and int(v) >= min else default

    def get_argument_enum(self, key, choice=[], default=None):
        v = self.get_argument(key, default)
        choice = [str(x) for x in choice]
        return v if v in choice else default

    def finish(self, chunk=None):
        if self._status_code != 200:
            super(BaseHandler, self).finish(chunk)
            return

        body = chunk
        if body is None:
            body = b''.join(self._write_buffer)
            try:
                body = json_decode(body)
            except:
                body = None

        if self.request.method == 'POST' and self.current_user and isinstance(body, dict) and body['code'] == 0:
            self.write_log()

        super(BaseHandler, self).finish(chunk)

    def all_arguments(self):
        all = {}
        for k in self.request.arguments:
            all[k] = self.get_argument(k, '').strip()
        return ObjectDict(all)

    def add_header(self, name, value):
        'hack SameSite'

        if name != 'Set-Cookie':
            return super().add_header(name, value)

        if DEBUG:
            if 'Secure' in value:
                value = value.replace('Secure', 'SameSite=None; Secure', 1)
        return super().add_header(name, value)

    def set_cookie(self, *args, **kargs):
        'add secure'

        if SELF[:5] == 'https':
            kargs['secure'] = True
        super().set_cookie(*args, **kargs)


class ObjectDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return ''

    def __setattr__(self, name, value):
        self[name] = value


