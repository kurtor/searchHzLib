@echo off
start cmd /k "cd /d C:\ProgramData\Anaconda3\Scripts && activate.bat && cd /d %~dp0\ && python ./requestbook/rb_spyder.py"
