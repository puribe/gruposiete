# Proyecto API SMA (GRUPO7)
   Este es un proyecto realizado en el curso "Desarrollo Aplicaciones Back-End Python-TalentoFuturo", el cual busca cubrir la necesidad de registrar y reportar medidas de avance de los diferentes PPDA por parte de los organismos sectoriales.

   #### Tecnologías utilizadas
   Las tecnologías utilizadas en este proyecto fueron las siguientes:
      
      - Lenguaje: Python
      - Base de Datos: PostgreSQL
      - Framework: Django
      - Versionamiento: GIT
      - Gestión del proyecto: Taiga

   

   ## Clonado e Instalación del proyecto

   - Para comenzar con la preparación e instalación del proyecto, debera ejecutar los siguiente comandos en la maquina en la cual se desplegará:

   ```bash
   # Clonamos el repositorio
   git clone https://github.com/puribe/gruposiete
   # Acceder a la carpeta
   cd gruposiete
   # Crear y activar entorno virtual
   python -m venv .venv
   # Linux/Mac
   source venv/bin/activate
   # Windows
   .venv\Scripts\activate
   # instalacion de librerias
   pip install -r requirements.txt
   ```

   ## Creación de la base de datos y ejecución de migraciones

   - Crear la base de datos (nombre de la base de datos `grupo7`) en PostgreSQL.
   - Crear (ya que no es parte del repositorio) el archivo ".env", para setear credenciales de acceso a la Base de Datos.

   El archivo .env debe situarse al mismo nivel del archivo manager.py y su estructura es la siguiente:

   ```bash
   SECRET_KEY = 'django-insecure-=)=&ii#5%w_#y+ad$b@_^^apm-szd=4njfuxpwz@+*m=9g=kkk'
   # Base de Datos
   NAME = 'grupo7'
   USER = ''
   PASSWORD = ''
   HOST = 'localhost'
   PORT = 5432

    # las variables se establecen según las credenciales locales de cada uno.
   ```
  

   - Luego ejecutar los siguientes comandos:

   ```bash
   python manage.py migrate
   python manage.py loaddata database.json
   # el archivo database.json incluye la creación del usuario administrador
   # por facilidad y sólo para uso local las credenciales son :
   # Username: admin
   # Password: admin
   ```

   ## Ejecución del proyecto
   - Para correr el proyecto, se debe ejecutar desde la carpeta de instalación, el siguiente comando:
      ```bash
      python manage.py runserver
      ```

   - Una vez realizado el paso anterior, la aplicación se ejecutará en:

      `http://127.0.0.1:8000/admin/` y `http://127.0.0.1:8000/api/`

   - Para probar el api, ingrese al panel de administracion:

     Ir a tokens y copiar el del usuario admin (para poder ejecutar todos los endpoints). 
     Cada vez que se crea un usuario, el sistema le asigna automáticamente un token. 

   - Luego en Postman seguir los pasos a continuación: 
      1. Abrir Postman.
      2. Seleccionar el método HTTP (GET, POST, etc.).
      3. Ingresar la URL de la API, por ejemplo:
         http://127.0.0.1:8000/api/organismos/
      4. En la pestaña "Authorization", agregar:
         - Auth Type: API Key
         - Key: Authorization
         - Value: Token [AQUI_VA_EL_TOKEN]
         (Ejemplo: Token 123456789abcdef123456789abcdef)
         - Add to: Header
      5. Presionar "Send" y verificar la respuesta.

   ## Proyecto publicado y en producción
   - https://gruposiete-er2w.onrender.com/api/

   ## Documentación

   - [Diagrama Modelo de Datos](documentation/img/grupo7-modelo_de_datos_public_v3.png)
   - La documentación de los endpoints fue generada con Swagger. Para acceder a ésta, la podemos encontrar en distintas fuentes:

      - [Swagger local](http://127.0.0.1:8000/api/docs/) (debe estar corriendo el proyecto)

      - [Swagger públicado en internet](https://app.swaggerhub.com/apis-docs/myorganization-834/api-de_sma/1.0.0#/)

      - [Postman](https://www.postman.com/ubicuacl/grupo7) (reemplazar por su token en API de SMA ->Variables -> apiKey )

   - Para acceder a la documentación en la cual se baso este proyecto, puede acceder a los siguientes enlaces:
      - [Documento-Presentacion-cliente](documentation/pdf/1-Presentacion-cliente.pdf)
      - [PPDA-Ejemplos-reporte](documentation/pdf/2-PPDA-ejemplos-reporte.pdf)
      - [Instrucciones-MMA-reporte-Diario-Oficial](documentation/pdf/3-200820-Dicta-Instrucciones-MMA.pdf)


   ## Autores

   - [@mayerlynyrs](https://www.github.com/mayerlynyrs)
   - [@puribe](https://www.github.com/puribe)
   - [@bianelbianchini](https://github.com/bianelbianchini)
   - [@eltan-ing](https://github.com/eltan-ing)
   - [@seba2305](https://github.com/seba2305)

