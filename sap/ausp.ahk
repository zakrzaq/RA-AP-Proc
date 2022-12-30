#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;AUSP
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}ose16 {enter}
  Sleep (1500)
  Send ausp
  Send {enter}
  Sleep (1500)
  Send +{F5}
  Sleep (1000)
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
  Sleep (17000)
  Send ^+{F7}
  Sleep (20000)
  Send +{tab} {tab}
  Sleep, 500
  Send, C:\RA-Apps\AP-Proc\INPUTS\ausp{enter}
  Sleep (4000)
  IfWinExist, Data Browser: Table AUSP Select Entries
  {
    Sleep, (1500)
    WinClose, Data Browser: Table AUSP Select Entries
  }
}
Return