import math

def es_primo(n):
    if n < 2:
        return False
    pequeñas = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in pequeñas:
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in [2, 3, 5, 7, 11, 13, 17]:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        ok = False
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                ok = True
                break
        if not ok:
            return False
    return True

def factores_primos(n):
    f = []
    while n % 2 == 0:
        f.append(2)
        n //= 2
    p = 3
    while p * p <= n:
        while n % p == 0:
            f.append(p)
            n //= p
        p += 2
    if n > 1:
        f.append(n)
    return sorted(set(f))

def es_generador(g, p):
    if math.gcd(g, p) != 1:
        return False
    phi = p - 1
    for q in factores_primos(phi):
        if pow(g, phi // q, p) == 1:
            return False
    return True

def pot_mod_pasos(base, exp, mod):
    print(f"Cálculo de {base}^{exp} mod {mod}")
    print(f"Exponente en binario: {exp:b}")
    resultado = 1
    base_actual = base % mod
    e = exp
    paso = 0
    while e > 0:
        paso += 1
        print(f"Paso {paso}: resultado={resultado}, base={base_actual}, e={e}")
        if e & 1:
            resultado = (resultado * base_actual) % mod
            print(f"  e es impar, resultado=resultado*base % mod -> {resultado}")
        base_actual = (base_actual * base_actual) % mod
        print(f"  base=base^2 % mod -> {base_actual}")
        e >>= 1
    print(f"Resultado final: {resultado}")
    return resultado

def validar_entradas(p, g, a, b):
    if not es_primo(p):
        raise ValueError("P debe ser primo.")
    if not (2 <= g <= p - 2):
        raise ValueError("G debe estar en el rango [2, P-2].")
    if not es_generador(g, p):
        raise ValueError("G no es generador de Z_p* para el P dado.")
    if not (2 <= a <= p - 2):
        raise ValueError("Private_Alice debe estar en [2, P-2].")
    if not (2 <= b <= p - 2):
        raise ValueError("Private_Bob debe estar en [2, P-2].")

def ejecutar_intercambio(p, g, a, b):
    validar_entradas(p, g, a, b)
    print("Parámetros válidos")
    print(f"P={p}, G={g}, Private_Alice={a}, Private_Bob={b}")
    print("\nCálculo de la clave pública de Alice: A = G^a mod P")
    A = pot_mod_pasos(g, a, p)
    print("\nCálculo de la clave pública de Bob: B = G^b mod P")
    B = pot_mod_pasos(g, b, p)
    print("\nIntercambio de claves públicas: Alice recibe B, Bob recibe A")
    print("\nCálculo de la clave compartida en Alice: s = B^a mod P")
    s_alice = pot_mod_pasos(B, a, p)
    print("\nCálculo de la clave compartida en Bob: s = A^b mod P")
    s_bob = pot_mod_pasos(A, b, p)
    if s_alice != s_bob:
        raise RuntimeError("Las claves derivadas no coinciden.")
    print(f"\nClave compartida verificada: {s_alice}")
    return {"A": A, "B": B, "S": s_alice}

def leer_entero(m):
    while True:
        try:
            return int(input(m))
        except:
            print("Entrada inválida. Intenta de nuevo.")

def menu():
    print("Implementación de Diffie-Hellman")
    print("1) Ingresar P, G, Private_Alice, Private_Bob")
    print("2) Ejecutar ejemplo clásico (P=23, G=5, a=6, b=15)")
    print("3) Salir")
    op = input("Opción: ").strip()
    if op == "1":
        p = leer_entero("P: ")
        g = leer_entero("G: ")
        a = leer_entero("Private_Alice: ")
        b = leer_entero("Private_Bob: ")
        ejecutar_intercambio(p, g, a, b)
    elif op == "2":
        p, g, a, b = 23, 5, 6, 15
        ejecutar_intercambio(p, g, a, b)
    else:
        print("Fin")

if __name__ == "__main__":
    menu()
