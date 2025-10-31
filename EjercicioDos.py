""" Escribe una función en lenguaje de su preferencia que tome una lista de
enteros y un entero de destino, y devuelva los índices de los dos números
que sumados dan el resultado del entero destino. """

def find_indices(numbers, target):
    seen = {}

    for i, num in enumerate(numbers):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return "No se encontró ningún par que sume el valor objetivo."

numbers = [7, 11, 15,8,1,2]

print("Lista actual:", numbers)
print("------- Escriba 'FIN' para salir. -----\n")

while True:
    user_input = input("Ingrese el número objetivo a buscar: ")

    if user_input.strip().upper() == "FIN":
        print("\n Fin del programa")
        break

    try:
        target = int(user_input)
        result = find_indices(numbers, target)
        print("Resultado:", result, "\n")
    except ValueError:
        print("Error: Debe ingresar un número entero o 'FIN' para salir.\n")
