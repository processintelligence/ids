$Path = "C:\Temp\FuzzStarter.txt"

"START" | Out-File -FilePath $Path -Force -Encoding ascii

$secure = ConvertTo-SecureString "WrongPassword123" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("InvalidUser", $secure)
try {
    Start-Process "cmd.exe" -Credential $cred -ErrorAction Stop
}
catch {
}
$secure = ConvertTo-SecureString "WrongPassword123" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("InvalidUser", $secure)
try {
    Start-Process "cmd.exe" -Credential $cred -ErrorAction Stop
}
catch {
}
$secure = ConvertTo-SecureString "WrongPassword123" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("InvalidUser", $secure)
try {
    Start-Process "cmd.exe" -Credential $cred -ErrorAction Stop
}
catch {
}
$secure = ConvertTo-SecureString "WrongPassword123" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("InvalidUser", $secure)
try {
    Start-Process "cmd.exe" -Credential $cred -ErrorAction Stop
}
catch {
}
$secure = ConvertTo-SecureString "WrongPassword123" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("InvalidUser", $secure)
try {
    Start-Process "cmd.exe" -Credential $cred -ErrorAction Stop
}
catch {
}


$username = "Thesis"
$domain = "."
$password = "Master123"

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class LogonUtil {
    [DllImport("advapi32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
    public static extern bool LogonUser(
        string lpszUsername,
        string lpszDomain,
        string lpszPassword,
        int dwLogonType,
        int dwLogonProvider,
        out IntPtr phToken);
}

public class HandleUtil {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool CloseHandle(IntPtr hObject);
}
"@

$intertoken = [IntPtr]::Zero
[LogonUtil]::LogonUser($username, $domain, $password, 2, 0, [ref] $intertoken)


[HandleUtil]::CloseHandle($intertoken) | Out-Null

$Path = "C:\Temp\FuzzEnder.txt"

"END" | Out-File -FilePath $Path -Force -Encoding ascii