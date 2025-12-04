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

$nettoken = [IntPtr]::Zero

# LOGON32_LOGON_INTERACTIVE = 2
# LOGON32_PROVIDER_DEFAULT = 0
[LogonUtil]::LogonUser($username, $domain, $password, 3, 0, [ref] $nettoken)