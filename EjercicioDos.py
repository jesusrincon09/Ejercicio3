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

def validate_input(user_input):
    if user_input.strip().upper() == "FIN":
        return None
    if not user_input.isdigit():
        raise ValueError("Entrada inválida. Debe ser un número entero positivo o 'FIN'.")
    return int(user_input)


numbers = [7, 11, 15, 8, 1, 2]

print("Lista actual:", numbers)
print("------- Escriba 'FIN' para salir. -----\n")

while True:
    user_input = input("Ingrese el número objetivo a buscar: ")
    try:
        target = validate_input(user_input)
        if target is None:
            print("\nFin del programa")
            break
        result = find_indices(numbers, target)
        print("Resultado:", result, "\n")
    except ValueError as e:
        print(f"Error: {e}\n")