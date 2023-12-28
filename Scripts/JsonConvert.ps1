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

    try {
        # Attempt to parse the received data as JSON
        $fileData = ConvertFrom-Json $data -ErrorAction Stop

        # Check if the parsed data contains exactly two strings
        if ($fileData -is [Array] -and $fileData.Count -eq 2 -and $fileData[0] -is [String] -and $fileData[1] -is [String]) {
            $source = $fileData[0]
            $destination = $fileData[1]

            # Perform operations using $source and $destination as required
            Write-Host "Source: $source, Destination: $destination"

            # Execute PowerShell commands using source and destination paths
            Get-Content $source -Raw -Encoding unicode | Out-File -FilePath $destination -Encoding utf8
            
            # Sending a response back to acknowledge the successful execution
            $response = $context.Response
            $responseContent = "Received valid source and destination paths: Source=$source, Destination=$destination"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseContent)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
            $response.Close()
        } else {
            Write-Host "Invalid data format. Expected exactly two strings."
        }
    } catch {
        Write-Host "Error parsing JSON data: $_"
    }

    # Stop the listener and exit the script after handling the request
    $listener.Stop()
    break
}
