<#
$source=$args[0]
$destination=$args[1]

Get-Content $source -Raw -Encoding unicode | Out-File -FilePath $destination -Encoding utf8
#>

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://*:8000/")
$listener.Start()

Write-Host "PowerShell listener started. Waiting for requests..."

while ($true) {
    $context = $listener.GetContext()
    $request = $context.Request
    $body = $request.InputStream
    $reader = New-Object System.IO.StreamReader($body, [System.Text.Encoding]::UTF8)
    $data = $reader.ReadToEnd()
    $reader.Close()
    $body.Close()

    Write-Host "Received POST request with data: $data"
    
    # Here you can process the received data as needed

    $response = $context.Response
    $responseContent = "Received data: $data"
    $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseContent)
    $response.ContentLength64 = $buffer.Length
    $response.OutputStream.Write($buffer, 0, $buffer.Length)
    $response.Close()

    # Stop the listener and exit the script after handling the request
    $listener.Stop()
    break
}
