param(
    [string]$Path = "C:\Temp\FuzzFile.txt"
)

Add-Content -Path $Path -Value "Modified at $(Get-Date)"
