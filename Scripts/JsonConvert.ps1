$source=$args[0]
$destination=$args[1]

Get-Content $source -Raw -Encoding unicode | Out-File -FilePath $destination -Encoding utf8
