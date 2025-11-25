param(
    [string]$Path = "C:\Temp\FuzzFile.txt"
)

# Creates the file (overwrites if exists)
New-Item -Path $Path -ItemType File -Force | Out-Null
