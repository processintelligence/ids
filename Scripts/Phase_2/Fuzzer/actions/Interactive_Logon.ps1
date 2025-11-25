param(
    [string]$Username,
    [string]$Password
)

if (-not $Username -or -not $Password) {
    Write-Host "You must supply -Username and -Password"
    exit
}

$secure = ConvertTo-SecureString $Password -AsPlainText -Force

$cred = New-Object System.Management.Automation.PSCredential($Username, $secure)

Start-Process "powershell.exe" -Credential $cred -ArgumentList "-NoExit"
