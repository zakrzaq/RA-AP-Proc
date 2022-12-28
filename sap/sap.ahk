#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

Send, #r
Sleep (1000)
Send, cmd /c "start msedge https://portal.ra.rockwell.com/irj/portal{enter}
Sleep (5000)
WinActivate, Welcome - SAP NetWeaver Portal - RA INT - Microsoft​ Edge
Sleep (1000)
Send {Click, 573, 250}
Sleep (1000)
Send {Click, 50, 492}
Sleep (7000)
Send, #r
Sleep (1000)
Send, C:\Users\jzakrzewski\Downloads\tx.sap{enter}
Sleep (5000)
WinActivate, SAP Easy Access
Return