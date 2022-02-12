@echo off

set Mainkey=HKEY_CURRENT_USER\SOFTWARE\Microsoft\InputMethod\Settings\CHS

for /f %%i in ('reg query %MainKey% /v "Enable Double Pinyin" ^| findstr /i "0x1"') do (set flg=%%i)

if not defined flg (
    reg add %MainKey% /v "Enable Double Pinyin" /t REG_DWORD /d 0x1 /f
    echo double-spelling
) else (
    reg add %MainKey% /v "Enable Double Pinyin" /t REG_DWORD /d 0x0 /f
    echo full-spelling
)

pause