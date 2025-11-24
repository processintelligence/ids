param(
    [int]$Iterations = 10,
    [string]$Username,
    [string]$Password
)

if (-not $Username -or -not $Password) {
    Write-Host "You must supply -Username and -Password"
    exit
}
Write-Host "Attempting to trigger 4624_2"


for ($i = 1; $i -le $Iterations; $i++) {

    Write-Host "---- Iteration $i ----"

    $pw = ConvertTo-SecureString $Password -AsPlainText -Force
    $cred = New-Object System.Management.Automation.PSCredential($Username, $pw)

    Start-Process "powershell.exe" -Credential $cred -ArgumentList @"
        Write-Host 'Inside session: opening CMD';
        Start-Process cmd.exe;
        Start-Sleep -Seconds 2;
        shutdown.exe /l
"@

    Start-Sleep -Seconds 8
}
