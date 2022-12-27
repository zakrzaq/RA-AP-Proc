#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

;MARC
WinActivate ahk_class IEFrame
Send {/}ose16 {enter}
Sleep (1500)
Send marc
Send {enter}
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
Sleep (5000)
Send ^+{F7}
Sleep (3000)
Send +{tab} {tab}
Sleep (2500)
Send, C:\RA-Apps\AP-Proc\INPUTS\marc_%A_YYYY%-%A_MM%-%A_DD%_%A_HOUR%%A_MIN% {enter}
; Send, W:\ap_data\marc{enter}
Return