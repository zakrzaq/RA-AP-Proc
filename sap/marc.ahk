#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;MARC
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}ose16 {enter}
  Sleep (1500)
  Send marc
  Send {enter}
  Sleep (1500)
  Send +{F5}
  Sleep (1500)
  Send {F8}
  Sleep (1500)
  Send {TAB 2}
  Send {enter}
  Sleep (1500)
  Send +{F12}
  Sleep (1500)
  Send {F8}
  Sleep (1500)
  Send {F8}
  Sleep (5000)
  Send ^+{F7}
  Sleep (3000)
  Send +{tab} {tab}
  Sleep (2500)
  Send, C:\RA-Apps\AP-Proc\INPUTS\marc{enter}
  Sleep (2000)
  WinClose, Data Browser: Table MARC
  Sleep, (1000)
  WinClose, marc.XLSX - Excel
  Sleep, (1000)
  Return
}