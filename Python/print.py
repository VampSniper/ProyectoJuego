def labBin(archivo):
    with open(archivo, 'r') as file:
        lineas = file.readlines()
        a = [[0 for _ in range(19)] for _ in range(11)]
        for i in range(0, 11, 1):
            if i < len(lineas):
                b = ''.join(lineas[i][j] for j in range(1, 57, 3))  # Saltear columnas de por medio

                for j in range(min(19, len(b))):
                    a[i][j] = b[j]
    return a
archivo = 'labBin.txt'
atravesar = labBin(archivo)
#for i in range(0, 11, 1):
#    for j in range(0, 19, 1):
#        print(atravesar[i][j])
#    print("//////////////////")
print(atravesar[10][1])

#10,8,6,4,2,0
#-1,0,1,2,3,4