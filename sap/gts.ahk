#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

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
  WinClose ahk_class SAP_FRONTEND_SESSION
  Sleep, (1000)
  WinClose, Export / Import Classification Report
  Sleep, (1000)
  Return
}
