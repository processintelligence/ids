param(
    [string]$Path = "C:\Temp\FuzzFile.txt"
)

# Deletes the file
Remove-Item -Path $Path -Force
