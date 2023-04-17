#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

table := "MARA"
path := "C:\RA-Apps\AP-Proc\INPUTS\"
out_file := % path table

;MARA
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}oih09 {enter}
  WinWaitActive, Display Material: Material Selection
  Sleep (1000)
  Send {TAB 2}
  Send {enter}
  WinWaitActive, Multiple Selection for Material
  Sleep (1000)
  ; paste parts from clipboard
  Send +{F12}
  Sleep (3000)
  Send {F8}
  Sleep (2500)
  ; execute
  Send {F8}
  WinWaitActive, Display Material: Material List
  Sleep (1000)
  ; save
  Send +{F10}
  Sleep (2500)
  Send {up} {enter}
  Sleep (2500)
  Send {enter}
  Sleep (3000)
  Send +{tab} {tab}
  Sleep (1500)
  Send, %out_file%{enter}
  Sleep (2500)
}

IfWinExist, Display Material: Material List
{
  Sleep, (2500)
  WinClose, Display Material: Material List
}
Return
