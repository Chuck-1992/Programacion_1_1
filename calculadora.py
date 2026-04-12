# **********************************************************************************************
# Calculadora básica con interfaz gráfica en Python
# Solicita dos o más números, valida la entrada, realiza una determinada operación aritmética
# y finalmente muestra un análisis a partir del resultado obtenido
# **********************************************************************************************

import tkinter as tk
from tkinter import messagebox


# Declaración de variables
UMBRAL_ANALISIS = 1000
NUMERO_MAXIMO_PERMITIDO = 1000000
nombre_usuario = ""


# Método para maximizar la ventana al momento de abrirla
def maximizar_ventana(ventana):
    try:
        ventana.state("zoomed")
    except tk.TclError:
        ancho = ventana.winfo_screenwidth()
        alto = ventana.winfo_screenheight()
        ventana.geometry(f"{ancho}x{alto}+0+0")

    ventana.resizable(True, True)


# Método para formatear un número, eliminando decimales y ceros innecesarios
def formatear_numero(numero):
    numero = round(float(numero), 10)

    if numero.is_integer():
        return str(int(numero))

    return f"{numero:.10f}".rstrip("0").rstrip(".")



# Método para validar el nombre del usuario antes de abrir la calculadora
def iniciar_calculadora(event=None):

    global nombre_usuario

    nombre = entrada_nombre.get().strip()
    mensaje_error.config(text="")

    if nombre == "":
        mensaje_error.config(text="Por favor, ingrese su nombre.")
        return

    if len(nombre) < 5:
        mensaje_error.config(text="El nombre debe tener mínimo 5 caracteres.")
        return

    if len(nombre) > 25:
        mensaje_error.config(text="El nombre no debe superar los 25 caracteres.")
        return

    nombre_usuario = nombre

     # Cerramos la ventana de bienvenida
    ventana_bienvenida.destroy()

    # Abrimos la ventana de la calculadora
    abrir_calculadora() 


