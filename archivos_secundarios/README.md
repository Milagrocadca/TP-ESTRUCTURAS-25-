# TP-ESTRUCTURAS-25-


EXAMEN FINAL:


ACLARACIONES:
- El programa detecta que no se pueden agregar mas de una vez el mismo tipo de vehiculo
- Al imprimirse los vehiculos con su informacion Costo kg es cero en camion y Costo km es cero en tren de carga porque por default al principio vale eso. 
- Si hay dos itinerarios que tienen el mismo valor minimo (KPI) (ejemplo: si el tiempo minimo es igual en ambos), devuelve el primer itinerario que se crea
- Toda solicitud debe tener un id_carga unico y no nulo
- Los graficos imprimen por solicitud. Por lo tanto, una solicitud tiene los graficos de kpi costo y tiempo. Hay graficos comentados segun lo comentado con Federico.
- Se puede cargar una vez el archivo de solicitudes. 


COMO EJECUTAR EL PROGRAMA:
1- Ejecutar desde main y seguir la guia del menu
  

COSAS QUE MODIFICAMOS:
- No modificamos la funcion calcular costo en vehiculos porque ya cumplia con los requisitos de las correcciones
- No modificamos la manera de calcular los graficos ya que no volvemos llamar a la funcion planificar, por ende, no volvemos a calcular el mejot itinerario. De modo que nuestro codigo ya cumplia con los requisitos de la correccion
- Los comentarios docstring ya se encontraban en la entrega anterior. En nuestra clase red es necesario almacenar en ambos sentidos, debido a nuestro codigo, de esta forma, considerariamos la ida y vuelta de los posibles viajes
- En nodos y conexiones cambiamos el path, ahora son un parametro de entrada que debe ingresar el usuario
- En la clase Vehiculos, modificamos el nombre de la clase maritimo por acuatico, asi no es repetitivo
- Sacamos los setters y getters no usados en el codigo (es decir, los que nunca fueron llamados ni utilizados)
- Restructuramos el main, los mensajes que se imprimian sobre el main los colocamos dentro del mismo y no en otros archivos
- Tambien modificamos el menu para que no haya posibilidad de que el usuario ingrese los datos de forma incorrecta
- En vehiculos modificamos una esructura SET por un DICCIONARIO ya que era la mejor forma de optimizar el tiempo de busqueda
- Eliminamos el archivo validaciones y sus funciones las agregamos en los archivos requeridos. Esto fue debido a que no eran utilizados en muchos archivos a la vez y, ademas, cada clase deberia encargarse de validar sus propios datos 
- Realizamos un diccionario de restricciones con el fin de facilitar el mantenimiento del codigo y organizar las restricciones. Esto se debe a que son atributos que pueden modificarse y necesitan estar dentro de una estructura
- Modificamos el archivo graficos con el fin de que todos los graficos se impriman a la vez y mejorar la visualizacion del programa
- Restrucuramos la funcion planificar: ahora la funcion planificar calcula unicamente los posibles itinerarios y la funcion seleccionar_mejor_itinerario elige las mejores rutas que cumplan con cada kpi. De este modo, al crear un itinerario en el main, el programa te devuelve UN ITINERARIO POR KPI
- Agregamos un tercer KPI que nos devuelva una ruta aleatoria con menos o igual a tres tramos
- Creamos un grafico estadistico con el objetivo de dibujar una red mostrando la utilización de cada conexión.
    - Los nodos son las ciudades.
    - Las aristas se dibujan más gruesas según cuántas veces se usaron en los itinerarios.
- Verificamos en el metodo agregar_conexion de la clase nodos que el parametro sea una instancia de conexion
















Lunes 26 de mayo: planteamos todas las clases bases de nuestro TP junto a un archivo dedicado a las validaciones.


Domingo 1 de junio: organizamos las variables ya que teniamos un problema cuando las definimos anteriormente. 
    Ademas, restructuramos la clase Vehiculos ya que era confuso el nombreamiento de las variables y agregamos las nuevas correcciones del tp subidas al campus.


Lunes 2 de junio: realizams la carga de archivos.
    Realizamos las funciones correspondientes a la clase Planificador: son aquellas que aportan en la eleccion de las rutas y la creacion de un plan de viaje.
    Agregamos que planificador devuelva el itinerario final y cree una clase Itinerario.
    Tenemos que solucionar dudas en clase sobre lo creado.

Martes 3 de junio: 
    Modificamos la velocidad de los aviones de acuerdo a la restriccion de mal clima.
    Creamos la clase red y modularizamos la funcion de cargar conexiones.
    Editamos la funcion evaluar ruta para que calcule la cantidad de vehiculos a utilizar de acuerdo al tramo mas "critico".
    Agregamos unos getters faltantes.

Sabado 7 de junio: 
    Reorganizamos main y organizamos planificador en base a lo trabajado anteriormente. 
    Probamos la carga de archivos

Domingo 8 de junio:
    Modificamos la relacion entre conexiones.
    Intentamos resolver los calculos de costo y tiempo

Lunes 9 de junio:
    Pensamos los graficos a realizar.
    Resolvimos los calculos de tiempo.
    Corregimos el print de itinerario, ahora imprime costo total y tiempo total siempre. Luego elige la mejor opcion segun el kpi elegido

