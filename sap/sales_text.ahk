#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;SALES TEXT
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}oZ_COM_SALETXT_LD_EXT {enter}
  Sleep (1500)
  Send +{F5}
  Sleep (1500)
  Send {F8}
  Sleep (1500)
  Send {tab 5} {enter}
  Sleep (1500)
  Send +{F12}
  Sleep (1500)
  Send {F8}
  Sleep (1500)
  Send {F8}
  return
}