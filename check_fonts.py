import os, glob

sys_fonts = glob.glob(r'C:\Windows\Fonts\msyh*') + glob.glob(r'C:\Windows\Fonts\simhei*') + glob.glob(r'C:\Windows\Fonts\simsun*')
print('System Chinese fonts found:')
for f in sys_fonts:
    print(f'  {f} ({os.path.getsize(f)} bytes)')