Martes 10 de junio: 
    Teniamos problemas con caluclar el kpi, estuvimos toda la clase con el ayudante hasta que encontramos nuestro error. 
    Ademas notamos que los calculos propuestos por la catedra podrian estar mal.

Miercoles 11 de junio:
    Terminamos de solucionar problemas que teniamos con los graficos. Y creamos un grafico extra.
    Solucionamos varios problemas en el main, como pedia las solicitudes, como se presentaban las opciones a elegir
    Notamos que teniamos problemas con como habiamos entendido que funcionaba restriccion y valor_restriccion en el archivo de conexiones, entonces hicimos cambios en la clase vehiculos

Lunes 16 de junio:
    Corregimos las nuevas pautas recientes.
    Probamos todos los requisitos que debia cumplir nuestro codigos, y lo cumple con satisfaccion.



RESUMEN:

CLASE CONEXION: Se utiliza para encapsular la lógica y los atributos relacionados con una conexión (origen, destino, tipo, restricciones, etc.), permitiendo representar cada tramo como un objeto con comportamiento propio.
Dentro se utiliza random para simular de forma probabilística si hay mal clima en vuelos.

CLASE GRAFICOS: Para visualizar gráficamente distintos aspectos de los itinerarios de transporte. 
---  graficar_distancia_vs_tiempo() muestra cómo se acumula la distancia recorrida a medida que pasa el tiempo de cada itinerario creado. 
---  graficar_costo_vs_distancia() ilustra cómo se acumula el costo con la distancia total recorrida de cada itinerario creado. 
---  graficar_comparacion_itinerarios() compara dos itinerarios en términos de costo y tiempo total solo si los itinerarios de kpi costo y tiempo son distintos. 
--- Otras dos funciones comentadas permitirian ver los costos y timepos de cada modo de transporte.

CLASE INPUTS: Ambas funciones aseguran que los datos ingresados por el usuario cumplan con restricciones básicas antes de ser utilizados en el programa. 

CLASE ITINERARIO: Almacena los datos de la solicitud, el vehículo asignado, los tramos que componen el recorrido, el costo total, el tiempo total y el tipo de KPI (criterio de optimización). También guarda la cantidad máxima de vehículos necesarios en cualquier tramo.
Tuplas: self.tramos (origen, destino, conexion)
Cada tramo es una tupla para iterar y descomponer fácilmente.
Listas: tramos
para almacenar todos los tramos en orden secuencial y permite mantener la estructura de una ruta desde origen hasta destino.

CLASE MAIN: Permite gestionar vehículos, cargar solicitudes desde un archivo, planificar rutas optimizadas por costo y tiempo, y visualizar gráficos asociados. El flujo se asegura de ejecutar el planificador solo una vez para evitar duplicados.
Diccionario: en red_nodos.get_red()
Para representar la red de nodos y conexiones. 
Lista: solicitudes
Para almacenar todas las solicitudes cargadas desde archivo.

CLASE NODO: Cada nodo almacena su nombre, los modos de transporte habilitados y las conexiones salientes hacia otros nodos. 
Set: self.modos
Se utiliza para almacenar los modos de transporte habilitados, permite buscarlos eficientemente y evita repeticiones.

CLASE PLANIFICADOR: Encuentra rutas óptimas entre ciudades para solicitudes de transporte. Usa búsqueda en profundidad (_dfs) considerando restricciones del tipo de conexión, capacidad del vehículo y peso de la carga. Calcula itinerarios optimizados según un criterio e incluye una lógica especial para camiones por su restriccion personal. Y devuelve instancias de Itinerario como resultado final del plan.
Diccionario: self.nodos, self.vehiculos
Los nodos y vehículos se almacenan en diccionarios para permitir acceso rápido por nombre o tipo.
Lista: ruta, rutas_validas, self.itinerarios_validos
Set: visitados
El conjunto evita ciclos en la duncion dfs, marcando los nodos ya recorridos.
Tupla: cada tramo en la forma (origen, destino, vehiculo, conexion, cant_vehiculos)
Para registrar cada paso de una ruta.
Math.ceil: para calcular la cantidad necesaria de vehículos en función de la carga.

CLASE RED: Carga nodos como instancias de Nodo desde nodos.csv y conexiones bidireccionales desde conexiones.csv como instancias de Conexion.
Diccionario: self.red
Set: nodo.modos
Se usa para mantener los modos de transporte habilitados sin repeticiones.
En caso de querer modificar los archivos de nodos y conexiones, debera modificar el path. 

CLASE SOLICITUD: Permite cargar múltiples solicitudes desde un archivo CSV que es solicitado al usuario cuando se ejecuta el codigo. 
Set:solicitud.ids_usados
Para verificar que no se repita el ID de una carga.

CLASE VALIDACIONES: Define funciones reutilizables de validación de datos para otras clases del sistema.

CLASE VEHICULOS: Automotor, Tren, Aereo y Maritimo heredan de Vehiculo para definir vehículos específicos con valores predeterminados y comportamiento particular (costos especiales, cálculo de tiempo con clima).
Diccionario para almacenar vehiculos.

