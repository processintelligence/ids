param(
    [string]$Path = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
    [string]$Name = "Personal",
    [string]$Value = "%SystemDrive%\NewDocs"
)

Set-ItemProperty -Path $Path -Name $Name -Value $Value
