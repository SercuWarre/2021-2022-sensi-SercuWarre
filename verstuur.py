teversturenwaarde = 0b0100110

for i in range(8):
    waarde = teversturenwaarde >> i & 1
    print(waarde)
