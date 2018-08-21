
$ErrorActionPreference = "Stop"

$Env:Path = "$Env:Path;C:\ProgramData\chocolatey\bin;C:\Python36\Scripts"

# Function Do-IEESC {
#     $AdminKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A7-37EF-4b3f-8CFC-4F3A74704073}"
#     $UserKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A8-37EF-4b3f-8CFC-4F3A74704073}"
#     Set-ItemProperty -Path $AdminKey -Name "IsInstalled" -Value 0
#     Set-ItemProperty -Path $UserKey -Name "IsInstalled" -Value 0
#     Stop-Process -Name Explorer -Force -ErrorAction "Ignore"
#     Write-Host "IE Enhanced Security Configuration (ESC) has been disabled." `
#         -ForegroundColor Green
# }
#
# Function Do-WinRM {
#     # Not sure if this can be improved? It's taken from
#     # https://learn.chef.io/manage-a-node/windows/bootstrap-your-node/
#
#     winrm quickconfig -q
#     winrm set winrm/config/winrs '@{MaxMemoryPerShellMB="1024"}'
#     winrm set winrm/config '@{MaxTimeoutms="1800000"}'
#     winrm set winrm/config/service '@{AllowUnencrypted="true"}'
#     winrm set winrm/config/service/auth '@{Basic="true"}'
#
#     netsh advfirewall firewall add rule `
#         name="WinRM 5985" `
#         protocol=TCP `
#         dir=in `
#         localport=5985 `
#         action=allow
#     netsh advfirewall firewall add rule `
#         name="WinRM 5986" `
#         protocol=TCP `
#         dir=in `
#         localport=5986 `
#         action=allow
#
#     net stop winrm
#     sc.exe config winrm start= auto
#     net start winrm
#
#     Write-Host "WinRM setup complete" -ForegroundColor Green
# }

Function Do-Chocolatey {
    If ( Test-Path('C:\ProgramData\chocolatey\bin\choco.exe') ) {
        Write-Host 'Chocolatey Already Installed'
    } Else {
        Write-Host 'Installing Chocolatey'
        iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))
    }
}

Function Do-Google-Chrome {
    Write-Host 'Installing Google Chrome'

    # temporarily ignore checksums due to upstream issue! Please try to remove
    # this asap
    choco install -y google-chrome-x64 --ignore-checksum
    If (Test-Path('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')) {
        Write-Host "Google Chrome setup complete" -ForegroundColor Green
    } Else {
        Write-Host "Google Chrome setup failed" -ForegroundColor Red
        Exit 1
    }
}

Function Do-Python {
    Write-Host 'Installing Python'
    choco install -y python3 pip

    If (Test-Path('C:\Python37\python.exe')) {
        Write-Host "Python setup complete" -ForegroundColor Green
    } Else {
        Write-Host "Python setup failed" -ForegroundColor Red
        Exit 1
    }

    C:\Python37\Scripts\pip.exe install virtualenv
}

Function Do-Misc {
    Write-Host 'Installing Microsoft Visual C++ Build Tools'
    choco install -y microsoft-visual-cpp-build-tools

    Write-Host 'Installing Make'
    choco install -y make
}



# Function Test-RegistryValue {
#     param(
#         [Alias("RegistryPath")]
#         [Parameter(Position = 0)]
#         [String]$Path
#         ,
#         [Alias("KeyName")]
#         [Parameter(Position = 1)]
#         [String]$Name
#     )
#
#     process
#     {
#         If (Test-Path $Path)
#         {
#             $Key = Get-Item -LiteralPath $Path
#             If ($Key.GetValue($Name, $null) -ne $null)
#             {
#                 If ($PassThru)
#                 {
#                     Get-ItemProperty $Path $Name
#                 }
#                 Else
#                 {
#                     $true
#                 }
#             }
#             Else
#             {
#                 $false
#             }
#         }
#         Else
#         {
#             $false
#         }
#     }
# }

# Function Do-UAC {
#     Write-Host "Disabling UAC"
#     $EnableUACRegistryPath = "REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System"
#     $EnableUACRegistryKeyName = "EnableLUA"
#     $UACKeyExists = Test-RegistryValue -RegistryPath $EnableUACRegistryPath `
#                         -KeyName $EnableUACRegistryKeyName
#
#     If ($UACKeyExists)
#     {
#         Set-ItemProperty -Path $EnableUACRegistryPath `
#                          -Name $EnableUACRegistryKeyName `
#                          -Value 0
#     }
#     Else
#     {
#         New-ItemProperty -Path $EnableUACRegistryPath `
#                          -Name $EnableUACRegistryKeyName `
#                          -Value 0 `
#                          -PropertyType "DWord"
#     }
# }


# Do-IEESC
# Do-WinRM
Do-Chocolatey
Do-Google-Chrome
Do-Misc
Do-Python

# Do-UAC
Clear-History

Exit 0