# Método para construir la interfaz de la calculadora, procesar las operaciones aritméticas y mostrar un análisis del resultado
def abrir_calculadora():
    ventana = tk.Tk()
    ventana.title("Calculadora Básica | Python")
    ventana.configure(bg="#0f1117")
    maximizar_ventana(ventana)

    entrada_actual = "0"
    primer_valor = None
    operador_actual = None
    reiniciar_pantalla = False

    variable_pantalla = tk.StringVar(value="0")

    # Método para actualizar el contenido visible en la pantalla de la calculadora
    def actualizar_pantalla():
        variable_pantalla.set(entrada_actual)


    # Método para devolver el símbolo visual correspondiente al operador matemático
    def obtener_operador_simbolo(operador):
        if operador == "+":
            return "+"
        if operador == "-":
            return "−"
        if operador == "*":
            return "×"
        if operador == "/":
            return "÷"
        return operador
    
    # Método para limpiar la caja de análisis de resultado
    def limpiar_analisis():
        caja_analisis.config(state="normal")
        caja_analisis.delete("1.0", tk.END)
        caja_analisis.insert(tk.END, "Aquí se mostrará el análisis del resultado.", "normal")
        caja_analisis.config(state="disabled")


    # Método para mostrar en la caja de análisis un mensaje de error relacionado con la operación realizada
    def mostrar_error_analisis(mensaje):
        caja_analisis.config(state="normal")
        caja_analisis.delete("1.0", tk.END)
        caja_analisis.insert(tk.END, "Error:\n", "titulo")
        caja_analisis.insert(tk.END, mensaje, "normal")
        caja_analisis.config(state="disabled")


    # Método para mostrar en la caja de análisis el resumen de la operación realizzada
    def mostrar_analisis(primer_numero, operador, segundo_numero, resultado):
        tipo_resultado = ""
        tipo_numero = ""

        if resultado > 0:
            tipo_resultado = "Positivo"
        elif resultado < 0:
            tipo_resultado = "Negativo"
        else:
            tipo_resultado = "Cero"

        if float(resultado).is_integer():
            tipo_numero = "Entero"
        else:
            tipo_numero = "Decimal"

        supera_umbral = resultado > UMBRAL_ANALISIS

        if supera_umbral:
            mensaje_umbral = f"Sí, supera el umbral de {UMBRAL_ANALISIS}."
        else:
            mensaje_umbral = f"No, no supera el umbral de {UMBRAL_ANALISIS}."

        resumen = (
            f"{formatear_numero(primer_numero)} "
            f"{obtener_operador_simbolo(operador)} "
            f"{formatear_numero(segundo_numero)} = "
            f"{formatear_numero(resultado)}"
        )

        caja_analisis.config(state="normal")
        caja_analisis.delete("1.0", tk.END)

        caja_analisis.insert(tk.END, "Resumen del cálculo:\n", "titulo")
        caja_analisis.insert(tk.END, resumen + "\n\n", "normal")

        caja_analisis.insert(tk.END, "Tipo de resultado: ", "titulo")
        caja_analisis.insert(tk.END, tipo_resultado + "\n", "normal")

        caja_analisis.insert(tk.END, "Clasificación numérica: ", "titulo")
        caja_analisis.insert(tk.END, tipo_numero + "\n", "normal")

        caja_analisis.insert(tk.END, "¿Supera el umbral?: ", "titulo")
        caja_analisis.insert(tk.END, mensaje_umbral, "normal")

        caja_analisis.config(state="disabled")


    # Método para agregar un número o punto decimal a la entrada actual y actualizar la pantalla de la calculadora
    def agregar_numero(numero):
        nonlocal entrada_actual, reiniciar_pantalla

        if entrada_actual == "Error":
            entrada_actual = "0"

        if reiniciar_pantalla:
            entrada_actual = ""
            reiniciar_pantalla = False

        if numero == "." and "." in entrada_actual:
            return

        if entrada_actual == "0" and numero != ".":
            entrada_actual = numero
        else:
            entrada_actual += numero

        actualizar_pantalla()

    # Método para guardar el operador seleccionado y preparar la calculadora para ingresar el segundo valor
    def establecer_operador(operador):
        nonlocal entrada_actual, primer_valor, operador_actual, reiniciar_pantalla

        if entrada_actual == "Error":
            return

        if operador_actual is not None and not reiniciar_pantalla:
            calcular_resultado()

        try:
            primer_valor = float(entrada_actual)
            operador_actual = operador
            reiniciar_pantalla = True
        except ValueError:
            entrada_actual = "Error"
            actualizar_pantalla()


    # Método para realizar la operación seleccionada, validar posibles errores y mostrar el resultado junto con su análisis
    def calcular_resultado():
        nonlocal entrada_actual, primer_valor, operador_actual, reiniciar_pantalla

        if operador_actual is None or reiniciar_pantalla:
            return

        try:
            segundo_valor = float(entrada_actual)
            primer_numero_operacion = primer_valor
            operador_operacion = operador_actual

            if operador_actual == "+":
                resultado = primer_valor + segundo_valor
            elif operador_actual == "-":
                resultado = primer_valor - segundo_valor
            elif operador_actual == "*":
                resultado = primer_valor * segundo_valor
            elif operador_actual == "/":
                if segundo_valor == 0:
                    entrada_actual = "Error"
                    operador_actual = None
                    primer_valor = None
                    reiniciar_pantalla = True
                    actualizar_pantalla()
                    mostrar_error_analisis("No se puede dividir para cero.")
                    return
                resultado = primer_valor / segundo_valor
            else:
                return

            resultado = round(resultado, 10)

            if abs(resultado) > NUMERO_MAXIMO_PERMITIDO:
                messagebox.showwarning(
                    "Límite excedido",
                    f"Ha excedido el número máximo permitido ({NUMERO_MAXIMO_PERMITIDO})."
                )
                limpiar_pantalla()
                return

            entrada_actual = formatear_numero(resultado)
            operador_actual = None
            primer_valor = None
            reiniciar_pantalla = True

            actualizar_pantalla()
            mostrar_analisis(
                primer_numero_operacion,
                operador_operacion,
                segundo_valor,
                resultado
            )

        except ValueError:
            entrada_actual = "Error"
            actualizar_pantalla()
            mostrar_error_analisis("Se produjo un problema al procesar la operación.")


    # Método para limpiar la pantalla y restablecer los valores iniciales de la calculadora
    def limpiar_pantalla():
        nonlocal entrada_actual, primer_valor, operador_actual, reiniciar_pantalla

        entrada_actual = "0"
        primer_valor = None
        operador_actual = None
        reiniciar_pantalla = False
        actualizar_pantalla()
        limpiar_analisis()

    # Método para volver a la ventana de inicio
    def volver_a_inicio():
        ventana.destroy()
        main()


    # Método para detectar la tecla presionada y ejecutar la acción correspondiente en la calculadora
    def tecla_presionada(evento):
        tecla = evento.keysym
        caracter = evento.char

        if caracter.isdigit() or caracter == ".":
            agregar_numero(caracter)
        elif caracter in ["+", "-", "*", "/"]:
            establecer_operador(caracter)
        elif tecla == "Return":
            calcular_resultado()
        elif tecla == "Escape" or caracter.lower() == "c":
            limpiar_pantalla()

 
    # Marco principal de la ventana que se expande para contener toda la interfaz
    contenedor_general = tk.Frame(ventana, bg="#0f1117")
    contenedor_general.pack(fill="both", expand=True)


    # Encabezado superior de la interfaz que contiene el mensaje de bienvenida y el botón de retorno al inicio
    header = tk.Frame(contenedor_general, bg="#0f1117")
    header.pack(fill="x", padx=20, pady=15)

    top_bar = tk.Frame(header, bg="#0f1117")
    top_bar.pack(fill="x")

    saludo = tk.Label(
        top_bar,
        text=f"Hola, {nombre_usuario}",
        bg="#1a1d24",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=14,
        pady=10,
        anchor="w"
    )
    saludo.pack(side="left", fill="x", expand=True)

    boton_volver = tk.Button(
        top_bar,
        text="Volver a inicio",
        bg="#d85b5b",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=14,
        pady=10,
        command=volver_a_inicio,
        cursor="hand2"
    )
    boton_volver.pack(side="right", padx=(12, 0))

    # Estructura principal del contenido, encargada de ocupar el espacio disponible y centrar el panel principal de la calculadora
    main_content = tk.Frame(contenedor_general, bg="#0f1117")
    main_content.pack(fill="both", expand=True, padx=20, pady=10)

    # Este contenedor ocupa toda la pantalla disponible
    zona_central = tk.Frame(main_content, bg="#0f1117")
    zona_central.pack(fill="both", expand=True)

    # Este panel queda centrado dentro de la zona central
    panel_principal = tk.Frame(zona_central, bg="#0f1117")
    panel_principal.place(relx=0.5, rely=0.5, anchor="center")


    # Contendor para los elementos de la calculadora
    contenedor = tk.Frame(panel_principal, bg="#0f1117")
    contenedor.pack(side="left", padx=(0, 20), anchor="n")

    calculator = tk.Frame(
        contenedor,
        bg="#111318",
        padx=20,
        pady=20
    )
    calculator.pack()

    display = tk.Entry(
        calculator,
        textvariable=variable_pantalla,
        font=("Arial", 34),
        justify="right",
        bd=0,
        relief="flat",
        bg="#1a1d24",
        fg="white",
        readonlybackground="#1a1d24"
    )
    display.configure(state="readonly")
    display.pack(fill="x", pady=(0, 18), ipady=18)

    buttons_frame = tk.Frame(calculator, bg="#111318")
    buttons_frame.pack(fill="both", expand=True)

    botones = [
        ("AC", 0, 0, 1, "#d85b5b", limpiar_pantalla),
        ("÷", 0, 1, 1, "#3b4360", lambda: establecer_operador("/")),
        ("×", 0, 2, 1, "#3b4360", lambda: establecer_operador("*")),
        ("−", 0, 3, 1, "#3b4360", lambda: establecer_operador("-")),

        ("7", 1, 0, 1, "#2d3342", lambda: agregar_numero("7")),
        ("8", 1, 1, 1, "#2d3342", lambda: agregar_numero("8")),
        ("9", 1, 2, 1, "#2d3342", lambda: agregar_numero("9")),
        ("+", 1, 3, 1, "#3b4360", lambda: establecer_operador("+")),

        ("4", 2, 0, 1, "#2d3342", lambda: agregar_numero("4")),
        ("5", 2, 1, 1, "#2d3342", lambda: agregar_numero("5")),
        ("6", 2, 2, 1, "#2d3342", lambda: agregar_numero("6")),
        ("=", 2, 3, 2, "#9dbcf2", calcular_resultado),

        ("1", 3, 0, 1, "#2d3342", lambda: agregar_numero("1")),
        ("2", 3, 1, 1, "#2d3342", lambda: agregar_numero("2")),
        ("3", 3, 2, 1, "#2d3342", lambda: agregar_numero("3")),

        ("0", 4, 0, 2, "#2d3342", lambda: agregar_numero("0")),
        (".", 4, 2, 1, "#2d3342", lambda: agregar_numero(".")),
    ]

    for texto, fila, columna, colspan, color, comando in botones:
        fg_color = "#111" if texto == "=" else "white"

        boton = tk.Button(
            buttons_frame,
            text=texto,
            bg=color,
            fg=fg_color,
            font=("Arial", 18, "bold"),
            relief="flat",
            width=5,
            height=2,
            command=comando,
            cursor="hand2",
            activebackground=color,
            activeforeground=fg_color
        )
        boton.grid(
            row=fila,
            column=columna,
            columnspan=colspan,
            padx=6,
            pady=6,
            sticky="nsew"
        )

    for fila in range(5):
        buttons_frame.grid_rowconfigure(fila, weight=1)

    for columna in range(4):
        buttons_frame.grid_columnconfigure(columna, weight=1)


    # Contendor para los elementos del panel de análisis
    panel_analisis = tk.Frame(
        panel_principal,
        bg="#1a1d24",
        padx=20,
        pady=20
    )
    panel_analisis.pack(side="left", anchor="n")

    caja_analisis = tk.Text(
        panel_analisis,
        width=36,
        height=12,
        bg="#1a1d24",
        fg="#cfd6e6",
        bd=0,
        wrap="word",
        font=("Arial", 12),
        spacing3=8
    )
    caja_analisis.pack(fill="both", expand=True)

    caja_analisis.tag_configure("titulo", foreground="white", font=("Arial", 12, "bold"))
    caja_analisis.tag_configure("normal", foreground="#cfd6e6", font=("Arial", 12))

    limpiar_analisis()

    ventana.bind("<Key>", tecla_presionada)
    ventana.mainloop()


