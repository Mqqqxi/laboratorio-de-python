'''
Objetivo: Desarrollar un sistema para registrar y gestionar ventas de productos.

Requisitos:

Crear una clase base Venta con atributos como fecha, cliente, productos vendidos, etc.
Definir al menos 2 clases derivadas para diferentes tipos de ventas (por ejemplo, VentaOnline, VentaLocal) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar las ventas.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.

'''

#ventalocal -> direccion tienda, nomvendedor
#ventaonline -> direccion de envio, metodo de pago

import mysql.connector
from mysql.connector import Error
from decouple import config
import json
import re
from datetime import datetime, date


       #metodo init inicializa a los atributos
class Venta:  #self hace ref a todos los atributos
    def __init__(self,id_venta,id_producto,dnicliente,nomcliente, apecliente, fecha, productovend,precio):   #init constructor -> metodo especial de py 
        self.__id_venta = self.validar_id(id_venta)  #se le asigna a cada variable-atributo
        self.__id_producto = self.validar_id(id_producto)
        self.__dnicliente = self.validar_dni(dnicliente)
        self.__nomcliente = self.validar_nombreape(nomcliente)   #__ -> dato protegido
        self.__apecliente = self.validar_nombreape(apecliente)
        self.__fecha = self.validar_fecha(fecha)
        self.__productovend = productovend
        self.__precio = self.validar_precio(precio)


    #encapsulamento 
    #solo para consultar datos
    @property   #a la funcion se lo convierte en propiedad, se hace para cada uno porq estan protegidos 
    def id_venta(self):  
        return self.__id_venta
    
    @property
    def id_producto(self):  
        return self.__id_producto
    
    @property
    def dnicliente(self):
        return self.__dnicliente
    
    
    @property
    def nomcliente(self): 
        return self.__nomcliente.capitalize() 
    
    @property
    def apecliente(self):
        return self.__apecliente.capitalize()
    
    @property
    def fecha(self):
        return self.__fecha
    
    #todos estos property son solo para consultar datos
    @property
    def productovend(self):
        return self.__productovend
    
    @property
    def precio(self):
        return self.__precio
    

     #para modificar se usa setter para guardar en el json
    @id_producto.setter
    def id_producto(self, nuevo_id):
        self.__id_producto = self.validar_id(nuevo_id)

    def validar_dni(self, dnicliente):
        try:
            dni_num = int(dnicliente)
            if len(str(dnicliente)) not in [7,8]: #para saber la long, se convierte a str
                raise ValueError("Debe tener 7-8 digitos el DNI")
            if dni_num <= 0:
                raise ValueError("El DNI debe ser positivo")
            if not str(dnicliente).isdigit(): #comprueba que no se ingresen letras
                raise ValueError("El DNI debe estar compuesto únicamente por digitos")
            return dni_num
        except ValueError:
            raise ValueError("El DNI debe ser positivo y estar compuesto por 8 digitos.")


    def validar_id(self, id_venta):
        try:
            if not re.match(r'^[a-zA-Z0-9]+$', id_venta):
                raise ValueError("El ID debe ser alfanumérico.")
            if len(id_venta) < 5 or len(id_venta) > 10:
                raise ValueError("El ID debe tener entre 5 y 10 caracteres.")
            return id_venta
        except ValueError as e:
            raise ValueError(f"Error de validación del ID: {e}")
        
    def validar_nombreape(self, nomapecliente):
        try:
            if not nomapecliente.isalpha():
                raise ValueError("El nombre o apellido del cliente solo debe estar formado por letras.")
            if len(nomapecliente) < 2 or len(nomapecliente) > 50:
                raise ValueError("El nombre o apellido del cliente debe tener entre 2 y 50 caracteres.")
            return nomapecliente
        except ValueError as e:
            raise ValueError(f"Error de validación del ID: {e}")



    def validar_fecha(self, fecha):
        try:
            # Si la fecha ya es un objeto datetime.date, connvertir a string
            if isinstance(fecha, date): 
                fecha = fecha.strftime('%Y-%m-%d')
            # Luego valida el string en formato AAAA-MM-DD
            datetime.strptime(fecha, '%Y-%m-%d')
            return fecha
        except ValueError:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")
    


        

        
    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError("El precio debe ser positivo.")
            return precio_num
        except ValueError as e:
            raise ValueError(f"Error de validación del precio: {e}")
    

    def to_dict(self):  #devuelve lso datos de cada atributo como diccionario
        return {
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "dnicliente": self.dnicliente,
            "nomcliente": self.nomcliente,
            "apecliente": self.apecliente,
            "fecha": self.fecha,
            "productovend": self.productovend,
            "precio": self.precio
        }

    def __str__(self):   #cuando se imprime el obj, devuelve nom y ape del obj
        return f"{self.nomcliente} {self.apecliente}"

