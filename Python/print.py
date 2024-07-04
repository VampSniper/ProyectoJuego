def labBin(archivo):
     # Open the file in read mode
    with open(archivo, 'r') as file:
        # Read all lines from the file
        lineas = file.readlines()
        # Create a matrix 'a' with dimensions 11x19 initialized with zeros
        a = [[0 for _ in range(19)] for _ in range(11)]
         # Iterate over the first 11 lines of the file (if they exist
        for i in range(0, 11, 1):
            if i < len(lineas):
                 # Extract specific characters from each line, skipping every other column
                b = ''.join(lineas[i][j] for j in range(1, 57, 3))  # Skip every other column
 # Copy the first 19 characters of 'b' into the i-th row of matrix 'a'
                for j in range(min(19, len(b))):
                    a[i][j] = b[j]
    return a
archivo = 'labBin.txt'
atravesar = labBin(archivo)
#for i in range(0, 11, 1):
#    for j in range(0, 19, 1):
#        print(atravesar[i][j])
#    print("//////////////////")

# Print the value at position (10, 1) in the matrix 'atravesar'
print(atravesar[10][1])

#10,8,6,4,2,0
#-1,0,1,2,3,4