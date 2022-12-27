#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

;SALES TEXT
WinActivate ahk_class IEFrame
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
;Sleep (60000)
;Excel := ComObjCreate("Excel.Application")
;Excel.Visible := True
;file := "W:\ap_data\sales_text.xls"
;Excel.Workbooks.Open(file)
return