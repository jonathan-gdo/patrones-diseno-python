from notificaciones import (Alerta, Advertencia, Confirmacion, Mensaje,
                            PlataformaEscritorio, PlataformaMovil, PlataformaWeb)

if __name__ == "__main__":
    plataformas = [PlataformaEscritorio(), PlataformaMovil(), PlataformaWeb()]
    tipos = [Mensaje, Alerta, Advertencia, Confirmacion]

    # Todas las combinaciones tipo x plataforma sin subclases combinadas
    for tipo in tipos:
        for p in plataformas:
            print(tipo(p).enviar("Pago procesado"))

    # Cambio de plataforma en tiempo de ejecución
    n = Alerta(PlataformaWeb())
    print(n.enviar("Saldo bajo"))
    n.cambiar_plataforma(PlataformaMovil())
    print(n.enviar("Saldo bajo"))
