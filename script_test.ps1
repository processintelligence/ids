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
"@

$token = [IntPtr]::Zero
[LogonUtil]::LogonUser($username, $domain, $password, 2, 0, [ref] $token) | Out-Null

Start-Process -FilePath "notepad.exe"

New-Item -Path "C:\Temp\FuzzFile84.txt" -ItemType File -Force | Out-Null

[System.Runtime.InteropServices.Marshal]::FreeHGlobal($token)