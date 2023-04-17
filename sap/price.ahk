#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

table := "PRICE"
path := "C:\RA-Apps\AP-Proc\INPUTS\"
out_file := % path table

;LIST PRICE
IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}osqvi {enter}
  WinWaitActive, QuickViewer: Initial Screen
  Sleep (1000)
  ; select variant
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
  ; paste parts from cliboard
  Send {TAB 2}
  Send {enter}
  WinWaitActive, Multiple Selection for MATNR
  Sleep (1500)
  Send +{F12}
  Sleep (2500)
  Send {F8}
  Sleep (2500)
  ; esecute
  Send {F8}
  WinWaitActive, AP_LIST_PRICE
  Sleep (2000)
  ; save
  ; Send +{F10}
  Send {AppsKey}
  Sleep (1500)
  Send {up} {enter}
  Sleep (1500)
  Send {enter}
  Sleep (4000)
  Send +{tab}
  Sleep (1000)
  Send {tab}
  Sleep (2000)
  Send, %out_file%{enter}
}

IfWinExist, AP_LIST_PRICE
{
  Sleep, (2500)
  WinClose, AP_LIST_PRICE
  WinClose, Material Sales Text Load/Extract
  WinClose, ausp.XLSX - Excel
  WinClose, mara.XLSX - Excel
  WinClose, marc.XLSX - Excel
  WinClose, mlan.XLSX - Excel
  WinClose, mvke.XLSX - Excel
  WinClose, gts.XLSX - Excel
  WinClose, price.XLSX - Excel
}
Return
