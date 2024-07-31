import os
import platform
import re

from lab_python import (
    VentaOnline,
    VentaLocal,
    GestionVentas,
)


def mostrar_menu():
    print("========== Menu de gestion de ventas de productos==========")
    print('1. Agregar Venta del local')
    print('2. Agregar Venta online')
    print('3. Buscar Venta por id')
    print('4. Actualizar Venta')
    print('5. Eliminar Venta por id')
    print('6. Mostrar todas las ventas')
    print('7. Salir')
    print('======================================================')


def agregar_venta(gestion, tipo_venta):
    try:
        id_venta= input('Ingrese id de la venta: ')
        id_producto= input('Ingrese id del producto vendido: ')
        dnicliente = input('Ingrese dni del cliente que compro el producto: ')
        nomcliente = input('Ingrese nombre del cliente que compro el producto: ')
        apecliente = input('Ingrese apellido del cliente que compro el producto: ')
        fecha = input('Ingrese la fecha en que se compro el producto: ')
        productovend = input('Ingrese el producto vendido: ')
        precio = input('Ingrese precio del producto vendido: ')

        if tipo_venta == '1':
            dirlocal = input('Ingrese la direccion del local donde se vendio: ')
            nomvendedor = input('Ingrese el nombre del vendedor: ')
            venta = VentaLocal(id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio,dirlocal,nomvendedor)
        elif tipo_venta == '2':
            direnvio = input('Ingrese direccion de envio: ')
            metodopago = input('Ingrese el metodo de pago: ')
            venta = VentaOnline(id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio,direnvio, metodopago)
        else:
            print('Opción inválida')
            return

        gestion.crear_venta(venta)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_venta_por_id(gestion): #se usa gestion en todo porq manjea el crud
    id_venta = input('Ingrese el id de la venta a buscar: ')
    gestion.leer_venta(id_venta)
    input('Presione enter para continuar...')


def actualizar_id_producto(gestion):
  try:
        id_venta = input('Ingrese el id de la venta para actualizar el id del producto: ')
        id_producto = input('Ingrese el id nuevo del producto: ')
        
        # Validar id_producto
        if not re.match(r'^[a-zA-Z0-9]+$', id_producto):
            raise ValueError("El ID del producto debe ser alfanumérico.")
        if len(id_producto) < 5 or len(id_producto) > 10:
            raise ValueError("El ID del producto debe tener entre 5 y 10 caracteres.")
        
        # Actualizar la venta en la gestión
        gestion.actualizar_venta(id_venta, id_producto)
        input('Presione enter para continuar...')

  except ValueError as e:
        print(f'Error en la validación del id del producto: {e}')
  except Exception as e:
        print(f'Error inesperado: {e}')

def eliminar_venta_por_id(gestion):
    id_venta = input('Ingrese el id de la venta a eliminar: ')
    gestion.eliminar_venta(id_venta)
    input('Presione enter para continuar...')

def mostrar_todos_las_ventas(gestion):
    print('=============== Listado completo de las Ventas ==============')
    for ventas in gestion.leer_datos().values(): #concatena los valores
        if 'nomvendedor' in ventas: 
            print(f"dni cliente: {ventas['dnicliente']} - nomvendedor: {ventas['nomvendedor']}")
        else:
            print(f"dni cliente: {ventas['dnicliente']} - direnvio: {ventas['direnvio']}")
    print('=====================================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_ventas = 'ventas_db.json' #crea el archivo y se guarda aca
    gestion = GestionVentas(archivo_ventas) #instancia obj de gestion

    while True:
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_venta(gestion, opcion) #opcion es el tipo
        
        elif opcion == '3':
            buscar_venta_por_id(gestion)

        elif opcion == '4':
            actualizar_id_producto(gestion)

        elif opcion == '5':
            eliminar_venta_por_id(gestion)

        elif opcion == '6':
            mostrar_todos_las_ventas(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
        

