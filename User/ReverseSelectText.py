import sublime, sublime_plugin

class ReverseSelectTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        for s in view.sel():
            view.replace(edit, s, view.substr(s)[::-1])
