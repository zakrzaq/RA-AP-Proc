#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

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
  Sleep (4000)
  Send +{tab}
  Sleep (1000)
  Send {tab}
  Sleep (2000)
  Send, C:\RA-Apps\AP-Proc\INPUTS\price{enter}
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