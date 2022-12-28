#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

IfWinExist, Data Browser: Table AUSP
{
  MsgBox "Hi"
  ; WinClose, Data Browser: Table AUSP
}