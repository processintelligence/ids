param(
    [string]$ServiceName = "TempService4624",
    [string]$Executable = "C:\Windows\System32\notepad.exe"
)

# Create service using LocalService account
sc.exe create $ServiceName binPath= "\"$Executable\"" obj= "NT AUTHORITY\LocalService" type= own

# Start service → triggers 4624 Type 5
Start-Service $ServiceName
Start-Sleep -Seconds 2

# Stop service → triggers 4634 Type 5
Stop-Service $ServiceName -Force

# Remove service
sc.exe delete $ServiceName
