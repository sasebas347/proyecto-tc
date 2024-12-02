from twilio.rest import Client
from datetime import datetime
from sqlalchemy.orm import Session
from app import SessionLocal, ReferenciaPago, Cliente  # Importar desde app.py
import schedule
import time

# Función para enviar mensajes
def enviar_mensaje(celular, mensaje):
    account_sid = 'tu_account_sid'
    auth_token = 'tu_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=mensaje,
        from_='+1234567890',  # Número de Twilio
        to=celular
    )
    return message.sid

# Tarea diaria para verificar y actualizar estados
def verificar_cuentas():
    db = SessionLocal()
    hoy = datetime.now().date()
    referencias = db.query(ReferenciaPago).all()

    for referencia in referencias:
        cliente = db.query(Cliente).filter(Cliente.referencia_pago_id == referencia.id).first()
        if not cliente:
            continue

        dias_restantes = (referencia.fecha_cancelacion - hoy).days

        if referencia.estado == "no pago" and dias_restantes <= 3:
            enviar_mensaje(cliente.telefono, "Recuerda pagar antes del vencimiento.")
        elif referencia.estado == "no pago" and dias_restantes < 0:
            referencia.estado = "vencido"
            db.commit()
            enviar_mensaje(cliente.telefono, "Tu factura está vencida. Realiza el pago pronto.")
        elif referencia.estado == "vencido" and dias_restantes < -7:
            referencia.estado = "cortado"
            db.commit()
            enviar_mensaje(cliente.telefono, "Tu servicio ha sido suspendido. Contacta atención al cliente.")

    db.close()

# Programar la tarea diaria
schedule.every().day.at("08:00").do(verificar_cuentas)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)