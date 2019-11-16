import sublime, sublime_plugin, os

_actionGlobal     = None
_controllerGlobal = None

class ViewToControllerCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    global _actionGlobal
    global _controllerGlobal

    file_name         = self.view.file_name()
    source_path       = os.path.dirname(file_name)
    _controllerGlobal = source_path.replace('views', 'controllers') + '_controller.rb'

    self.detect_action_name(file_name, source_path)

    if os.path.isfile(_controllerGlobal):
      sublime.active_window().open_file(_controllerGlobal)

  def detect_action_name(self, file_name, source_path):
    global _actionGlobal

    action_file   = file_name.split(source_path + '/')[1]
    _actionGlobal = 'def ' + action_file.split('.')[0]

class LoadListener(sublime_plugin.ViewEventListener):

  def on_activated(self):
    global _actionGlobal
    global _controllerGlobal

    if _controllerGlobal == self.view.file_name():
      action_def   = self.view.find(_actionGlobal, 0)
      line, column = self.view.rowcol(action_def.begin())
      self.view.run_command("goto_line", {"line": line + 2} )