# Método para crear la ventana de bienvenida, solicitar el nombre del usuario e iniciar la calculadora
def main():
    global ventana_bienvenida, entrada_nombre, mensaje_error

    ventana_bienvenida = tk.Tk()
    ventana_bienvenida.title("Bienvenida")
    ventana_bienvenida.configure(bg="#0f1117")
    maximizar_ventana(ventana_bienvenida)

    contenedor_principal = tk.Frame(ventana_bienvenida, bg="#0f1117")
    contenedor_principal.pack(fill="both", expand=True)

    marco = tk.Frame(
        contenedor_principal,
        bg="#111318",
        padx=25,
        pady=25
    )
    marco.place(relx=0.5, rely=0.5, anchor="center")

    titulo = tk.Label(
        marco,
        text="Bienvenido",
        bg="#111318",
        fg="white",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=(0, 20))

    etiqueta = tk.Label(
        marco,
        text="Ingrese su nombre",
        bg="#111318",
        fg="#cfd6e6",
        font=("Arial", 11)
    )
    etiqueta.pack(anchor="w", pady=(0, 8))

    entrada_nombre = tk.Entry(
        marco,
        width=28,
        font=("Arial", 12),
        bd=0,
        bg="#1a1d24",
        fg="white",
        insertbackground="white"
    )
    entrada_nombre.pack(fill="x", ipady=8, pady=(0, 15))

    boton = tk.Button(
        marco,
        text="Continuar",
        bg="#9dbcf2",
        fg="#111",
        font=("Arial", 11, "bold"),
        relief="flat",
        command=iniciar_calculadora,
        cursor="hand2"
    )
    boton.pack(fill="x", ipady=8)

    mensaje_error = tk.Label(
        marco,
        text="",
        bg="#111318",
        fg="#d85b5b",
        font=("Arial", 10)
    )
    mensaje_error.pack(pady=(15, 0))

    ventana_bienvenida.bind("<Return>", iniciar_calculadora)
    ventana_bienvenida.mainloop()


main()