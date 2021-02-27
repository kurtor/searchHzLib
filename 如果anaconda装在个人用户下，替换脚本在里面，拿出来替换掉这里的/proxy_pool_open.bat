@echo off
start cmd /k "cd /d %userprofile%\anaconda3\Scripts && activate.bat &&conda.bat activate py35 &&cd /d %~dp0\proxy_pool && python proxyPool.py schedule"
timeout /t 2 /nobreak > nul
start cmd /k "cd /d %userprofile%\anaconda3\Scripts && activate.bat &&conda.bat activate py35 &&cd /d %~dp0\proxy_pool && python proxyPool.py server"
