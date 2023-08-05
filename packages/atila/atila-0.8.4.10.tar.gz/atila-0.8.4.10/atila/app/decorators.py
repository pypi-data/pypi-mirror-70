from functools import wraps
import os
import time, threading
import re
import inspect
import skitai

class Decorators:
    def __init__ (self):
        self.handlers = {}
        self._ws_channels = {}
        self._maintern_funcs = {}
        self._mount_option = {}
        self._testpasses = {}
        self._decos = {
            "bearer_handler": self.default_bearer_handler
        }
        self._reloading = False
        self._function_specs = {}
        self._current_function_specs = {}
        self._parameter_caches = {}
        self._conditions = {}
        self._cond_check_lock = threading.RLock ()
        self._binds_server = [None] * 7
        self._binds_request = [None] * 4

    # function param saver ------------------------------------------
    def get_func_id (self, func, mount_option = None):
        mount_option = mount_option or self._mount_option
        return ("ns" in mount_option and mount_option ["ns"] + "." or "") + func.__name__

    def save_function_spec (self, func):
        # save original function spec for preventing distortion by decorating wrapper
        # all wrapper has *args and **karg but we want to keep original function spec for auto parametering call
        func_id = self.get_func_id (func)
        if func_id not in self._function_specs or func_id not in self._current_function_specs:
            # save origin spec
            self._function_specs [func_id] = inspect.getfullargspec (func)
            self._current_function_specs [func_id] = None
        return func_id

    def get_function_spec (self, func, mount_option = None):
        # called by websocet_handler with mount_option
        func_id = self.get_func_id (func, mount_option)
        return self._function_specs.get (func_id)

    # app life cycling -------------------------------------------
    def before_mount (self, f):
        self._binds_server [0] = f
        return f
    start_up = before_mount
    startup = before_mount

    def mounted (self, f):
        self._binds_server [3] = f
        return f

    def mounted_or_reloaded (self, f):
        self._binds_server [6] = f
        return f

    def before_reload (self, f):
        self._binds_server [5] = f
        return f
    onreload = before_reload
    reload = before_reload

    def reloaded (self, f):
        self._binds_server [1] = f
        return f

    def before_umount (self, f):
        self._binds_server [4] = f
        return f

    def umounted (self, f):
        self._binds_server [2] = f
        return f
    shutdown = umounted

    # Request chains ----------------------------------------------
    def before_request (self, f):
        self._binds_request [0] = f
        return f

    def finish_request (self, f):
        self._binds_request [1] = f
        return f

    def failed_request (self, f):
        self._binds_request [2] = f
        return f

    def teardown_request (self, f):
        self._binds_request [3] = f
        return f

    def testpass_required (self, testfunc):
        def decorator(f):
            func_id = self.save_function_spec (f)
            self._testpasses [func_id] = testfunc
            self.set_auth_flag (f, ('testpass', testfunc.__name__))
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                testfunc = self._testpasses [func_id]
                response = testfunc (was)
                if response is False:
                    return was.response ("403 Permission Denied")
                elif response is not True and response is not None:
                    return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator

    # parameter helpers ------------------------------------------------
    RX_EMAIL = re.compile (r"[a-z0-9][-.a-z0-9]*@[-a-z0-9]+\.[-.a-z0-9]{2,}[a-z]$", re.I)
    RX_UUID = re.compile (r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
    RX_UNSAFE = re.compile (r"(<script[\s>]|['\"=]\s*javascript:|\son[:a-z]+\s*=\s*|&#x[0-9a-f]{2};|┻━┻)", re.I)
    PARAM_CUSTOM_TYPES = {'required', 'leastone', 'emails', 'uuids'}
    PARAM_TYPES = {'ints', 'floats', 'lists', 'strings', 'dicts', 'booleans', 'ranges', 'safes', 'notags'}
    def _validate_param (self, params, **kargs):
        params = params or {}
        for k in list (kargs.keys ()):
            if k in self.PARAM_CUSTOM_TYPES:
                fields = kargs.pop (k)
                if k == 'required':
                    for each in fields:
                        if not params.get (each):
                            return 'parameter {} required'.format (each)

                elif k == 'leastone':
                    vals = []
                    for fd in fields:
                        vals.append (params.get (fd) is not None and 1 or 0)
                    if sum (vals) == 0:
                        return 'at least one parameter of {} are required'.format (', '.join (leastone))

                elif k == 'emails':
                    for fd in fields:
                        kargs [fd] = self.RX_EMAIL

                elif k == 'uuids':
                    for fd in fields:
                        kargs [fd] = self.RX_UUID

            elif k in self.PARAM_TYPES:
                types = kargs.pop (k)
                for each in types:
                    try:
                        val = params [each]
                    except KeyError:
                        continue

                    if val is None:
                        continue

                    try:
                        if k == 'ints':
                            val = int (val)
                        elif k == 'floats':
                            val = float (val)
                        elif k == 'lists':
                            if not isinstance (val, (str, list, tuple)):
                                return 'parameter {} should be a list or bar delimtered string'.format (each)
                            if isinstance (val, str):
                                val = val.split ("|")
                        elif k == 'strings':
                            if not isinstance (val, str):
                                raise ValueError
                        elif k == 'dicts':
                            if not isinstance (val, dict):
                                raise ValueError
                        elif k == 'booleans':
                            if val in ('yes', 'true', 'y', 't'): val = True
                            elif val in ('no', 'false', 'n', 'f'): val = False
                            if val not in (True, False):
                                return 'parameter {} should be a boolean (one of yes, no, y, n, t, f, true or false)'.format (each)
                        elif k == 'ranges':
                            a, b = map (int, val.split ('~'))
                            val = (a, b)
                        elif k == 'safes':
                            if self.RX_UNSAFE.search (val):
                                return 'parameter {} is unsafe'.format (each)
                        elif k == 'notags':
                            val = val.replace ('<', '&lt;').replace ('>', '&gt;')
                        params [each] = val

                    except ValueError:
                        return 'parameter {} should be {} type'.format (each, k [:-1])

        for fd_, cond in kargs.items ():
            ops = fd_.split ("__")
            fd = ops [0]
            val = params.get (fd)
            if val is None:
                continue

            if not (len (ops) <= 3 and fd):
                raise SyntaxError ("invalid require expression on {}".format (fd))

            if len (ops) == 1:
                if type (cond) is type:
                    if not isinstance (val, cond):
                        return 'parameter {} should be an instance of {}'.format (fd, cond)
                elif isinstance (cond, (list, tuple)):
                    matched = False
                    for each in cond:
                        if isinstance (val, each):
                            matched = True
                            break
                    if not matched:
                        return 'parameter {} is invalid type'.format (fd)
                elif hasattr (cond, "search"):
                    if not cond.search (val):
                        return 'parameter {} is invalid'.format (fd)
                elif val != cond:
                    return 'parameter {} is invalid'.format (fd)
                continue

            if len (ops) == 3:
                if ops [1] == "len":
                    val = len (val)
                    fd = "length of {}".format (fd)

            op = ops [-1]
            val = (isinstance (cond, (list, tuple)) and type (cond [0]) or type (cond)) (val)

            # mostly comaptible with sqlphile operators -------------------
            if op == "between":
                if not (cond [0] <= val <= cond [1]):
                    return 'parameter {} should be between {} ~ {}'.format (fd, cond [0], cond [1])
            elif op == "in":
                if val not in cond:
                    return 'parameter {} should be one of {}'.format (fd, cond)
            elif op == "notin":
                if val in cond:
                    return 'parameter {} should be not one of {}'.format (fd, cond)

            elif op in ("eq", "exact"):
                if val != cond:
                    return 'parameter {} should be {}'.format (fd, cond)
            elif op == "neq":
                if val == cond:
                    return 'parameter {} should not be {}'.format (fd, cond)
            elif op == "lte":
                if val > cond:
                    return 'parameter {} should less or equal than {}'.format (fd, cond)
            elif op == "lt":
                if val >= cond:
                    return 'parameter {} should less than {}'.format (fd, cond)
            elif op == "gte":
                if val < cond:
                    return 'parameter {} should greater or equal than {}'.format (fd, cond)
            elif op == "gt":
                if val <= cond:
                    return 'parameter {} should greater than {}'.format (fd, cond)

            elif op == "startswith":
                if not val.startswith (cond):
                    return 'parameter {} should be start with {}'.format (fd, cond)
            elif op == "endswith":
                if not val.endswith (cond):
                    return 'parameter {} should be end with {}'.format (fd, cond)
            elif op == "nstartswith":
                if val.startswith (cond):
                    return 'parameter {} should be not start with {}'.format (fd, cond)
            elif op == "nendswith":
                if val.endswith (cond):
                    return 'parameter {} should be not end with {}'.format (fd, cond)
            elif op == "contains":
                if val.find (cond) == -1:
                    return 'parameter {} should be contain {}'.format (fd, cond)
            elif op == "ncontains":
                if val.find (cond) != -1:
                    return 'parameter {} should be not contain {}'.format (fd, cond)

            elif op == "regex":
                if not re.compile (cond).search (val):
                    return 'parameter {} should not be {}'.format (fd, cond)
            else:
                raise ValueError ("Unknown operator: {}".format (op))

        if 'nones' in kargs: # must be None if not val
            nones = kargs ['nones']
            for each in nones:
                try:
                    if not params [each]:
                        params [each] = None
                except KeyError:
                    pass

    def get_parameter_requirements (self, func_id):
        return self._parameter_caches.get (func_id, {})

    def require (self, scope = 'ARGS', required = None, **kargs):
        # required, leastone, ints, floats, uuids, emails, nones, lists, strings, booleans, dicts, notags, safes, ranges, **kargs
        def decorator (f):
            self.save_function_spec (f)
            func_id = self.get_func_id (f)
            if func_id not in self._parameter_caches:
                self._parameter_caches [func_id] = {}
            if required:
                kargs ['required'] = required

            for k, v in kargs.items ():
                if (k in self.PARAM_CUSTOM_TYPES or k in self.PARAM_TYPES) and isinstance (v, str):
                    kargs [k] = v.split ()
                else:
                    kargs [k] = v
            self._parameter_caches [func_id][scope] = kargs

            @wraps (f)
            def wrapper (was, *args, **kwargs):
                scope_ = scope
                if scope in ("FORM", "JSON", "DATA"):
                    if was.request.method not in {"POST", "PUT", "PATCH"}:
                        return f (was, *args, **kwargs)
                    if scope == "JSON" and not was.request.get_header ("content-type", '').startswith ("application/json"):
                        return f (was, *args, **kwargs)

                elif scope not in ("URL", "ARGS"):
                    if was.request.method != scope:
                        return f (was, *args, **kwargs)
                    if scope in {"GET", "DELETE"}:
                        scope_ = "URL"
                    elif scope in {"POST", "PUT", "PATCH"}:
                        if was.request.get_header ("content-type", '').startswith ("application/json"):
                            scope_ = "JSON"
                        else:
                            scope_ = "FORM"
                    else:
                        return f (was, *args, **kwargs)

                validatable_args = getattr (was.request, scope_)
                more_info = self._validate_param (validatable_args, **kargs)
                if more_info:
                    return was.response.adaptive_error ("400 Bad Request", 'missing or bad parameter in {}'.format (scope_), 40050, more_info)

                # syncing args --------------------------------------
                for k, v in validatable_args.items ():
                    if k in kwargs:
                        kwargs [k] = v
                    if scope_ in ("FORM", "JSON", "URL", "DATA"):
                        was.request.ARGS [k] = v
                    if scope_ == "ARGS":
                        for other_ in ("DATA", "URL"):
                            target_ = getattr (was.request, other_)
                            if target_ and k in target_:
                                target_ [k] = v
                return f (was, *args, **kwargs)

            return wrapper
        return decorator
    parameters_required = params_required = test_params = require

    # Automation ------------------------------------------------------
    def run_before (self, *funcs):
        def decorator(f):
            self.save_function_spec (f)
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                for func in funcs:
                    response = func (was)
                    if response is not None:
                        return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator

    def run_after (self, *funcs):
        def decorator(f):
            self.save_function_spec (f)
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                response = f (was, *args, **kwargs)
                for func in funcs:
                    func (was)
                return response
            return wrapper
        return decorator

    # Conditional Automation ------------------------------------------------------
    def _check_condition (self, was, key, func, interval, mtime_func):
        now = time.time ()
        with self._cond_check_lock:
            oldmtime, last_check = self._conditions [key]

        if not interval or not oldmtime or now - last_check > interval:
            mtime = mtime_func (key)
            if mtime > oldmtime:
                response = func (was, key)
                with self._cond_check_lock:
                    self._conditions [key] = [mtime, now]
                if response is not None:
                    return response

            elif interval:
                with self._cond_check_lock:
                    self._conditions [key][1] = now

    def if_updated (self, key, func, interval = 1):
        def decorator(f):
            self.save_function_spec (f)
            self._conditions [key] = [0, 0]
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                response = self._check_condition (was, key, func, interval, was.getlu)
                if response is not None:
                    return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator

    def if_file_modified (self, path, func, interval = 1):
        def decorator(f):
            self.save_function_spec (f)
            self._conditions [path] = [0, 0]
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                def _getmtime (path):
                    return os.path.getmtime (path)
                response = self._check_condition (was, path, func, interval, _getmtime)
                if response is not None:
                    return response
                return f (was, *args, **kwargs)
            return wrapper
        return decorator

    # Websocket ------------------------------------------------------
    def websocket (self, spec, timeout = 60, onopen = None, onclose = None, encoding = "text"):
        use_session = False
        if spec & skitai.WS_SESSION == skitai.WS_SESSION:
            use_session = True
            assert not onopen and not onclose, 'skitai.WS_SESSION cannot have onopen or onclose handler'
        def decorator(f):
            self.save_function_spec (f)
            @wraps(f)
            def wrapper (was, *args, **kwargs):
                if not was.wshasevent ():
                    return f (was, *args, **kwargs)
                if was.wsinit ():
                    session = use_session and f (was, *args, **kwargs) or None
                    return was.wsconfig (spec, timeout, encoding, session)
                elif was.wsopened ():
                    return onopen and onopen (was) or ''
                elif was.wsclosed ():
                    return onclose and onclose (was) or ''
            return wrapper
        return decorator
    websocket_config = websocket

    def register_websocket (self, client_id, send):
        self._ws_channels [client_id] = send

    def remove_websocket (self, client_id):
        try: self._ws_channels [client_id]
        except KeyError: pass

    def websocket_send (self, client_id, msg):
        try:
            self._ws_channels [client_id] (msg)
        except KeyError:
            pass

    # Mainterinancing -------------------------------------------------------
    def maintain (self, f):
        if not self._started:
            assert f.__name__ not in self._maintern_funcs, "maintain func {} is already exists".format (f.__name__)
        self._maintern_funcs [f.__name__] = f
        return f

    # Error handling ------------------------------------------------------
    def add_error_handler (self, errcode, f, **k):
        self.handlers [errcode] = (f, k)

    def error_handler (self, errcode, **k):
        def decorator(f):
            self.add_error_handler (errcode, f, **k)
            @wraps(f)
            def wrapper (*args, **kwargs):
                return f (*args, **kwargs)
            return wrapper
        return decorator

    def default_error_handler (self, f):
        self.add_error_handler (0, f)
        return f
    defaulterrorhandler = default_error_handler
    errorhandler = error_handler
