from chat import SalaChat, Usuario

if __name__ == "__main__":
    sala = SalaChat("Arquitectura")
    ana, luis, eva = Usuario("Ana"), Usuario("Luis"), Usuario("Eva")
    for u in (ana, luis, eva):
        u.unirse(sala)

    ana.enviar("Hola a todos")          # difusión
    luis.enviar("Solo para Eva", "Eva")  # privado
    sala.retirar(eva)                    # nadie más se modifica
    ana.enviar("¿Siguen ahí?")
