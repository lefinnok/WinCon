# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 00:45 2018

@author: CristiFati

*slightly modified*
"""

import sys
from ctypes import POINTER, WinDLL, Structure, sizeof, byref
from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE


LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11


class COORD(Structure):
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT),
    ]


class CONSOLE_FONT_INFOEX(Structure):
    _fields_ = [
        ("cbSize", ULONG),
        ("nFont", DWORD),
        ("dwFontSize", COORD),
        ("FontFamily", UINT),
        ("FontWeight", UINT),
        ("FaceName", WCHAR * LF_FACESIZE)
    ]


kernel32_dll = WinDLL("kernel32.dll")

get_last_error_func = kernel32_dll.GetLastError
get_last_error_func.argtypes = []
get_last_error_func.restype = DWORD

get_std_handle_func = kernel32_dll.GetStdHandle
get_std_handle_func.argtypes = [DWORD]
get_std_handle_func.restype = HANDLE

get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
get_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
get_current_console_font_ex_func.restype = BOOL

set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
set_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
set_current_console_font_ex_func.restype = BOOL


def modRes(height):
    while 1:
        try: 
            height = int(height)
            break
        except: 
            print('Invalid height, must be a number, try again.')
            height = input('||>')   
    
    print('Module by CristiFati from StackOverflow')
    # Get stdout handle
    stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
    if not stdout:
        print("{:s} error: {:d}".format(get_std_handle_func.__name__, get_last_error_func()))
        return
    # Get current font characteristics
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = sizeof(CONSOLE_FONT_INFOEX)
    res = get_current_console_font_ex_func(stdout, False, byref(font))
    if not res:
        print("{:s} error: {:d}".format(get_current_console_font_ex_func.__name__, get_last_error_func()))
        return
    # Display font information
    print("Console information for {:}".format(font))
    for field_name, _ in font._fields_:
        field_data = getattr(font, field_name)
        if field_name == "dwFontSize":
            print("    {:s}: {{X: {:d}, Y: {:d}}}".format(field_name, field_data.X, field_data.Y))
        else:
            print("    {:s}: {:}".format(field_name, field_data))
   
    # Alter font height
    font.dwFontSize.X = 10  # Changing X has no effect (at least on my machine)
    font.dwFontSize.Y = height
    # Apply changes
    res = set_current_console_font_ex_func(stdout, False, byref(font))
    if not res:
        print("{:s} error: {:d}".format(set_current_console_font_ex_func.__name__, get_last_error_func()))
        return
    print("OMG! The window changed :)")
    # Get current font characteristics again and display font size
    res = get_current_console_font_ex_func(stdout, False, byref(font))
    if not res:
        print("{:s} error: {:d}".format(get_current_console_font_ex_func.__name__, get_last_error_func()))
        return
    print("\nNew sizes    X: {:d}, Y: {:d}".format(font.dwFontSize.X, font.dwFontSize.Y))


if __name__ == "__main__":
    print("Python {:s} on {:s}\n".format(sys.version, sys.platform))
    modRes(10)