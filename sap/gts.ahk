#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;GST
IfWinExist, SAP Easy Access
{
  WinActivate ahk_class SAP_FRONTEND_SESSION
  Sleep (1500)
  Send {/}oZ_SLO_EXPIMP_CLSSFCT {enter}
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
  Sleep (6000)
  Send ^{F2}
  Sleep (3000)
  Send +{tab} {tab}
  Sleep (2000)
  Send, C:\RA-Apps\AP-Proc\INPUTS\gts{enter}
  Sleep (2000)
  WinClose, Export / Import Classification Report
  Return
}
