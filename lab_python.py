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


import json
import re
from datetime import datetime
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
    def __init__(self,id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio,dirlocal,nomvendedor): #metodo init inicialia los valores propios
        super().__init__(id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio) #super llama  al init(o a cualquier metodo) de la superclasey se instancia con los valores de la superclase y se agreg dep
        self.__dirlocal = dirlocal
        self.__nomvendedor = self.validar_nombreape(nomvendedor) #hereda el metodo de venta

    @property
    def dirlocal(self):
        return self.__dirlocal
    
    @property
    def nomvendedor(self):
        return self.__nomvendedor

    def to_dict(self): #utiliza el mismo metodo de arriba(pasa a dicc) y agrega dep
        data = super().to_dict()
        data["dirlocal"] = self.dirlocal
        data["nomvendedor"] = self.nomvendedor

        return data

    def __str__(self):  
        return f"{super().__str__()} - Direccion local: {self.dirlocal}- nombre vendedor: {self.nomvendedor}"

class VentaOnline(Venta):
    def __init__(self,id_venta, id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio,direnvio, metodopago):
        super().__init__(id_venta,id_producto,dnicliente ,nomcliente, apecliente, fecha, productovend,precio)
        self.__direnvio = direnvio
        self.__metodopago = metodopago

    @property
    def direnvio(self):
        return self.__direnvio
    
    @property
    def metodopago(self):
        return self.__metodopago

    def to_dict(self):
        data = super().to_dict()
        data["direnvio"] = self.direnvio
        data["metodopago"] = self.metodopago
        return data

    def __str__(self):
        return f"{super().__str__()} - direccion envio: {self.direnvio}- Metodo de pago: {self.metodopago}"

class GestionVentas:  #se aplica al CRUD a este clase
    def __init__(self, archivo):
        self.archivo = archivo #inicializamos el archivo

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
            datos = self.leer_datos() #primero se lee los datos del json
            id_venta   = venta.id_venta   
            if not str(id_venta) in datos.keys(): #busca si el id_venta ya existe
                datos[id_venta] = venta.to_dict() #si no existe, se crea, to_dict porq es el dicc que tiene todos los atributos 
                self.guardar_datos(datos) #json anterior + lo nuevo q se agrego
                print(f'Se guardo con exito')
            else: #si ya existe
                print(f'Venta  con id {id_venta } ya existe')
        except Exception as error:
            print(f'Error inesperado al crear venta: {error}')

    def leer_venta(self, id_venta):
        try:
            datos = self.leer_datos() #leemos los datos del json
            if id_venta in datos:
                venta_data = datos[id_venta] #id_venta porq se identifica por id_venta el diccionario
                if 'dirlocal' in venta_data:
                    venta = VentaLocal(**venta_data) #** porq es diccionario
                else:
                    venta = VentaOnline(**venta_data)
                print(f'venta encontrada con id {id_venta}')
            else:
                print(f'No se encontró venta con id {id_venta}')
        except Exception as e:
            print(f'Error al leer venta: {e}')



    def actualizar_venta(self, id_venta, nuevo_id):
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos.keys(): #se accede a las keys
                 datos[id_venta]['id_producto'] = nuevo_id 
                 self.guardar_datos(datos) 
                 print(f'Id producto actualizado para id venta:{id_venta}')
            else:
                print(f'No se encontró Id producto con id venta:{id_venta}')
        except Exception as e:
            print(f'Error al actualizar el id del producto: {e}')

    def eliminar_venta(self, id_venta):
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos.keys():
                 del datos[id_venta] #del elimina si encuentra, el objeto completo elimina
                 self.guardar_datos(datos)
                 print(f'Producto id:{id_venta} eliminado correctamente')
            else:
                print(f'No se encontró producto con id:{id_venta}')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')