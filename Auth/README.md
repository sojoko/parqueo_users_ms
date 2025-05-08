# HMAC Authentication

Este módulo proporciona autenticación HMAC para las peticiones a la API. La autenticación HMAC verifica que las peticiones provengan de un cliente autorizado utilizando una firma basada en una clave secreta compartida.

## Configuración

La autenticación HMAC requiere las siguientes variables de entorno:

- `USER_API_KEY`: La clave API que identifica al cliente
- `USER_SECRET_KEY`: La clave secreta utilizada para firmar las peticiones

Estas variables deben estar definidas en el archivo `.env` del proyecto.

## Cómo funciona

La autenticación HMAC se aplica globalmente a todas las rutas de la API, excepto a las rutas exentas definidas en `EXEMPT_ROUTES` en el archivo `hmac_sign.py`.

Actualmente, las siguientes rutas están exentas de autenticación HMAC:
- `/api/v1/login`
- `/api/v1/create_user`

## Requisitos para las peticiones

Para que una petición sea autenticada correctamente, debe incluir los siguientes headers:

- `x-api-key`: La clave API del cliente
- `x-timestamp`: El timestamp actual en formato Unix (segundos desde el epoch)
- `x-signature`: La firma HMAC generada

## Cómo generar la firma HMAC

La firma HMAC se genera de la siguiente manera:

1. Concatenar la clave API y el timestamp con dos puntos: `{x_api_key}:{x_timestamp}`
2. Firmar esta cadena utilizando HMAC-SHA256 con la clave secreta
3. Convertir el resultado a formato hexadecimal

Ejemplo en JavaScript:
```javascript
const crypto = require('crypto');

function generateSignature(apiKey, timestamp, secretKey) {
  const dataToSign = `${apiKey}:${timestamp}`;
  const signature = crypto.createHmac('sha256', secretKey)
    .update(dataToSign)
    .digest('hex');
  return signature;
}

// Uso
const apiKey = 'YOUR_API_KEY';
const timestamp = Math.floor(Date.now() / 1000);
const secretKey = 'YOUR_SECRET_KEY';
const signature = generateSignature(apiKey, timestamp, secretKey);

// Headers para la petición
const headers = {
  'x-api-key': apiKey,
  'x-timestamp': timestamp.toString(),
  'x-signature': signature
};
```

## Validación de la firma

La firma es válida si:
1. La clave API coincide con la configurada en el servidor
2. El timestamp no tiene más de 5 minutos de antigüedad
3. La firma coincide con la calculada por el servidor

Si alguna de estas condiciones no se cumple, la petición será rechazada con un error 401.