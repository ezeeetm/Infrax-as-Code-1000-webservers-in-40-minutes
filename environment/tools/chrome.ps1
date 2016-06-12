while ($true)
{
$resp = Resolve-DnsName -Name test612.trycatchfinally.fail -Server ns-279.awsdns-34.com
$cname = $resp | where {$_.Type -eq 'CNAME'}
$cname.NameHost
Start-Process chrome.exe -ArgumentList @( '-incognito', $cname.NameHost )
#sleep -Seconds 1
}
