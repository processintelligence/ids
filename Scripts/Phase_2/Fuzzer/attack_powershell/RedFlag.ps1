$Path = "C:\Temp\FuzzStarter.txt"

"START" | Out-File -FilePath $Path -Force -Encoding ascii

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

Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "Common" -Value "abc"

[HandleUtil]::CloseHandle($intertoken) | Out-Null

$Path = "C:\Temp\FuzzEnder.txt"

"END" | Out-File -FilePath $Path -Force -Encoding ascii