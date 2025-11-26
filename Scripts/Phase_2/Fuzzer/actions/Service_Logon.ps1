param(
    [string]$ServiceName = "TempService4624",
    [string]$Executable = "C:\Windows\System32\notepad.exe"
)

$serviceAccount = "NT AUTHORITY\LocalService"

New-Service -Name $ServiceName `
            -BinaryPathName $Executable `
            -Credential $serviceAccount `
            -DisplayName "Temp Service for 4624 Type 5 Event" `
            -Description "Triggers a 4624_5 Service Logon event" `
            -StartupType Manual

Start-Service -Name $ServiceName
Start-Sleep -Seconds 2
Stop-Service -Name $ServiceName -Force

Remove-Service -Name $ServiceName -Force
