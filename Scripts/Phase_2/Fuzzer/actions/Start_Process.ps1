param(
    [string]$ExePath,
    [string[]]$Arguments = @()
)

Start-Process -FilePath $ExePath -ArgumentList $Arguments
