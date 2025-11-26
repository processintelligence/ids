param(
    [string]$Domain = "TESTDOMAIN",
    [string]$User = "TestUser",
    [string]$Password = "P@ssw0rd!",
    [string]$Command = "powershell.exe"
)

$signature = @"
using System;
using System.Runtime.InteropServices;

public class LogonAPI {
    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool CreateProcessWithLogonW(
        String userName,
        String domain,
        String password,
        int logonFlags,
        String applicationName,
        String commandLine,
        int creationFlags,
        int environment,
        String currentDirectory,
        ref STARTUPINFO startupInfo,
        out PROCESS_INFORMATION processInformation);

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct STARTUPINFO {
        public int cb;
        public string lpReserved;
        public string lpDesktop;
        public string lpTitle;
        public int dwX;
        public int dwY;
        public int dwXSize;
        public int dwYSize;
        public int dwXCountChars;
        public int dwYCountChars;
        public int dwFillAttribute;
        public int dwFlags;
        public short wShowWindow;
        public short cbReserved2;
        public IntPtr lpReserved2;
        public IntPtr hStdInput;
        public IntPtr hStdOutput;
        public IntPtr hStdError;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct PROCESS_INFORMATION {
        public IntPtr hProcess;
        public IntPtr hThread;
        public int dwProcessId;
        public int dwThreadId;
    }
}
"@

Add-Type $signature

$si = New-Object LogonAPI+STARTUPINFO
$pi = New-Object LogonAPI+PROCESS_INFORMATION
$si.cb = [Runtime.InteropServices.Marshal]::SizeOf($si)

$LOGON_NETONLY = 2

$result = [LogonAPI]::CreateProcessWithLogonW(
    $User,
    $Domain,
    $Password,
    $LOGON_NETONLY,
    $null,
    $Command,
    0,
    0,
    $null,
    [ref]$si,
    [ref]$pi
)

if (-not $result) {
    throw "CreateProcessWithLogonW failed, error code: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"
} else {
    Write-Host "Launched process under /netonly credentials → 4624_9 will be logged."
}
