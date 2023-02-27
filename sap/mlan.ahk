#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

table := "MLAN"
path := "C:\RA-Apps\AP-Proc\INPUTS\"
out_file := % path table

IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}ose16 {enter}
  WinWaitActive, Data Browser: Initial Screen
  Sleep (1000)
  Send %table%
  Send {enter}
  WinWaitActive, Data Browser: Table %table%: Selection Screen
  Sleep (1000)
  ; select variant
  Send +{F5}
  Sleep (1000)
  Send {down}
  Sleep (1000)
  Send {up}
  Sleep (1000)
  Send {F2}
  Sleep (1000)
  ; paste parts from clipoard
  Send {TAB 2}
  Send {enter}
  WinWaitActive, Multiple Selection for MATNR
  Sleep (1000)
  Send +{F12}
  Sleep (2500)
  Send {F8}
  Sleep (2500)
  ; execute
  Send {F8}
  WinWaitActive, Data Browser: Table %table% Select Entries
  Sleep (1500)
  ; save
  Send ^+{F7}
  Sleep (2500)
  WinWaitActive, Save As
  Sleep (2500)
  Send +{tab} {tab}
  Sleep (2500)
  Send, %out_file%{enter}
  Sleep, 2500
  ; close window
  IfWinExist, Data Browser: Table %table% Select Entries
  {
    Sleep, (2500)
    WinClose, Data Browser: Table %table% Select Entries
  }
}

Return