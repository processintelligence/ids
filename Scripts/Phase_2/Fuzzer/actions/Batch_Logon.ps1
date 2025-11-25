param(
    [string]$TaskName = "CMD Task"
)

Start-ScheduledTask -TaskName $TaskName
