import re, os, socket, subprocess, thread
from functools import partial
from string import Template
import sublime, sublime_plugin
import nrepl
from quicklojure_helpers import get_repl_view, template_string_keys, from_input_panel, resolve_attr, append_to_view, selection, symbol_under_cursor, current_line

# *.sublime-keymap: clojure_eval
class ClojureEval(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return bool(get_repl_view(self.window))

    def run(self, expr = None, input_panel = None, **kwargs):
        on_done = partial(self._handle_input, expr, **kwargs)
        if 'from_input_panel' in template_string_keys(expr):
            from_input_panel(self.window, input_panel, on_done)
        else:
            on_done(None)

    def _handle_input(self, expr, from_input_panel,
                      handler="quicklojure_handlers.OutputToRepl", handler_args={}):
        repl_view = get_repl_view(self.window)
        expr = Template(expr).safe_substitute(from_input_panel=from_input_panel)

        port = int(repl_view.settings().get('nrepl_port'))
        client = nrepl.NreplClient('localhost', port)
        handler_class = resolve_attr(handler)
        handler_obj = handler_class(args=handler_args,
                                    window=self.window,
                                    repl_view=repl_view)
        thread.start_new_thread(client.eval, (expr, handler_obj))

# *.sublime-keymap: clojure_eval_from_view
class ClojureEvalFromView(sublime_plugin.TextCommand):
    def is_enabled(self):
        return bool(get_repl_view(self.view.window()))

    def run(self, edit, expr, in_ns=True, **kwargs):
        input_keys = template_string_keys(expr)
        input_mapping = {}

        try:
            for key in ['selection', 'symbol_under_cursor', 'current_line']:
                if key in input_keys:
                    input_mapping[key] = globals()[key](self.view)
        except UserWarning as warning:
            sublime.status_message(str(warning))
            return

        expr = Template(expr).safe_substitute(input_mapping)

        """
    file_name = self.view.file_name()
        if in_ns and file_name:
            #TODO use ns form in file
            _, after_src = file_name.rsplit("/src/", 1)
            file_ns = re.sub(r"\.clj$", "", re.sub("/", ".", after_src))
            #TODO prompt to save the file first
            expr = ("(do (load-file \"%s\") (in-ns '%s) %s)"
                    % (file_name, file_ns, expr))
    """

        kwargs.update(expr = expr)
        self.view.window().run_command('clojure_eval', kwargs)

# *.sublime-keymap: clojure_macroexpand
class ClojureMacroexpand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('clojure_eval_from_view',
                              {'expr': "(macroexpand '${selection})"})

# *.sublime-keymap: clojure_view_doc
class ClojureViewDoc(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('clojure_eval_from_view',
            {"expr": "(use 'clojure.repl)(clojure.repl/doc ${symbol_under_cursor})",
             #"handler": "quicklojure_handlers.OutputToRepl"})
             #EVAN
             "handler": "quicklojure_handlers.OutputToPanel"})

# *.sublime-keymap: clojure_view_source
class ClojureViewSource(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('clojure_eval_from_view',
            {"expr": "(use 'clojure.repl)(clojure.repl/source ${symbol_under_cursor})",
             "handler": "quicklojure_handlers.OutputToView"})

# *.sublime-commands: clojure_start_repl
class ClojureStartRepl(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return not get_repl_view(self.window)

    def run(self):
        cwd = self.window.folders()[0]

        repl_view = self.window.new_file()

        repl_view.set_name("nREPL launching...")
        repl_view.set_scratch(True)
        repl_view.set_read_only(True)

        repl_view.settings().set('nrepl_port', 7999) #FIXME default or find an used one?
        repl_view.settings().set('nrepl_cwd', cwd)
        repl_view.settings().set('line_numbers', False)
        repl_view.set_syntax_file('Packages/Clojure/Clojure.tmLanguage')

        append_to_view(repl_view,
                       ("; running `clj --nrepl-headless`%s...\n"
                        % ("in " + cwd if cwd else "")))
        thread.start_new_thread(self._start_server, (repl_view, cwd))

    def _project_path(self):
        folders = self.window.folders()
        for folder in folders:
            path = project_path(folder)
            if path: return path

        active_view = self.window.active_view()
        if active_view:
            file_name = active_view.file_name()
            if file_name:
                dir_name = os.path.dirname(file_name)
                return project_path(dir_name) or dir_name

        return None

    def _start_server(self, repl_view, cwd):
        port = 7999 #cannot use repl_view.settings().get(...)
        proc = subprocess.Popen(["clj", "--nrepl-headless", str(port)])
        sublime.set_timeout(partial(self._on_connected, repl_view, port), 0)

    def _on_connected(self, repl_view, port):
        repl_view.set_name("nREPL connected")
        repl_view.settings().set('nrepl_port', port)
        append_to_view(repl_view,
            (("; nREPL server started on port %d\n" +
              "; closing all REPL views using this port will kill the server\n")
             % port))
        repl_view.window().run_command('clojure_eval', {'expr': '(str "These ones go up to " (inc 10))'})