class VentaLocal(Venta): #hereda todo de colab
    def __init__(self,id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio,dirlocal): #metodo init inicialia los valores propios
        super().__init__(id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio) #super llama  al init(o a cualquier metodo) de la superclasey se instancia con los valores de la superclase y se agreg dep
        self.__dirlocal = dirlocal


    @property
    def dirlocal(self):
        return self.__dirlocal
    


    def to_dict(self): #utiliza el mismo metodo de arriba(pasa a dicc) y agrega dep
        data = super().to_dict()
        data["dirlocal"] = self.dirlocal

        return data

    def __str__(self):  
        return f"{super().__str__()} - Direccion local: {self.dirlocal}"

class VentaOnline(Venta):
    def __init__(self,id_venta, id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio,direnvio):
        super().__init__(id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio)
        self.__direnvio = direnvio

    @property
    def direnvio(self):
        return self.__direnvio
    


    def to_dict(self):
        data = super().to_dict()
        data["direnvio"] = self.direnvio
        return data

    def __str__(self):
        return f"{super().__str__()} - direccion envio: {self.direnvio}"

class GestionVentas:  #se aplica al CRUD a este clase
    def __init__(self):
        self.host = config('DB_HOST') #inicializamos el archivo
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port= config('DB_PORT')

    def connect(self):
        '''Establecer una conexión con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )

            if connection.is_connected():
                return connection

        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None


    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file: #r -> metodo lectura
                datos = json.load(file) #toma el archivo, lee y lo guarda en datos
        except FileNotFoundError:
            return {} #retorna el dicc vacio
        except Exception as error: 
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:  
                json.dump(datos, file, indent=4) #dump-> obj de python lo pasa al archivo(jsno)
        except IOError as error: #indent cuanto espacio se deja
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_venta(self, venta):         
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #verif si idventa ya existe
                    cursor.execute('SELECT id_venta FROM venta WHERE id_venta = %s', (venta.id_venta,))
                    if cursor.fetchone():
                        print(f'Error: Ya existe venta con ese id {venta.id_venta}')
                        return
                    
                    # Insertar venta dependiendo del tipo
                    if isinstance(venta,VentaLocal):
                        query = '''
                        INSERT INTO venta (id_venta,id_producto,dnicliente,nomcliente,apecliente,fecha,productovend,precio)
                        VALUES (%s, %s, %s, %s, %s,%s,%s,%s)
                        '''
                        cursor.execute(query, (venta.id_venta, venta.id_producto,venta.dnicliente,venta.nomcliente,venta.apecliente,venta.fecha,venta.productovend,venta.precio))

                        query = '''
                        INSERT INTO ventalocal (id_venta,id_producto,dnicliente,nomcliente,apecliente,fecha,productovend,precio,dirlocal)
                        VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)
                        '''

                        cursor.execute(query, (venta.id_venta, venta.id_producto,venta.dnicliente,venta.nomcliente,venta.apecliente,venta.fecha,venta.productovend,venta.precio,venta.dirlocal))

                    elif isinstance(venta, VentaOnline):
                        query = '''
                        INSERT INTO venta (id_venta,id_producto,dnicliente,nomcliente,apecliente,fecha,productovend,precio)
                        VALUES (%s, %s, %s, %s, %s,%s,%s,%s)
                        '''
                        cursor.execute(query, (venta.id_venta, venta.id_producto,venta.dnicliente,venta.nomcliente,venta.apecliente,venta.fecha,venta.productovend,venta.precio))

                        query = '''
                        INSERT INTO ventaonline (id_venta,id_producto,dnicliente,nomcliente,apecliente,fecha,productovend,precio,direnvio)
                        VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)
                        '''

                        cursor.execute(query, (venta.id_venta, venta.id_producto,venta.dnicliente,venta.nomcliente,venta.apecliente,venta.fecha,venta.productovend,venta.precio,venta.direnvio))

                    connection.commit()
                    print(f'venta {venta.id_venta} creada correctamente')
        except Exception as error:
            print(f'Error inesperado al crear la venta: {error}')


    def leer_venta(self, id_venta):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM venta WHERE id_venta = %s', (id_venta,))  #, porq es una tupla
                    id_ventadata= cursor.fetchone()

                    if id_ventadata:
                        cursor.execute('SELECT dirlocal FROM ventalocal WHERE id_venta = %s', (id_venta,))
                        dirlocal = cursor.fetchone()

                        if dirlocal:
                            id_ventadata['dirlocal'] = dirlocal['dirlocal']
                            venta = VentaLocal(**id_ventadata)
                        else: #ventaonline
                            cursor.execute('SELECT direnvio FROM ventaonline WHERE id_venta = %s', (id_venta,))
                            direnvio = cursor.fetchone()
                            if direnvio:
                                id_ventadata['direnvio'] = direnvio['direnvio']
                                venta = VentaOnline(**id_ventadata) # se manda el diccionario
                            else:
                                venta = Venta(**id_ventadata)

                        print(f'Venta encontrada: {venta}')

                    else:
                        print(f'No se encontró venta con idventa {id_venta}.')

        except Error as e:
                print('Error al leer la venta: {e}')
        finally:
            if connection.is_connected():
                connection.close()



    def actualizar_venta(self, id_venta, nuevo_id):
        '''Actualizar el idproducto de una venta en al base de datos'''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el idventa existe
                    cursor.execute('SELECT * FROM venta WHERE id_venta = %s', (id_venta,))
                    if not cursor.fetchone():
                        print(f'No se encontro venta con idventa {id_venta}.')
                        return #termina todo, sino sigue con la actualizacion
                    
                    # Actualizar idproducto
                    cursor.execute('UPDATE venta SET id_producto = %s WHERE id_venta = %s', (nuevo_id, id_venta))

                    if cursor.rowcount > 0:  #cuenta filas
                        connection.commit()
                        print(f'Id de producto actualizado para la venta con ID: {id_venta}')
                    else:
                        print(f'no se encontró la venta con ID: {id_venta}')

        except Exception as e:
            print(f'Error al actualizar el ID: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_venta(self, id_venta):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                   # Verificar si idventa existe
                    cursor.execute('SELECT * FROM venta WHERE id_venta = %s', (id_venta,))
                    if not cursor.fetchone():
                        print(f'No se encontro venta con ID {id_venta}.')
                        return 

                    # Eliminar la venta
                    cursor.execute('DELETE FROM ventalocal WHERE id_venta = %s', (id_venta,))
                    cursor.execute('DELETE FROM ventaonline WHERE id_venta = %s', (id_venta,))
                    cursor.execute('DELETE FROM venta WHERE id_venta = %s', (id_venta,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Venta con ID: {id_venta} eliminado correctamente')
                    else:
                        print(f'No se encontró venta con ID : {id_venta}')

        except Exception as e:
            print(f'Error al eliminar la venta: {e}')
        finally:
            if connection.is_connected():
                connection.close()


    def leer_todos_las_ventas(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM venta')
                    ventas_data = cursor.fetchall()  #trae todos las ventas

                    ventas = []  #lista
                    
                    for venta_data in ventas_data:
                        id_venta = venta_data['id_venta']

                        cursor.execute('SELECT dirlocal FROM ventalocal WHERE id_venta = %s', (id_venta,))
                        dirlocal = cursor.fetchone()

                        if dirlocal:
                            venta_data['dirlocal'] = dirlocal['dirlocal']
                            venta= VentaLocal(**venta_data)
                        else:
                            cursor.execute('SELECT direnvio FROM ventaonline WHERE id_venta = %s', (id_venta,))
                            direnvio = cursor.fetchone()
                            venta_data['direnvio'] = direnvio['direnvio']
                            venta = VentaOnline(**venta_data)

                        ventas.append(venta)

        except Exception as e:
            print(f'Error al mostrar las ventas: {e}')
        else:
            return ventas
        finally:
            if connection.is_connected():
                connection.close()
