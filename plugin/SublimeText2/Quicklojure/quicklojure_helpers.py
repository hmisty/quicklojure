import re, os, socket, subprocess, thread
from functools import partial
from string import Template
import sublime
import nrepl

def commented(text):
    return "; %s\n" % "\n; ".join(text.splitlines())

def symbol_char(char):
    return re.match("[-\w*+!?/.<>]", char)

def template_string_keys(template_str):
    return [m[1] or m[2] for m
            in Template.pattern.findall(template_str)
            if m[1] or m[2]]

def from_input_panel(window, options, on_done):
    initial_text_chunks = options['initial_text']
    initial_text = "".join(initial_text_chunks) if initial_text_chunks else ""
    input_view = window.show_input_panel(options['prompt'],
                                         initial_text,
                                         on_done, None, None)

    if initial_text_chunks and len(initial_text_chunks) > 1:
        input_view.sel().clear()
        offset = 0
        for chunk in initial_text_chunks[0:-1]:
            offset += len(chunk)
            input_view.sel().add(sublime.Region(offset))

def resolve_attr(qualified_attr):
    namespace, attr_name = re.match(r"(.+)\.([^.]+)", qualified_attr).groups()
    return getattr(__import__(namespace), attr_name)

def selection(view):
    sel = view.sel()
    
    if sel[0].empty(): #try line instead
        sel = view.lines(view.sel()[0])


    if len(sel) == 1 and not sel[0].empty():
        return view.substr(sel[0]).strip()
    else:
        raise UserWarning("There must be one selection / line to evaluate")

def current_line(view):
    sel = view.lines(view.sel()[0])
    if len(sel) == 1 and not sel[0].empty():
        return view.substr(sel[0]).strip()
    else:
        raise UserWarning("There must be one line to evaluate")

def symbol_under_cursor(view):
    begin = end = view.sel()[0].begin()
    while symbol_char(view.substr(begin - 1)): begin -= 1
    while symbol_char(view.substr(end)): end += 1
    if begin == end:
        raise UserWarning("No symbol found under cursor")
    else:
        return view.substr(sublime.Region(begin, end))

def get_repl_view(window):
    try:
        return (v for v
                in window.views()
                if v.settings().get('nrepl_port')).next()
    except StopIteration:
        return None

def append_to_view(v, text):
    return insert_into_view(v, v.size(), text)

def insert_into_view(v, start, text):
    v.set_read_only(False)
    edit = v.begin_edit()
    end = start + v.insert(edit, start, text)
    v.end_edit(edit)
    v.set_read_only(True)
    return sublime.Region(start, end)

def append_to_region(v, region_name, text):
    regions = v.get_regions(region_name)
    start = regions[-1].end()
    region = insert_into_view(v, start, text)
    regions.append(region)
    v.add_regions(region_name, regions, '')


class nrepl_handler(object):
    def __init__(self, args, window, repl_view):
        self.args = args
        self.window = window
        self.repl_view = repl_view
        for callback in ('on_sent', 'on_out', 'on_err', 'on_value',
                         'on_status', 'on_done'):
            unwrapped = "_%s" % callback
            if hasattr(self, unwrapped):
                setattr(self, callback, self._wrapped_callback(unwrapped))

    def on_sent(self, req):
        self.req = req

    def _wrapped_callback(self, method_name):
        method = getattr(self, method_name)
        return lambda m: sublime.set_timeout(partial(method, m), 0)
