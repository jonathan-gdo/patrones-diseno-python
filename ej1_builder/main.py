from automovil import AutomovilBuilder, DirectorAutomovil

if __name__ == "__main__":
    builder = AutomovilBuilder()

    # Construcción a medida, solo con lo que el cliente quiere
    auto = (builder.modelo("Familiar").motor("2.0L híbrido").color("Azul")
            .llantas("17\" aleación").con_gps().build())
    print(auto)

    # Configuraciones predefinidas mediante el director
    director = DirectorAutomovil(builder)
    print(director.basico())
    print(director.deportivo_full())

    # Inmutabilidad
    try:
        auto.color = "Negro"
    except Exception as e:
        print("Inmutable ->", type(e).__name__)
