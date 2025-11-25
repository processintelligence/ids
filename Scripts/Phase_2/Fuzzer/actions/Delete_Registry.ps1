param(
    [string]$Path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    [string]$Name = "Test4657"
)

# 4657_delete (%%1906)
Remove-ItemProperty -Path $Path -Name $Name
