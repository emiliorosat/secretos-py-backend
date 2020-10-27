# Tarea 6

## Realiza un api en Python para una aplicación que es para registrar secretos personales

El api debe tener los siguientes métodos:

- Registrar usuario: se podrá agregar un usuario, pasando como paramento el correo, nombre y clave. Se debe validar que el usuario no exista en la db, y retornar un mensaje, indicando si fue posible crear el usuario que se mando a crear.
- Inicio de sesión, donde validara las credenciales que pasen (correo y clave) y va a retornar si es valida, junto a un token único para ese inicio sesión.
- Modificar mis datos: Se podrá modificar el nombre y correo electrónico.
- Cambiar Clave: Se podrá cambiar la contraseña enviando la clave anterior y el token.
- Ver mis secretos: Luego de iniciar sesión y enviando el toquen de alguna manera el usuario podrá ver sus secretos.
- Eliminar secreto: pasando alguna id de referencia eliminara el secreto seleccionado. Solo podrá eliminar los secretos del usuario.
- Registrar Secreto : Se podrá agregar un nuevo secreto, se deben pasar los datos que son:
    1. Titulo. => Es el titulo de su secreto.
    2. Descripción => Es lo que paso o detalles de lo que no quiere olvidar.
    3. Valor monetario. => Que cantidad de dinero esta involucrada en ese "secreto"
    4. Fecha => En que fecha aprox paso esto.
    5. Lugar => En donde paso.
    6. Lat y Lng => coordenadas de donde paso ese secreto.

- Cerrar Sesion: Se deshabilitar el token actual y se cerrara la sesión.

La base de datos que deben usar es SQLITE. Se vale usar Fastapi u otro que consideres pero siempre usando Python.
