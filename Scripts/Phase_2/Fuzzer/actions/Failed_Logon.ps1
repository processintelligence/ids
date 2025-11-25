param(
    [string]$Username = "InvalidUser",
    [string]$WrongPassword = "WrongPassword123!"
)

$secure = ConvertTo-SecureString $WrongPassword -AsPlainText -Force

$cred = New-Object System.Management.Automation.PSCredential($Username, $secure)

Start-Process "cmd.exe" -Credential $cred -ErrorAction Stop
