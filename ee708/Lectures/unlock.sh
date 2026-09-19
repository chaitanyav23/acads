param (
    [Parameter(Mandatory=$true, Position=0)] [string]$InputFile,
    [Parameter(Mandatory=$true, Position=1)] [string]$OutputFile
)

# 1. Resolve to full Windows paths first
$FullInputPath = Resolve-Path $InputFile
$FullOutputPath = Join-Path (Get-Location) $OutputFile

# 2. Convert Windows paths to WSL paths
$WslInput = wsl wslpath $FullInputPath
$WslOutput = wsl wslpath $FullOutputPath

# Prompt for password securely
$Password = Read-Host "Enter PDF Password" -AsSecureString
$PassPtr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password)
$PlainPass = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($PassPtr)

# 3. Run qpdf using the converted paths
wsl qpdf --password="$PlainPass" --decrypt "$WslInput" "$WslOutput"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: '$OutputFile' has been created." -ForegroundColor Green
} else {
    Write-Host "Error: Failed to decrypt the PDF." -ForegroundColor Red
}
