import math
import builtins
import random 



_builtin_print = builtins.print
def p(*args, sep=" ", end="\n", flush=False):
    texto = sep.join(str(a) for a in args)
    _builtin_print(texto, end=end, flush=flush)

print = p
primos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

def es_primo(n):
    if n < 2:
        return False
    pequeñas = primos
    for p_ in pequeñas:
        if n % p_ == 0:
            return n == p_
    return True

def factores_primos(n):
    f = []
    while n % 2 == 0:
        f.append(2)
        n //= 2
    p_ = 3
    while p_ * p_ <= n:
        while n % p_ == 0:
            f.append(p_)
            n //= p_
        p_ += 2
    if n > 1:
        f.append(n)
    return sorted(set(f))

def es_generador(g, p_):
    if math.gcd(g, p_) != 1:
        return False
    phi = p_ - 1
    for q in factores_primos(phi):
        if pow(g, phi // q, p_) == 1:
            return False
    return True

def encontrar_generador(p_):
    """Encuentra un generador para el grupo Z_p*"""
    if not es_primo(p_):
        return None
    
    phi = p_ - 1
    for g in range(2, p_):
        if es_generador(g, p_):
            return g
    return None

def pot_mod_pasos(base, exp, mod):
    print(f"Cálculo de {base}^{exp} mod {mod}.")
    print(f"Exponente en binario: {exp:b}.")
    resultado = 1
    base_actual = base % mod
    e = exp
    paso = 0
    while e > 0:
        paso += 1
        print(f"Paso {paso}: resultado={resultado}, base={base_actual}, e={e}.")
        if e & 1:
            resultado = (resultado * base_actual) % mod
            print(f"  e es impar, resultado=resultado*base % mod -> {resultado}.")
        base_actual = (base_actual * base_actual) % mod
        print(f"  base=base^2 % mod -> {base_actual}.")
        e >>= 1
    print(f"Resultado final: {resultado}.")
    return resultado

def validar_entradas(p_, g, a, b):
    if not es_primo(p_):
        raise ValueError("P debe ser primo.")
    if p_ <= 3:
        raise ValueError("P debe ser mayor a 3 para permitir claves privadas válidas.")
    if not (2 <= g <= p_ - 2):
        raise ValueError("G debe estar en el rango [2, P-2].")
    if not es_generador(g, p_):
        raise ValueError("G no es generador de Z_p* para el P dado.")
    if not (2 <= a <= p_ - 2):
        raise ValueError("Private_Alice debe estar en [2, P-2].")
    if not (2 <= b <= p_ - 2):
        raise ValueError("Private_Bob debe estar en [2, P-2].")

def ejecutar_intercambio(p_, g, a, b):
    validar_entradas(p_, g, a, b)
    print("Parámetros válidos.")
    print(f"P={p_}, G={g}, Private_Alice={a}, Private_Bob={b}.")
    print("\nCálculo de la clave pública de Alice: A = G^a mod P.")
    A = pot_mod_pasos(g, a, p_)
    print("\nCálculo de la clave pública de Bob: B = G^b mod P.")
    B = pot_mod_pasos(g, b, p_)
    print("\nIntercambio de claves públicas: Alice recibe B, Bob recibe A.")
    print("\nCálculo de la clave compartida en Alice: s = B^a mod P.")
    s_alice = pot_mod_pasos(B, a, p_)
    print("\nCálculo de la clave compartida en Bob: s = A^b mod P.")
    s_bob = pot_mod_pasos(A, b, p_)
    if s_alice != s_bob:
        raise RuntimeError("Las claves derivadas no coinciden.")
    print(f"\nClave compartida verificada: {s_alice}.")
    print("\nResumen de valores:")
    print(f"{'Variable':<15}{'Valor'}")
    print(f"{'-'*25}")
    print(f"{'P':<15}{p_}")
    print(f"{'G':<15}{g}")
    print(f"{'Private_Alice':<15}{a}")
    print(f"{'Private_Bob':<15}{b}")
    print(f"{'Public_Alice (A)':<15}{A}")
    print(f"{'Public_Bob (B)':<15}{B}")
    print(f"{'Shared_Key':<15}{s_alice}")
    return {"A": A, "B": B, "S": s_alice}

def leer_entero(m):
    while True:
        try:
            return int(input(m))
        except:
            print("Entrada inválida. Intenta de nuevo.")

def menu():
    print("Implementación de Diffie-Hellman.")
    print("1) Ingresar P, G, Private_Alice, Private_Bob.")
    print("2) Ejecutar ejemplo clásico (P=x, G=y, a=z, b=w).")
    print("3) Salir.")
    op = input("Opción: ").strip()
    if op == "1":
        p_ = leer_entero("P: ")
        while p_ > primos[-1] or p_ <= 3 or not es_primo(p_):
            if not es_primo(p_):
                print("P debe ser un número primo.")
            elif p_ <= 3:
                print("P debe ser mayor a 3 para permitir claves privadas válidas.")
            else:
                print("P debe ser menor o igual a 37 y que sea primo.")
            p_ = leer_entero("P: ")
        g = leer_entero("G: ")
        
        while g < 2 or g > p_ - 2:
            print("G debe estar en el rango [2, P-2].")
            g = leer_entero("G: ")
        
        while not es_generador(g, p_):
            print(f"G={g} no es generador de Z_{p_}*. Buscando un generador válido...")
            g_original = g
            g = 2
            while not es_generador(g, p_) and g < p_:
                g += 1
            if g < p_:
                print(f"Se encontró el generador {g}. ¿Usar este valor? (s/n): ", end="")
                if input().strip().lower() in ['s', 'si', 'y', 'yes']:
                    break
                else:
                    g = leer_entero("Ingresa otro valor para G: ")
            else:
                print("No se encontró un generador válido. Intenta con otro valor de P.")
                return
        a = leer_entero("Private_Alice: ")
        while a < 2 or a > p_ - 2:
            print("Private_Alice debe estar en el rango [2, P-2].")
            a = leer_entero("Private_Alice: ")
        b = leer_entero("Private_Bob: ")
        while b < 2 or b > p_ - 2:
            print("Private_Bob debe estar en el rango [2, P-2].")
            b = leer_entero("Private_Bob: ")
        
    
        ejecutar_intercambio(p_, g, a, b)
    elif op == "2":
        p_ = random.choice(primos)
        g = encontrar_generador(p_)
        if g is None:
            print(f"No se pudo encontrar un generador para p={p_}. Intentando con otro primo...")
            p_ = random.choice([p for p in primos if p != p_])
            g = encontrar_generador(p_)
        
        if p_ <= 3:
            print(f"P={p_} es demasiado pequeño para generar claves privadas válidas. Seleccionando otro primo...")
            p_ = random.choice([p for p in primos if p > 3])
            g = encontrar_generador(p_)
        
        a = random.randint(2, p_ - 2)
        b = random.randint(2, p_ - 2)
        print(f"P={p_}, G={g}, Private_Alice={a}, Private_Bob={b}.")
        ejecutar_intercambio(p_, g, a, b)
    else:
        print("Fin.")

if __name__ == "__main__":
    menu()