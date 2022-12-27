#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

;LIST PRICE
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}osqvi {enter}
  Sleep (7000)
  Send LIST_PRICE {F8}
  Sleep (1000)
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
  Sleep (10000)
  Send +{F10}
  Sleep (1500)
  Send {up} {enter}
  Sleep (1500)
  Send {enter}
  Sleep (2000)
  Send +{tab}
  Send {tab}
  Sleep (3000)
  Send, C:\RA-Apps\AP-Proc\INPUTS\price{enter}
  Sleep (2000)
  WinClose, AP_LIST_PRICE
  Sleep, (1000)
  WinClose, price.XLSX - Excel
  Sleep, (1000)
  WinClose, Material Sales Text Load/Extract
  Sleep, (1000)
  Return
}