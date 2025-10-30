$inputFile = "C:\Users\lomo0\Downloads\wls_day-01"
$outputFile = "C:\Users\lomo0\Downloads\wls_trimmed"
$sizeToKeep = 200MB
$bufferSize = 1MB

$in = [System.IO.File]::OpenRead($inputFile)
$out = [System.IO.File]::Create($outputFile)

$remaining = $sizeToKeep
$buffer = New-Object byte[] $bufferSize

while ($remaining -gt 0) {
    $readSize = [Math]::Min($bufferSize, $remaining)
    $bytesRead = $in.Read($buffer, 0, $readSize)
    if ($bytesRead -le 0) { break }
    $out.Write($buffer, 0, $bytesRead)
    $remaining -= $bytesRead
}

$in.Close()
$out.Close()
