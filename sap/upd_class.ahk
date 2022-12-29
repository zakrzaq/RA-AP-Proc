#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

IfWinExist, SAP Easy Access
{
  WinActivate, SAP Easy Access
  Sleep (1500)
  Send {/}oZ_PPI_MNT_CLASS_CHAR {enter}
  Sleep (2000)
  Send +{F5}
  Sleep, 1000
  Send {F8}
  Sleep (1000)
  Send {F8}
}
Return