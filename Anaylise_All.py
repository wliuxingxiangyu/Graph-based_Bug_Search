#!/usr/bin/env python
# coding=utf-8

from idc import *
from idaapi import *

class AnayBinFil(object):
    def __init__(self):
        list = []
    
    def GetXref_String(self,ea,n):
        if (GetOpType(ea,n) == 2):
            ea = GetOperandValue(ea,n)
        if (not SegName(ea) == '.rodata'):
            addrx = idautils.DataRefsFrom(ea)
            for item in addrx:
                return self.GetXref_String(item,n)
            return idc.GetDisasm(ea)
        return GetString(ea)
        
    
    #get the register's content whose number is i from ea forward search
    def get_content_register(self,ea,i):
        #print hex(ea) , idc.GetDisasm(ea), i 
        if (GetOpType(ea,0) == 1 and GetOperandValue(ea,0) == i):# wanted register
            if (ua_mnem (ea) == 'LDR'):
                if (GetOpType(ea,1) == 2):
                    return self.GetXref_String(ea,1)
                elif (GetOpType(ea,1) == 4):
                    return self.get_content_register(PrevHead(ea),i)
                else :
                    print 'unkown Optype:' ,hex(ea),idc.GetDisasm(ea)
            elif (ua_mnem(ea) == 'MOV'):
                if (GetOpType(ea,1) == 5):
                    return GetOperandValue(ea,1)
                elif (GetOpType(ea,1) == 1):
                    return self.get_content_register(PrevHead(ea),GetOperandValue(ea,1))
                else:
                    print 'unkown OpType:',hex(ea),idc.GetDisasm(ea)
        else:
            return self.get_content_register(PrevHead(ea),i)


    #from a call instruction BackForward search parameter
    def BackForward(self,addr,n):
        Reg_content = []
        addr = PrevHead(addr)
        i = 0 # register number
        for i in range(n):
            Reg_content.append(self.get_content_register(addr,i))

        return Reg_content


    def Anayl_Func_Call(self, func_name, para_num):
         if func_name == "":
             return
         fun_addr = idc.LocByName(func_name)
         #print hex(fun_addr),idc.GetDisasm(fun_addr)
         call_addrs = idautils.CodeRefsTo(fun_addr,0)
         dic = {}
         for item in call_addrs:
             para = self.BackForward(item,para_num)
             xref_funname = GetFunctionName(item)
             dic[xref_funname] = para

         return dic

        

#test code
ana_fun_name = 'printf'#要分析的函数名
para_num = 3 #参数数量
ana = AnayBinFil()
dic = ana.Anayl_Func_Call(ana_fun_name,para_num)

print '在函数中','其调用参数为'
for item in dic:
    print item , dic[item]

'''
# get all names and it's addr
for x in Names():
    print x
'''   
