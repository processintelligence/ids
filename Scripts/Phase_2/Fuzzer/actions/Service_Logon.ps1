param(
    [string]$ServiceName = "TempService4624",
    [string]$Executable = "C:\Windows\System32\notepad.exe",
    [string]$Username,
    [string]$Password
)

if (-not $Username -or -not $Password) {
    Write-Host "You must supply -Username and -Password"
    exit
}

$SecurePass = ConvertTo-SecureString $Password -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential($Username, $SecurePass)

New-Service -Name $ServiceName `
            -BinaryPathName $Executable `
            -Credential $Cred `
            -DisplayName "Temp Service for 4624 Type 5 Event" `
            -Description "Triggers a 4624_5 Service Logon event" `
            -StartupType Manual

Start-Service -Name $ServiceName

Start-Sleep -Seconds 2

Stop-Service -Name $ServiceName -Force

Remove-Service -Name $ServiceName -Force
