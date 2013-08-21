import sublime, sublime_plugin
import nrepl
from quicklojure_helpers import commented, append_to_region, append_to_view, nrepl_handler

class OutputToRepl(nrepl_handler):
    def _on_sent(self, req):
        region = append_to_view(self.repl_view, "\n\n%s\n" % req['code'])
        self.repl_view.add_regions(req['id'], [region], '')

    def _on_out(self, resp):
        append_to_region(self.repl_view, resp['id'], commented(resp['out']))

    def _on_err(self, resp):
        append_to_region(self.repl_view, resp['id'], commented(resp['err']))

    def _on_value(self, resp):
        append_to_region(self.repl_view, resp['id'], "%s\n" % resp['value'])
        self.repl_view.set_name("(in-ns '" + resp['ns'] + ")")

    def _on_status(self, resp):
        if 'done' in resp['status']:
            repl_view_group, _ = self.window.get_view_index(self.repl_view)
            if repl_view_group == -1: return

            active_view = self.window.active_view()
            active_group = self.window.active_group()
            self.window.focus_view(self.repl_view)
            if repl_view_group != active_group:
                # give focus back to the originally active view if it's in a
                # different group
                self.window.focus_view(active_view)
            self.repl_view.show(self.repl_view.get_regions(resp['id'])[0])

        # bookmark_point = sublime.Region(self.view.size())

        # view.sel().clear()
        # view.sel().add(bookmark_point)
        # bookmarks = view.get_regions('bookmarks')
        # bookmarks.append(bookmark_point)
        # view.add_regions('bookmarks', bookmarks, 'bookmarks', 'bookmark',
        #                  sublime.HIDDEN | sublime.PERSISTENT)


class OutputToPanel(nrepl_handler):
    def _on_done(self, resp):
        print "ClojureOutputToPanel resp\n", repr(resp)
        if resp.has_key('out'):
            panel = self.window.get_output_panel('eleven')
            append_to_view(panel, resp['out'])
            self.window.run_command("show_panel", {"panel": "output.eleven"})
        else:
            sublime.status_message("No output for `%s`" % self.req['code'])

class OutputToView(nrepl_handler):
    def __init__(self, **kwargs):
        nrepl_handler.__init__(self, **kwargs)
        if not self.args.has_key('syntax_file'):
            self.args['syntax_file'] = 'Packages/Clojure/Clojure.tmLanguage'

    def _on_done(self, resp):
        print "ClojureOutputToView resp\n", repr(resp)
        view = self.window.new_file()
        view.set_scratch(True)
        view.set_read_only(True)
        view.set_name(self.req['code'])
        if self.args.has_key('syntax_file'):
            view.set_syntax_file(self.args['syntax_file'])
        append_to_view(view, resp['out'])
        view.sel().clear()
        view.sel().add(sublime.Region(0))
        view.show(0)

# event listener
class NreplManager(sublime_plugin.EventListener):
    #TODO show nREPL status in status bar

    def on_close(self, view):
        port = view.settings().get('nrepl_port')
        if port:
            # If there are any other views using that server, don't kill it.
            for w in sublime.windows():
                for v in w.views():
                    if v.settings().get('nrepl_port') == port and v.id() != view.id():
                        return

            client = nrepl.NreplClient('localhost', port)
            thread.start_new_thread(client.kill_server, ())

    def on_load(self, view):
        port = view.settings().get('nrepl_port')
        if port:
            # We're loading a REPL window that existed from a hot exit.  Check
            # if nREPL is still running on that port.
            try:
                nrepl.NreplClient('localhost', port)
                print "nREPL on port %d is running" % port
            except:
                view.settings().set('nrepl_port', None)
                append_to_view(view, ("\n\n" +
                                      ";;;;;;;;;;;;;;;;\n" +
                                      "; DISCONNECTED ;\n" +
                                      ";;;;;;;;;;;;;;;;"))

