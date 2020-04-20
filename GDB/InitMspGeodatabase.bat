@echo off

SET PYTHON="C:\Python27\ArcGIS10.6\python.exe"
%PYTHON% "%~dp0\InitMspGeodatabase.py" %1

pause