# X-Nav-5.7.17 - Servidor y cliente de chat con WebSocket con obsesión horaria

## Enunciado

Basándote en la implementación de chat de SimpleExampleServer.py del ejercicio anterior,
modifica el servidor para que sea un servicio de chat que además responda a los conectados
con la hora, cuando  ́estos se lo pidan mediante un mensaje
`getTime`.

Recuerda que puedes hacer uso de la biblioteca time de Python.

## Resultado

Para ejecutar esta práctica es necesario descargarla y arrancar el servidor de pyhton con:

`python SimpleExampleServer.py --example=chat`

Después para servir la página web que hace uso de este servidor podemos usar un módulo de python que actúa como un servidor (desde otra terminal):

`python -m SimpleHTTPServer 8001`

Por último una vez hecho esto abrimos en el navegador varias pestañas accediendo a `localhost:8001` y podremos usar el programa
