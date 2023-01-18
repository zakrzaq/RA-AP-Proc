#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

IfWinNotExist, AP MM Service Request Log.xlsm - Excel
{
  Send, #r
  Sleep (1000)
  Send, C:\Users\JZakrzewski\Rockwell Automation, Inc\EDM - AP MM Service Request Process\AP MM Service Request Log.xlsm{enter}
  Sleep (5000)
}
WinActivate, AP MM Service Request Log.xlsm - Excel
Return