param(
    [string]$Username,
    [string]$Password
)

if (-not $Username -or -not $Password) {
    Write-Host "You must supply -Username and -Password"
    exit
}

Write-Host "Starting script."

$pw = ConvertTo-SecureString $Password -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($Username, $pw)

Start-Process "powershell.exe" -Credential $cred -ArgumentList @"
    Write-Host 'Inside session: opening CMD';
    Start-Process cmd.exe;
    Start-Sleep -Seconds 2;
    shutdown.exe /l
"@

# Give time for session to open and then log off
Start-Sleep -Seconds 8