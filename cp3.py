temperaturas=[28,31,34,33],[25,27,29,28],[32,35,36,34],[24,26,25,27]
tempmed_1=(temperaturas[0][0]+temperaturas[0][1]+temperaturas[0][2]+temperaturas[0][3])/4
tempmed_2=(temperaturas[1][0]+temperaturas[1][1]+temperaturas[1][2]+temperaturas[1][3])/4
tempmed_3=(temperaturas[2][0]+temperaturas[2][1]+temperaturas[2][2]+temperaturas[2][3])/4
tempmed_4=(temperaturas[3][0]+temperaturas[3][1]+temperaturas[3][2]+temperaturas[3][3])/4
qtd_1=0
for x in range(4):
  if temperaturas[0][x]>=33:
    qtd_1=qtd_1+1
qtd_2=0
for x in range(4):
  if temperaturas[1][x]>=33:
    qtd_2=qtd_2+1
qtd_3=0
for x in range(4):
  if temperaturas[2][x]>=33:
    qtd_3=qtd_3+1
qtd_4=0
for x in range(4):
  if temperaturas[3][x]>=33:
    qtd_4=qtd_4+1
w=qtd_1
if qtd_1<qtd_2:
  w=qtd_2
if qtd_1<qtd_3:
  w=qtd_3
if qtd_1<qtd_4:
  w=qtd_4
print("sala 1, temperatura média e registros críticos:",tempmed_1,"e",qtd_1)
print("sala 2, temperatura média e registros críticos:",tempmed_2,"e",qtd_2)
print("sala 3, temperatura média e registros críticos:",tempmed_3,"e",qtd_3)
print("sala 4, temperatura média e registros críticos:",tempmed_4,"e",qtd_4)
print("sala com maior risco:",w)
