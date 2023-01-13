#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;MVKE
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (2500)
  Send {/}ose16 {enter}
  Sleep (2500)
  Send mvke
  Send {enter}
  Sleep (2500)
  Send +{F5}
  Sleep (1000)
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
  Sleep (7000)
  Send ^+{F7}
  Sleep (4000)
  Send +{tab} {tab}
  Sleep, (2500)
  Send, C:\RA-Apps\AP-Proc\INPUTS\mvke{enter}
  Sleep, 2500
}

IfWinExist, Data Browser: Table MVKE Select Entries
{
  Sleep, (2500)
  WinClose, Data Browser: Table MVKE Select Entries
}
Return
