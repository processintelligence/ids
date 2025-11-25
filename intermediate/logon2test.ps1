# ---- Replace these values ----
$username = "testuser"     # <--- your username
$password = "P@ssw0rd!"    # <--- your password
$domain   = "."            # <--- "." means local machine
# ------------------------------

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

# LOGON32_LOGON_INTERACTIVE = 2
# LOGON32_PROVIDER_DEFAULT = 0
$ok = [LogonUtil]::LogonUser($username, $domain, $password, 2, 0, [ref] $token)

if ($ok) {
    Write-Host "Logon successful. Token: $token"
    # This action causes Security Event 4624 (Logon Type 2)
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($token)
} else {
    $err = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
    Write-Host "Logon FAILED. Win32 error: $err"
}
