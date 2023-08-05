# dj-DoCodeStripe (Django-App)

[![N|Solid](https://docode.com.mx/img/poweredbydocode.png)](https://docode.com.mx/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

DoCodeStripes una aplicacion para configurar stripe dentro de un proyecto hecho en Django

### Tecnologia

DoCodeStripe se implementa con las siguientes librerias previamente instaladas:

* [Django](https://www.djangoproject.com/) - Python base framework (v2.2)
* [API Stripe](https://pypi.org/project/stripe/) - A Python library for Stripe´s API.

### Instalacion

Instalar por medio de [pip](https://pypi.org/project/pip/)

```sh
$ pip install dj-DoCodeStripe
```
### Estructura de la App
La aplicacion tiene una estructura comun de una app [Django](https://www.djangoproject.com/)
```sh
DoCodeStripe/
    procesos
    templates
    admin.py
    apps.py
    models.py
    urls.py
    views.py
```

### Configuracion:

Agregar la App a "INSTALLED_APPS" dentro de los **settings.py**
```sh
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DoCodeStripe',
]
```

Agregar las claves de Stripe en **settings.py** **(clave publicable y clave secreta)**
Configurar claves de API activas cuando **DEBUG=False** y la aplicación se encuentre en produccion.

```sh
# Configuracion de Stripe
if DEBUG:
    # Test Keys
    STRIPE_SECRET_KEY = ''
    STRIPE_PUBLISHABLE_KEY = ''
else:
    # Production Mode
    STRIPE_SECRET_KEY = ''
    STRIPE_PUBLISHABLE_KEY = ''
```

### Uso:

**views.py**
* Definir el Pago

Definir el pago dentro de la vista utilizando la libreria:
*definir_pago(tituloPago,descr,cantidad,logo,url)*
* tituloPago = Nombre del pago
* descr = Descripción del pago (concatena cantidad)
* cantidad = Monto a pagar (MXN)
* logo = Logo personalizado (formato 'static' ej. 'img/logo.png')
* url = Se define la url que apunta despues de realizar el pago.
* debug = Si el valor es **True** muestra una tarjeta demo para utilizar.

```sh
from DoCodeStripe.procesos import pago

def vista(request):
    context = {
      'titulo' : titulo,
    }
    # Definir el pago y agregar al contexto existente
    context_pagos = pago.definir_pago("PagoUnico","Cobrar",80,None,'url',True)
    context.update(context_pagos)
    
    return context
```

* Realizar el Pago

**urls.py**

Crear una url y una vista para realizar el Pago
```sh
path('miURLPago', views.miURLPago, name='miURLPago')
```
**views.py**

Se crea la vista en base a la url *miURLPago*, y se configuran los templates **pagado.html** y **noPagado.html**
```sh
# Vista para realizar el pago
def miURLPago(request):
    contexto = pago.realizar_pago(request,80,"Pago realizado con exito")
    
    # Se verifica si el pago fue exitoso para mostrar templates personalizados
    if contexto['pagado']:
        return render(request, 'pagado.html', context=contexto)
    else:
        return render(request, 'noPagado.html', context=contexto)
```

El metodo **realizar_pago()** regresa lo siguiente en forma de directorio:
```sh
titulo : Siempre es 'Pagos'
charge : La cantidad que se cobro (MXN)
nombre : Correo que se ingreso al pagar
cantidad : Cantidad que se cobro
pagado : Estatus del pago (True/False)
recibo : URL donde se puede verificar el recibo en Stripe
error: Si no se realiza el pago puede contener la causa
```



**template.html**

Implementar el boton para realizar los pagos en el template
```sh
{% include 'btnStripe_cardpay.html' %}
```

Configuracion basica del tamplate **pagado.html**
```sh
<!-- template pagado.html -->
<h2>Estatus de tu pago <strong>${{cantidad}}.00 MXN</strong>!</h2>

<h3>Informacion de Pago:</h3>
<p>{{nombre}}</p>
<p>{{cantidad}}</p>
<p>Pagado: {{pagado}}</p>
<p>{{recibo}}</p>
```
#### Actualizacion v1.1.6
* Ya se puede definir una URL dentro del metodo "definir_pago"

#### Actualizacion v1.1.5
* Se actualizan datos de prueba para tarjetas Demo

#### Actualizacion v1.1.4
* Se verifica el formulario al momento de enviar pago

#### Actualizacion v1.1.3
* Se actualiza objeto de retorno al momento de ralizar el pago 'realizar_pago()'

#### Actualizacion v1.1.2
* Se implementa template para agregar boton

#### Actualizacion v1.1.1

- Se implementa boton basico para uso de stripe


#### Licencia

MIT License

Copyright (c) 2020 DoCode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.