param(
    [string]$Path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    [string]$Name = "Test4657"
)

Remove-ItemProperty -Path $Path -Name $Name
