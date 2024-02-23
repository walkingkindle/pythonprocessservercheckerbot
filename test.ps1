Start-Sleep -Seconds 2.5
Get-Process -Name "wscript" | Stop-Process -Force
Start-Sleep -Seconds 2.5