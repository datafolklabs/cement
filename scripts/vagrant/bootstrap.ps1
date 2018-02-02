function Do-IEESC {
    $AdminKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A7-37EF-4b3f-8CFC-4F3A74704073}"
    $UserKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A8-37EF-4b3f-8CFC-4F3A74704073}"
    Set-ItemProperty -Path $AdminKey -Name "IsInstalled" -Value 0
    Set-ItemProperty -Path $UserKey -Name "IsInstalled" -Value 0
    Stop-Process -Name Explorer
    Write-Host "IE Enhanced Security Configuration (ESC) has been disabled." `
        -ForegroundColor Green
}

function Do-WinRM {
    # Not sure if this can be improved? It's taken from 
    # https://learn.chef.io/manage-a-node/windows/bootstrap-your-node/

    winrm quickconfig -q
    winrm set winrm/config/winrs '@{MaxMemoryPerShellMB="1024"}'
    winrm set winrm/config '@{MaxTimeoutms="1800000"}'
    winrm set winrm/config/service '@{AllowUnencrypted="true"}'
    winrm set winrm/config/service/auth '@{Basic="true"}'
     
    netsh advfirewall firewall add rule `
        name="WinRM 5985" `
        protocol=TCP `
        dir=in `
        localport=5985 `
        action=allow
    netsh advfirewall firewall add rule `
        name="WinRM 5986" `
        protocol=TCP `
        dir=in `
        localport=5986 `
        action=allow
     
    net stop winrm
    sc.exe config winrm start= auto
    net start winrm

    Write-Host "WinRM setup complete" -ForegroundColor Green
}

function Do-Python2 {
    Invoke-WebRequest `
        -Uri https://www.python.org/ftp/python/2.7.11/python-2.7.11.amd64.msi `
        -OutFile python2-installer.msi

    msiexec /i python2-installer.msi /passive ALLUSERS=1 TARGETDIR=C:\Python27

    Start-Sleep -s 10

    C:\Python27\Scripts\pip.exe install virtualenv

    Write-Host "Python2 setup complete" -ForegroundColor Green

}

function Do-Python3 {
    Invoke-WebRequest `
        -Uri https://www.python.org/ftp/python/3.5.1/python-3.5.1-amd64.exe `
        -OutFile python3-installer.exe

    .\python3-installer.exe

    Start-Sleep -s 10

    C:\Python35\Scripts\pip.exe install virtualenv

    Write-Host "Python3 setup complete" -ForegroundColor Green

}

Do-IEESC
Do-WinRM
Do-Python2
Do-Python3
Clear-History
