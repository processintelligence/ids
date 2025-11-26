param(
    [string]$Path = "C:\Temp\FuzzFile.txt"
)

#create or overwrite, does not log if the file does already exist
New-Item -Path $Path -ItemType File -Force | Out-Null
