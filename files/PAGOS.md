# Configuración de pagos y entrega

La tienda está publicada como un sitio estático. El navegador puede enviar al
cliente al checkout seguro de la pasarela elegida (Wompi, PayPal o Stripe),
pero no debe decidir por sí mismo si un pago fue aprobado. La entrega de un
archivo digital debe ocurrir solamente después de que esa pasarela confirme
la transacción.

## Datos del producto

- **Producto:** MARATONaide — PDF + EPUB
- **Precio:** $45.000 COP
- **Entrega:** Dentro de 24 horas tras confirmación de pago (manual o automática)
- **Contacto:** maratonaide@gmail.com

## Antes de publicar

El checkout ahora deja elegir entre **tres pasarelas independientes**: Wompi,
PayPal y Stripe. El comprador escoge una en el formulario; el sitio nunca
procesa tarjetas por sí mismo, solo redirige al link correspondiente.

### Wompi (Colombia — tarjeta, PSE, Nequi)

1. Crea un **link de pago fijo en COP** para cada edición (ES, EN y FR).
   Wompi Colombia procesa COP, por lo que no se debe anunciar USD si el
   checkout cobra pesos colombianos.
2. Configura cada link con el nombre de la edición, precio de $45.000 COP, sin
   dirección de envío y con un SKU distinto (`maratonaide-es`,
   `maratonaide-en`, `maratonaide-fr`). Usa un link reutilizable.
3. Reemplaza las URLs de `PAYMENT_LINKS.wompi` en `js/checkout.js`:
   - `es`: ya configurado (VPOS_axGQjW)
   - `en`: PENDIENTE — crear link en Wompi
   - `fr`: PENDIENTE — crear link en Wompi
4. Configura en Wompi una URL de redirección hacia el sitio y un webhook HTTPS
   que reciba eventos de transacción. El webhook debe verificar la firma del
   evento y entregar el PDF/EPUB solo con estado `APPROVED`, importe y SKU
   esperados.

### PayPal (compradores internacionales)

1. Define el precio equivalente en USD (o la moneda que prefieras) para cada
   edición — PayPal no cobra en COP.
2. Crea un enlace **PayPal.me** (`paypal.me/tuUsuario/monto`) por edición, o un
   botón "Comprar ahora" desde PayPal Business (Herramientas de venta → Botones
   de pago), que también genera una URL en `www.paypal.com`.
3. Reemplaza las URLs de `PAYMENT_LINKS.paypal` en `js/checkout.js` con esos
   enlaces (uno por `es`, `en`, `fr`).
4. PayPal no envía webhook a un sitio estático en GitHub Pages: concilia los
   pagos manualmente en el panel de PayPal contra las solicitudes recibidas en
   Formspree, igual que con Wompi.

### Stripe (tarjeta internacional)

1. En el Dashboard de Stripe, crea un **Payment Link** por edición (Productos
   → Crear link de pago), con el precio en USD y sin necesidad de escribir
   código.
2. Copia la URL generada (empieza por `buy.stripe.com`) y reemplaza las URLs
   de `PAYMENT_LINKS.stripe` en `js/checkout.js`.
3. Igual que con PayPal, sin backend no hay entrega automática: usa el panel
   de Stripe para confirmar pagos `Succeeded` antes de enviar el archivo.

### Formspree (registro de solicitudes, para las tres pasarelas)

Confirma en Formspree que el formulario `meeyznvp` pertenece al correo del
vendedor y que permite solicitudes desde el dominio publicado. Los mensajes
ahora incluyen el campo `metodo_pago` (`wompi`, `paypal` o `stripe`) para que
sepas por dónde concilias cada pedido. Recuerda: estos mensajes son
solicitudes, **no son comprobantes de pago**.

## Entrega automática

GitHub Pages no puede recibir webhooks ni proteger secretos. Para automatizar
la entrega se necesita un endpoint de servidor (por ejemplo, una función
serverless) con estas responsabilidades por cada pasarela:

1. Validar la firma del webhook (Wompi tiene el suyo; Stripe también permite
   webhooks firmados; PayPal usa IPN/webhooks de PayPal Business).
2. Comprobar que la transacción está aprobada (`APPROVED` en Wompi,
   `Succeeded` en Stripe, `COMPLETED` en PayPal), corresponde al monto y SKU
   esperados, y no se ha procesado antes.
3. Guardar la orden y enviar al correo pagador los enlaces privados del PDF y
   EPUB de la edición comprada.
4. Marcar la transacción como entregada para que un reintento del webhook no
   genere otro envío.

Hasta que exista ese endpoint, concilia los pagos aprobados en el panel de
cada pasarela (Wompi, PayPal, Stripe) con la solicitud recibida en Formspree
— usa el campo `metodo_pago` para saber cuál revisar — y envía manualmente
los archivos.
