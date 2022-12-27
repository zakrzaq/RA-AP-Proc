#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
;SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

;MVKE
WinActivate ahk_class IEFrame
Send {/}ose16 {enter}
Sleep (1500)
Send mvke
Send {enter}
Sleep (1500)
Send +{F5}
Sleep (1000)
Send {F8}
Sleep (2500)
Send {TAB 2}
Send {enter}
Sleep (1500)
Send +{F12}
Sleep (1500)
Send {F8}
Sleep (1500)
Send {F8}
Sleep (7000)
Send ^+{F7}
Sleep (4000)
Send +{tab} {tab}
Send, C:\RA-Apps\AP-Proc\INPUTS\mvke_%A_YYYY%-%A_MM%-%A_DD%_%A_HOUR%%A_MIN% {enter}
; Send, W:\ap_data\mvke{enter}
Return