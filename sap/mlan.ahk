#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;MLAN
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}ose16 {enter}
  Sleep (1500)
  Send mlan {enter}
  Sleep (1500)
  Send +{F5}
  Sleep (1500)
  Send {down}
  Sleep (1500)
  Send {up}
  Sleep (1500)
  Send {F2}
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
  Sleep, 500
  Send, C:\RA-Apps\AP-Proc\INPUTS\mlan{enter}
}

IfWinExist, Data Browser: Table MLAN Select Entries
{
  Sleep, (2500)
  WinClose, Data Browser: Table MLAN Select Entries
}
Return