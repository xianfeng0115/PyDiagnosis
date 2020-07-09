@echo off

set localpyth_etc_rw=/etc_rw/iozone_test
set localpyth_logfs=/logfs/iozone_test
set localpyth_cache=/cache/iozone_test
set localpyth_fwfs=/lib/firmware/iozone_test
set localpyth_avmap_rw=/etc/avmap_rw/iozone_test
set localpyth_ztefile=/usr/wlan_backups/iozone_test

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.

adb shell mount -o remount / -w
set path_iozone=%DIRNAME%iozone
set path_iozone_run=%DIRNAME%iozone_run
set path_iozone_start=%DIRNAME%start

adb shell rm -rf /etc_rw/ioz*
adb shell rm -rf /logfs/ioz*
adb shell rm -rf /cache/ioz*

adb shell mkdir -p %localpyth_etc_rw%/log
adb push %path_iozone% %localpyth_etc_rw%
adb push %path_iozone_run% %localpyth_etc_rw%
adb shell chmod -R 755 %localpyth_etc_rw%

adb shell mkdir -p %localpyth_logfs%/log
adb push %path_iozone% %localpyth_logfs%
adb shell chmod -R 755 %localpyth_logfs%

adb shell mkdir -p %localpyth_cache%/log
adb push %path_iozone% %localpyth_cache%
adb shell chmod -R 755 %localpyth_cache%

adb shell mkdir -p %localpyth_fwfs%/log
adb push %path_iozone% %localpyth_fwfs%
adb shell chmod -R 755 %localpyth_fwfs%

adb shell mkdir -p %localpyth_avmap_rw%/log
adb push %path_iozone% %localpyth_avmap_rw%
adb shell chmod -R 755 %localpyth_avmap_rw%

adb shell mkdir -p %localpyth_ztefile%/log
adb push %path_iozone% %localpyth_ztefile%
adb shell chmod -R 755 %localpyth_ztefile%

adb shell < %path_iozone_start%

