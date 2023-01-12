#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;MARC
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (2500)
  Send {/}ose16 {enter}
  Sleep (2500)
  Send marc
  Send {enter}
  Sleep (2500)
  Send +{F5}
  Sleep (2500)
  Send {F8}
  Sleep (2500)
  Send {TAB 2}
  Send {enter}
  Sleep (2500)
  Send +{F12}
  Sleep (2500)
  Send {F8}
  Sleep (2500)
  Send {F8}
  Sleep (5000)
  Send ^+{F7}
  Sleep (3000)
  Send +{tab} {tab}
  Sleep (2500)
  Send, C:\RA-Apps\AP-Proc\INPUTS\marc{enter}
}

IfWinExist, Data Browser: Table MARC Select Entries
{
  Sleep, (2500)
  WinClose, Data Browser: Table MARC Select Entries
}
Return