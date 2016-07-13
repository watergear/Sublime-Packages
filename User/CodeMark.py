import datetime
import re
import sublime, sublime_plugin

Author = "Sim"
DateTime = "DataTime"
CodeMarkContents = "CodeMark"
EndLine = '\n'

class CodeMarkCommand(sublime_plugin.TextCommand):
    def add_code_mark(self, edit, modifycode=False):
        CodeMarkBegin = ' '.join(["///---"+Author, DateTime, CodeMarkContents])
        CodeMarkEnd = ' '.join(["///---END", CodeMarkContents])
        view = self.view
        for s in view.sel():
            text = view.substr(s);
            mm = re.search(r'^(\s*)\S', text)
            prefix = mm.group(1) if mm else ''
            if s.empty():
                view.insert(edit, s.begin(), prefix + CodeMarkBegin)
            else:
                view.insert(edit, s.end(), prefix + CodeMarkEnd + EndLine)

                if modifycode:
                    lastline = True
                    for textline in reversed(text.split('\n')):
                        if not textline and lastline:
                            lastline = False
                            continue
                        lastline = False
                        mmline = re.search(r'^(\s*)(.*)', textline)
                        textlinedup = mmline.group(1) + '//' + mmline.group(2) if mmline else '//' + textline
                        view.insert(edit, s.begin(), textlinedup + EndLine)

                view.insert(edit, s.begin(), prefix + CodeMarkBegin + EndLine)

    def run(self, edit):
        return self.add_code_mark(edit)

class CodeMarkModifyCommand(CodeMarkCommand):
    def run(self, edit):
        return self.add_code_mark(edit, modifycode=True)

class CodeMarkSetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        for s in view.sel():
            if s.empty():
                s = view.word(s)
            text = view.substr(s)
            mm = re.search(r'^(\d{4}-\d{2}-\d{2}) (.+)', text)
            global CodeMarkContents
            global DateTime
            if mm:
                DateTime = mm.group(1)
                CodeMarkContents = mm.group(2)
            else:
                DateTime = datetime.date.today().strftime("%Y-%m-%d")
                CodeMarkContents = text

