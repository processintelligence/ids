param(
    [string]$VMIP,
    [string]$Username,
    [string]$Password
)
Write-Host "Attempting to trigger 4624_3"

net use "\\$VMIP\c$" /user:$Username $Password

Start-Sleep -Seconds 2

net use "\\$VMIP\c$" /delete /y