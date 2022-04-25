import requests
from django.db import connection
from .models import Comprobante,Pedido,DetallePedido
from lista_producto.models import Mueble,ListaProducto
from os import environ
from datetime import datetime

def generar_comprobante(tipo_de_comprobante: int,tipo_documento:str,numero_documento:str,pedido_id:int):
    """Sirve para generar un comprobante electronico ya sea Factura, Boleta, Nota de Credito de un pedidos."""
    pedido=Pedido.objects.filter(id=pedido_id).first()

    #comprobando(errores posibles si no existe) forma facil haciendo 2da consulkta 
    validacionComprobante=Comprobante.objects.filter(pedido=pedido.id).first()
    if validacionComprobante is not None:
        raise Exception('Este pedido ya tiene un comprobante')
     
    if pedido is None:
        raise Exception('Pedido no existe')

    if pedido.total>700 and tipo_documento is None:
        raise Exception('El pedido mayor a 700, requiere un cliente')

    operacion='generar_comprobante'
    tipo=''
    sunat_transaction=1
    if tipo_de_comprobante==1:
        #esta serie se deberia de guardar en la bd en una tabla de series para que cuando
        #el contador desee cambiar de serie se modifique enea tabla de series
        serie='FFF1' #Serie.objects.filter(tipo='FACTURA').first()
        tipo='FACTURA'
    elif tipo_de_comprobante==2:
        serie='BBB1'
        tipo='BOLETA'
    elif tipo_de_comprobante==3 or tipo_de_comprobante==4:
        serie='0001'
        tipo='NOTA'   

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM vista_prueba')

    #select * from comprobantes where tipo='boleta | 'factura' order by numero desc
    ultimoComprobante=Comprobante.objects.values_list('numero','serie').filter(tipo=tipo).order_by('-numero').first()
    print(ultimoComprobante)
    if ultimoComprobante is None:
        numero=12
    else:
        numero=int(ultimoComprobante[0])+1
    
    if tipo_documento is None:
        cliente_tipo_de_documento='-'
        cliente_numero_de_documento=None
    else:
        if tipo_documento =='RUC':
            cliente_tipo_de_documento=6
        elif tipo_documento =='DNI':
            cliente_tipo_de_documento=1
        
        cliente_numero_de_documento=numero_documento
        
        if tipo_documento=='RUC':
            respuesta_apiperu=requests.get("https://apiperu.dev/api/ruc/"+numero_documento,
                        headers={'Authorization':'Bearer '+environ.get('APIPERU_TOKEN')})
            if respuesta_apiperu.json().get('success')==False:
                raise Exception('Datos del cliente no validos')
            else:
                cliente_denominacion=respuesta_apiperu.json().get('data').get('nombre_o_razon_social')
                cliente_direccion=respuesta_apiperu.json().get('data').get('direccion_completa')
        elif tipo_documento=='DNI':
            respuesta_apiperu=requests.get("https://apiperu.dev/api/dni/"+numero_documento,
                        headers={'Authorization':'Bearer'+environ.get('APIPERU_TOKEN')})
            if respuesta_apiperu.json().get('success')==False:
                raise Exception('Datos del cliente no validos')
            else:
                cliente_denominacion=respuesta_apiperu.json().get('data').get('noombre_completo') 
                cliente_direccion=''

    #aqui se debe cambiar el email por el email del cliente obtenido del FRONT
    cliente_email='joseph.mendoza.gonzales@gmail.com'
    fecha_de_emision=datetime.now().strftime('%d-%m-%Y')
    moneda=1
    porcentaje_de_igv=18.00
    #valor total de la venta incluye IGV
    total=float(pedido.total)
    #el valor sin IGB (la bse inponible)
    total_gravada=total/1.18
    #el valor de igv
    total_igv=total-total_gravada

    enviar_automaticamente_a_la_sunat=True
    enviar_automaticamente_al_cliente=True
    formato_de_pdf="TICKET"
    detalle_pedido: list[DetallePedido]=pedido.detalle_pedidos.all()
    detraccion=False
    items=[]

    for detalle in detalle_pedido:
        #extraigo el stock de ese detalle
        lista_producto:ListaProducto =detalle.listaProductoId
        #extraigo el mueble de esa lista de producto
        mueble:Mueble =lista_producto.muebleId

        unidad_de_medida="NIU"
        codigo=mueble.id
        descripcion=mueble.nombre
        cantidad=detalle.cantidad
        #precio unitario es precio con IGV
        precio_unitario=float(lista_producto.precio_diario)
        valor_unitario=precio_unitario/1.18
        subtotal=valor_unitario*cantidad
        tipo_de_igv=1
        igv=subtotal*0.18
        total_producto=precio_unitario*cantidad
        item={
            "unidad_de_medida":unidad_de_medida,
            "codigo":codigo,
            "descripcion":descripcion,
            "cantidad":cantidad,                    
            "precio_unitario":precio_unitario,
            "valor_unitario":valor_unitario,
            "subtotal":subtotal,                    
            "tipo_de_igv":tipo_de_igv,
            "igv":igv,
            "total":total_producto,
            'anticipo_regularizacion':False
        }
        items.append(item)

    comprobante_body={
        "operacion":operacion,
        "tipo_de_comprobante":tipo_de_comprobante,
        'serie':serie,
        'numero':numero,
        'sunat_transaction':sunat_transaction,
        'cliente_tipo_de_documento':cliente_tipo_de_documento,
        'cliente_numero_de_documento':cliente_numero_de_documento,
        'cliente_denominacion':cliente_denominacion,
        'cliente_direccion':cliente_direccion,
        'cliente_email':cliente_email,
        'fecha_de_emision':fecha_de_emision,
        'moneda':moneda,
        'porcentaje_de_igv':porcentaje_de_igv,
        'total_gravada':total_gravada,
        'total_igv':total_igv,
        'total':total,
        'detraccion':detraccion,
        'observaciones':'',
        'enviar_automaticamente_a_la_sunat':enviar_automaticamente_a_la_sunat,
        'enviar_automaticamente_al_cliente':enviar_automaticamente_al_cliente,
        'medio_de-pago':'EFECTIVO',
        'formato_de_pdf':formato_de_pdf,
        'items':items
    }

    url_nubefact=environ.get('NUBEFACT_URL')
    headers_nubefact={
        'Authorization':environ.get('NUBEFACT_TOKEN'),
        'Content-Type':'application/json'
    }

    respuestaNubefact=requests.post(url_nubefact,headers=headers_nubefact,json=comprobante_body)

    if respuestaNubefact .json().get('error'):
        raise Exception(respuestaNubefact.json().get('error'))
    else:
        nuevoComprobante = Comprobante(
            serie=serie,
            numero=numero,
            pdf=respuestaNubefact.json().get('enlace_del_pdf'),
            cdr=respuestaNubefact.json().get('enlace_del_cdr'), 
            xml=respuestaNubefact.json().get('enlace_del_xml'),
            tipo=tipo,
            pedido=pedido
        )
        nuevoComprobante.save()
        return nuevoComprobante

    print(respuestaNubefact.json())
