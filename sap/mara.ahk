#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;MARA
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}oih09 {enter}
  Sleep (2500)
  Send {TAB 2}
  Send {enter}
  Sleep (1500)
  Send +{F12}
  Sleep (1500)
  Send {F8}
  Sleep (1500)
  Send {F8}
  Sleep (5000)
  Send +{F10}
  Sleep (1500)
  Send {up} {enter}
  Sleep (1500)
  Send {enter}
  Sleep (3000)
  Send +{tab} {tab}
  Send, C:\RA-Apps\AP-Proc\INPUTS\mara{enter}
  Sleep (2000)
  WinClose, Display Material: Material List
  Sleep, (1000)
  WinClose, mara.XLSX - Excel
  Sleep, (1000)
  Return
}