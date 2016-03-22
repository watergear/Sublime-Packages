import sublime, sublime_plugin

from collections import deque
def reverse(iterable):
    d = deque()
    d.extendleft(iterable)
    return ''.join(d)

class ReverseSelectTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        for s in view.sel():
            text = reverse(view.substr(s))
            view.replace(edit, s, text)
