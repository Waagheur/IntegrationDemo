import os
files = os.listdir()
banks = []
for i in range (0, len(files)):
    if files[i].endswith(".bnk"):
        banks.append(files[i])

#Read all files actions, switches, . . .
events = {}

def extract(file):
    with open(file, "rb") as f:
        bank_id = 0
        # Section reading
        while (bytes := f.read(4)):
            print("Section : ", bytes)
            if (bytes == b'BKHD'):
                length = f.read(4)
                print("Version number : ")
                print(int.from_bytes(f.read(4), 'little'))
                print("Soundbank ID : ")
                bank_id = int.from_bytes(f.read(4), 'little')
                # Skip the remainer of the section
                f.read(int.from_bytes(length, 'little') - 8)
            else:
                if (bytes == b'HIRC'):
                    # Remove length bytes
                    f.read(4)
                    # Read the number of objects in the HIRC section
                    nb = int.from_bytes(f.read(4), 'little')
                    # Read the objects' data and store it
                    for obj in range (0, nb):
                        object_type = f.read(1)
                        object_length = int.from_bytes(f.read(4), 'little') - 4
                        object_id = int.from_bytes(f.read(4), 'little')
                        match object_type:
                            case b'\x03':
                                f.read(object_length)
                            case b'\x04':
                                f.read(object_length)
                            case _:
                                object_data = f.read(object_length)
                                # Rack.append([object_id, object_type, object_length, object])
                        events[object_id] = [object_type, file, bank_id]
                else:
                    # Skip sections that don't interest us

                    # Read section length (length without what is already read)
                    length = f.read(4)
                    # Skip section
                    f.read(int.from_bytes(length, 'little'))

for i in range(0, len(banks)):
    extract(banks[i])



#Read a file's events segment
def read(file):
    with open(file, "rb") as f:
        Rack = []
        # Section reading
        while (bytes := f.read(4)):
            print("Section : ", bytes)
            if (bytes == b'BKHD'):
                length = f.read(4)
                print("Version number : ")
                print(int.from_bytes(f.read(4), 'little'))
                print("Soundbank ID : ")
                print(int.from_bytes(f.read(4), 'little'))
                # Skip the remainer of the file
                f.read(int.from_bytes(length, 'little') - 8)
            else:
                if (bytes == b'HIRC'):
                    # Remove length bytes
                    f.read(4)
                    # Read the number of objects in the HIRC section
                    nb = int.from_bytes(f.read(4), 'little')
                    # Read the objects' data and store it
                    for obj in range (0, nb):
                        object_type = f.read(1)
                        object_length = int.from_bytes(f.read(4), 'little') - 4
                        object_id = int.from_bytes(f.read(4), 'little')
                        object_data = f.read(object_length)
                        Rack.append([object_id, object_type, object_length, object])
                else:
                    # Skip sections that don't interest us

                    # Read section length (length without what is already read)
                    length = f.read(4)
                    # Skip section
                    f.read(int.from_bytes(length, 'little'))
    return Rack

# Display what was found
#print("\n")
#print("All HIRC objects")
#for i in range (0, len(Rack)):
#    print("Rack " + str(i) + " :")
#    print(Rack[i])

# Display types #4 only (Events)
#print("\n")
#print("Types #4")
#for i in range (0, len(Rack)):
#    if (Rack[i][1] == b'\x04'):
#        print("Rack " + str(i) + " :")
#        print(Rack[i])

# Display array of types #4 ids
#print("\n")
#print("Arrays of types #4 ids")
#for i in range(0, len(Rack)):
#    if (Rack[i][1] == b'\x04'):
#        print(str(Rack[i][0]) + "U, ")
