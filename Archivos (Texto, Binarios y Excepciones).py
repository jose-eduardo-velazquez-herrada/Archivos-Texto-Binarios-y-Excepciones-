import struct
import os

ARCHIVO_TEXTO = "coleccion_videojuegos.txt"
ARCHIVO_BINARIO = "datos_videojuegos.bin"

def inicializar_archivos():
    try:
        if not os.path.exists(ARCHIVO_TEXTO):
            with open(ARCHIVO_TEXTO, 'w', encoding='utf-8') as archivo:
                archivo.write("")
    except Exception as e:
        print(f"Error inicializando archivos: {e}")

def agregar_videojuego():
    try:
        nombre = input("Nombre del videojuego: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        
        consola = input("Consola: ").strip()
        if not consola:
            raise ValueError("La consola no puede estar vacía")
        
        anio = input("Año de lanzamiento: ").strip()
        if not anio.isdigit():
            raise ValueError("El año debe ser un número válido")
        anio = int(anio)
        
        tipo = input("Tipo de videojuego: ").strip()
        if not tipo:
            raise ValueError("El tipo no puede estar vacío")
        
        desarrollador = input("Desarrollador: ").strip()
        if not desarrollador:
            raise ValueError("El desarrollador no puede estar vacío")
        
        rareza = int(input("Rareza (1-100): ").strip())
        if rareza < 1 or rareza > 100:
            raise ValueError("La rareza debe estar entre 1 y 100")
        
        calificacion = float(input("Calificación (0-10): ").strip())
        if calificacion < 0 or calificacion > 10:
            raise ValueError("La calificación debe estar entre 0 y 10")
        
        with open(ARCHIVO_TEXTO, 'a', encoding='utf-8') as archivo:
            archivo.write(f"{nombre}|{consola}|{anio}|{tipo}|{desarrollador}\n")
        
        with open(ARCHIVO_BINARIO, 'ab') as archivo_bin:
            datos_binarios = struct.pack('50si50siiff', 
                nombre.encode('utf-8')[:50].ljust(50, b'\0'),
                len(nombre),
                desarrollador.encode('utf-8')[:50].ljust(50, b'\0'),
                len(desarrollador),
                anio,  
                rareza,
                calificacion
            )
            archivo_bin.write(datos_binarios)
        
        print("Videojuego agregado exitosamente.")
        
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    except Exception as e:
        print(f"Error al agregar videojuego: {e}")

def mostrar_coleccion():
    try:
        with open(ARCHIVO_TEXTO, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        if not lineas:
            print("La colección está vacía.")
            return
        
        print("\n=== COLECCIÓN DE VIDEOJUEGOS ===")
        for i, linea in enumerate(lineas, 1):
            datos = linea.strip().split('|')
            if len(datos) == 5:
                print(f"{i}. {datos[0]}")
                print(f"   Consola: {datos[1]}")
                print(f"   Año: {datos[2]}")
                print(f"   Tipo: {datos[3]}")
                print(f"   Desarrollador: {datos[4]}")
                print()
                
    except FileNotFoundError:
        print("No se encontró el archivo de colección.")
    except Exception as e:
        print(f"Error al mostrar colección: {e}")

def buscar_videojuego():
    try:
        nombre_buscar = input("Nombre a buscar: ").strip().lower()
        
        with open(ARCHIVO_TEXTO, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        encontrados = []
        for linea in lineas:
            datos = linea.strip().split('|')
            if len(datos) >= 1 and nombre_buscar in datos[0].lower():
                encontrados.append(datos)
        
        if encontrados:
            print(f"\nSe encontraron {len(encontrados)} videojuego(s):")
            for datos in encontrados:
                print(f"Nombre: {datos[0]}")
                print(f"Consola: {datos[1]}")
                print(f"Año: {datos[2]}")
                print(f"Tipo: {datos[3]}")
                print(f"Desarrollador: {datos[4]}")
                print()
        else:
            print("No se encontraron videojuegos con ese nombre.")
            
    except FileNotFoundError:
        print("No se encontró el archivo de colección.")
    except Exception as e:
        print(f"Error en la búsqueda: {e}")

def mostrar_datos_binarios():
    try:
        if not os.path.exists(ARCHIVO_BINARIO):
            print("No hay datos binarios almacenados.")
            return
        
        with open(ARCHIVO_BINARIO, 'rb') as archivo_bin:
            print("\n=== DATOS BINARIOS DE VIDEOJUEGOS ===")
            
            while True:
                bloque = archivo_bin.read(struct.calcsize('50si50siiff'))
                if not bloque:
                    break
                
                datos = struct.unpack('50si50siiff', bloque)
                nombre = datos[0][:datos[1]].decode('utf-8', errors='ignore')
                desarrollador = datos[2][:datos[3]].decode('utf-8', errors='ignore')
                anio = datos[4]  
                rareza = datos[5]  
                calificacion = datos[6]  
                
                print(f"Videojuego: {nombre}")
                print(f"Desarrollador: {desarrollador}")
                print(f"Año: {anio}")  
                print(f"Rareza: {rareza}/100")
                print(f"Calificación: {calificacion:.1f}/10")
                print()
                
    except Exception as e:
        print(f"Error al leer datos binarios: {e}")

def menu():
    inicializar_archivos()
    
    while True:
        print("\n" + "="*30)
        print("   MI COLECCIÓN DE VIDEOJUEGOS")
        print("="*30)
        print("1. Agregar videojuego")
        print("2. Mostrar colección completa")
        print("3. Buscar videojuego por nombre")
        print("4. Mostrar datos binarios")
        print("5. Salir")
        print("="*30)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            agregar_videojuego()
        elif opcion == "2":
            mostrar_coleccion()
        elif opcion == "3":
            buscar_videojuego()
        elif opcion == "4":
            mostrar_datos_binarios()
        elif opcion == "5":
            print("¡Gracias por usar la colección de videojuegos!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()