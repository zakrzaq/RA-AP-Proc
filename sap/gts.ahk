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
  WinWaitActive, Export / Import Classification Report
  Sleep (1000)
  ; select cariant
  Send +{F5}
  Sleep (1500)
  Send {F8}
  Sleep (1500)
  ; paste parts from clipboard
  Send {TAB 2}
  Send {enter}
  Sleep (1500)
  Send +{F12}
  Sleep (1500)
  Send {F8}
  Sleep (1500)
  ; execute
  Send {F8}
  WinWaitActive, Export / Import Classification Report
  Sleep (1000)
  ; save
  Send ^{F2}
  Sleep (4000)
  Send +{tab} {tab}
  Sleep (3000)
  Send, %out_file%{enter}
  Sleep (3000)
  WinClose, Export / Import Classification Report
  Return
}
