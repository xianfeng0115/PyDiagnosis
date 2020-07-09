

from ctypes import *


       

def enum_win_processes(): 
    
    #PSAPI.DLL
    psapi = windll.psapi
    #Kernel32.DLL
    kernel = windll.kernel32
 
    arr = c_ulong * 256
    lpidProcess= arr()
    cb = sizeof(lpidProcess)
    cbNeeded = c_ulong()
    hModule = c_ulong()
    count = c_ulong()
    modname = c_buffer(30)
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    dic_process={}
 
    #Call Enumprocesses to get hold of process id's
    psapi.EnumProcesses(byref(lpidProcess),
                        cb,
                        byref(cbNeeded))
 
    #Number of processes returned
    nReturned = cbNeeded.value/sizeof(c_ulong())
 
    pidProcess = [i for i in lpidProcess][:nReturned]
 
    for pid in pidProcess:
 
        #Get handle to the process based on PID
        hProcess = kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                                      False, pid)
        if hProcess:
            psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
            psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
            dic_process["".join([ i for i in modname if i != '\x00'])] = pid
 
            #-- Clean up
            for i in range(modname._length_):
                modname[i]='\x00'
 
            kernel.CloseHandle(hProcess)
    return dic_process
