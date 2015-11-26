import sublime, sublime_plugin


import vamcodelib


class VamcodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        items = self.get_items()
        idx = self.view.show_popup_menu(items, None)
        if idx >= 0:
            self.view.insert(edit, self.view.sel()[0].begin(), self.get_symbol(items[idx]))

    def get_symbol(self, item):
        return item.split('-')[0]

    def get_items(self):
        items = []
        for k, v in vamcodelib.CODE_MAP:
            items.append("{} -> {}".format(v, k))
        return items


class VamcodeCompileCommand(sublime_plugin.WindowCommand):
    def run(self):
        compiler = Compiler(self.window.active_view().file_name())
        compiler.run(silent=True)
        view = self.window.open_file(compiler.output_filename)


class VamcodeDecompileCommand(sublime_plugin.WindowCommand):
    def run(self):
        decompiler = Decompiler(self.window.active_view().file_name())
        decompiler.run()
        view = self.window.open_file(decompiler.output_filename)
