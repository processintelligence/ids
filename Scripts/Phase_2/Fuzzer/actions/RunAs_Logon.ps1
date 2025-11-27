param(
    [string]$Domain,
    [string]$User,
    [string]$Executable = "powershell.exe"
)

$FullUser = "$Domain\$User"

$RunAsCmd = "runas.exe /netonly /user:$FullUser `"$Executable`""

cmd.exe /c $RunAsCmd
