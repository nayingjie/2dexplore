@echo off
set pypath=Python.exe
if exist C:\Python27 set pypath=C:\Python27\Python.exe
%pypath% main.py
