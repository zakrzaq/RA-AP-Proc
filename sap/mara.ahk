#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

;MARA
WinActivate ahk_class SAP_FRONTEND_SESSION
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
Send, C:\RA-Apps\AP-Proc\INPUTS\mara_%A_YYYY%-%A_MM%-%A_DD%_%A_HOUR%%A_MIN% {enter}
; Send, W:\ap_data\mara{enter}
;Sleep (5000)
;Send ^A
;Sleep (1000)
;Send ^C
;Sleep (1000)
;WinActivate AP MM Service Request Log.xlsm - Excel
;Sleep (1500)
Return