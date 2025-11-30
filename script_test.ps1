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

$token = [IntPtr]::Zero
[LogonUtil]::LogonUser($username, $domain, $password, 2, 0, [ref] $token)

Start-Process -FilePath "notepad.exe"

New-Item -Path "C:\Temp\FuzzFile50.txt" -ItemType File -Force | Out-Null

[HandleUtil]::CloseHandle($token) | Out-Null