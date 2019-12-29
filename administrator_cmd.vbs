cwd = CreateObject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
path = cwd & "\cmd_command.bat"

Set shell = CreateObject("Shell.Application")
shell.ShellExecute path,"","","runas",0

WScript.Quit