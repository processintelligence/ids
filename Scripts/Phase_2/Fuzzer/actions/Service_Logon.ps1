param(
    [string]$ServiceName = "TempService4624",
    [string]$Executable = "C:\Windows\System32\notepad.exe"
)

# Create service using LocalService account
sc.exe create $ServiceName binPath= "\"$Executable\"" obj= "NT AUTHORITY\LocalService" type= own

Start-Service $ServiceName
Start-Sleep -Seconds 2

Stop-Service $ServiceName -Force

sc.exe delete $ServiceName
