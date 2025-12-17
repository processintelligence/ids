$r = [System.Net.WebRequest]::Create("http://localhost/")
$r.Credentials = New-Object System.Net.NetworkCredential($User, $Password, ".");
try { $r.GetResponse() } catch {}


# Logoff
[System.Net.ServicePointManager]::CloseConnectionGroups("")


#alt logoff
#$r = $null
#[GC]::Collect()
#Start-Sleep -Milliseconds 200    # Helps ensure event emission
