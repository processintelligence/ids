param(
    [string]$KeyPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    [string]$Name = "Test4657",
    [string]$Value = "cba"
)

Set-ItemProperty -Path $KeyPath -Name $Name -Value $Value
