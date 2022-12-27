#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

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
  Send, C:\RA-Apps\AP-Proc\INPUTS\mlan{enter}
  Sleep (2000)
  WinClose, Data Browser: Table MLAN
  Sleep, (1000)
  WinClose, mlan.XLSX - Excel
  Sleep, (1000)
  Return
}