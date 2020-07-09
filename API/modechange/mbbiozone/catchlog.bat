@echo off
md D:\log
   adb pull /etc_rw/iozone_test/log D:\log
   adb pull /logfs/iozone_test/log D:\log
   adb pull /cache/iozone_test/log D:\log
   adb pull /lib/firmware/iozone_test/log D:\log
   adb pull /etc/avmap_rw/iozone_test/log D:\log
   adb pull /usr/wlan_backups/iozone_test/log D:\log