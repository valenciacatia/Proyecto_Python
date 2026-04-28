import streamlit as st
import pandas as pd
import numpy as np

from libreria_funciones_proyecto1 import calcular_wacc
from libreria_clases_proyecto1 import ProyectoInversion



st.set_page_config(
    page_title="Trabajo Práctico Modulo 1 - Python Fundamentals",
    layout="wide"
)

st.sidebar.image("DMC.png", use_container_width=True)

st.sidebar.title("Menú principal")
pagina = st.sidebar.selectbox(
    "Selecciona una sección",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)


# =========================================================


if "movimientos" not in st.session_state:
    st.session_state.movimientos = []

if "productos" not in st.session_state:
    st.session_state.productos = []

if "historico_wacc" not in st.session_state:
    st.session_state.historico_wacc = []

if "proyectos" not in st.session_state:
    st.session_state.proyectos = []


# =========================================================
# HOME
# =========================================================

if pagina == "Home":
    st.title("Trabajo Práctico Modulo 1 - Aplicación en Streamlit")
    st.subheader("Módulo 1 - Python Fundamentals")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Datos de la Alumna")
        st.write("**Nombre completo:** Catia Maria Valencia Vilca")
        st.write("**Curso:** Especialización en Python for Analytics")
        st.write("**Módulo:** Python Fundamentals")
        st.write("**Año:** 2026")

    with col2:
        st.markdown("### Tecnologías utilizadas")
        st.write("- Python")
        st.write("- Streamlit")
        st.write("- Pandas")
        st.write("- NumPy")
        st.write("- Programación funcional")
        st.write("- Programación orientada a objetos")

    st.info("Usa el menú lateral para navegar entre los ejercicios.")



# =========================================================

elif pagina == "Ejercicio 1":
    st.title("Ejercicio 1 - Flujo de caja con listas")

    st.markdown("""
    En este ejercicio se registran movimientos financieros usando una lista.
    Cada movimiento puede ser un **Ingreso** o un **Gasto**.
    """)

    with st.form("form_movimiento"):
        concepto = st.text_input("Concepto del movimiento")
        tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
        valor = st.number_input("Valor", min_value=0.0, step=10.0)
        agregar = st.form_submit_button("Agregar movimiento")

    if agregar:
        if concepto.strip() == "":
            st.error("Debes ingresar un concepto.")
        elif valor <= 0:
            st.error("El valor debe ser mayor que cero.")
        else:
            st.session_state.movimientos.append({
                "Concepto": concepto,
                "Tipo": tipo,
                "Valor": valor
            })
            st.success("Movimiento agregado correctamente.")

    if len(st.session_state.movimientos) > 0:
        df_mov = pd.DataFrame(st.session_state.movimientos)

        ingresos = df_mov.loc[df_mov["Tipo"] == "Ingreso", "Valor"].sum()
        gastos = df_mov.loc[df_mov["Tipo"] == "Gasto", "Valor"].sum()
        saldo = ingresos - gastos

        st.markdown("### Movimientos registrados")
        st.dataframe(df_mov, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total ingresos", f"S/ {ingresos:,.2f}")
        col2.metric("Total gastos", f"S/ {gastos:,.2f}")
        col3.metric("Saldo final", f"S/ {saldo:,.2f}")

        if saldo >= 0:
            st.success("El flujo de caja está a favor.")
        else:
            st.error("El flujo de caja está en contra.")

        if st.button("Limpiar movimientos"):
            st.session_state.movimientos = []
            st.rerun()
    else:
        st.warning("Aún no hay movimientos registrados.")



# =========================================================

elif pagina == "Ejercicio 2":
    st.title("Ejercicio 2 - Registro con NumPy, arrays y DataFrame")

    st.markdown("""
    En este ejercicio se registran productos usando widgets.  
    La información se almacena y luego se convierte en un DataFrame.
    """)

    with st.form("form_producto"):
        nombre_producto = st.text_input("Nombre del producto")
        categoria = st.selectbox("Categoría", ["Tecnología", "Oficina", "Hogar", "Alimentos", "Otros"])
        precio = st.number_input("Precio unitario", min_value=0.0, step=1.0)
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        agregar_producto = st.form_submit_button("Agregar producto")

    if agregar_producto:
        if nombre_producto.strip() == "":
            st.error("Debes ingresar el nombre del producto.")
        elif precio <= 0:
            st.error("El precio debe ser mayor que cero.")
        else:
            total = precio * cantidad
            st.session_state.productos.append([
                nombre_producto,
                categoria,
                precio,
                cantidad,
                total
            ])
            st.success("Producto agregado correctamente.")

    if len(st.session_state.productos) > 0:
        array_productos = np.array(st.session_state.productos, dtype=object)

        df_productos = pd.DataFrame(
            array_productos,
            columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
        )

        st.markdown("### DataFrame actualizado")
        st.dataframe(df_productos, use_container_width=True)

        total_ventas = df_productos["Total"].astype(float).sum()
        st.metric("Total registrado", f"S/ {total_ventas:,.2f}")

        if st.button("Limpiar productos"):
            st.session_state.productos = []
            st.rerun()
    else:
        st.warning("Aún no hay productos registrados.")


# =========================================================

elif pagina == "Ejercicio 3":
    st.title("Ejercicio 3 - Uso de función externa")

    st.markdown("""
    En este ejercicio se utiliza la función **calcular_wacc()** desde la libreria externa
    `libreria_funciones_proyecto1.py`.

    El WACC representa el costo promedio ponderado de capital de una empresa o proyecto.
    """)

    funcion = st.selectbox("Función seleccionada", ["calcular_wacc"])

    with st.form("form_wacc"):
        deuda = st.number_input("Deuda", min_value=0.0, step=1000.0)
        patrimonio = st.number_input("Patrimonio", min_value=0.0, step=1000.0)
        costo_deuda_pct = st.number_input("Costo de deuda (%)", min_value=0.0, max_value=100.0, step=0.1)
        costo_patrimonio_pct = st.number_input("Costo de patrimonio (%)", min_value=0.0, max_value=100.0, step=0.1)
        impuesto_pct = st.number_input("Impuesto (%)", min_value=0.0, max_value=100.0, step=0.1)

        ejecutar = st.form_submit_button("Calcular WACC")

    if ejecutar:
        try:
            resultado = calcular_wacc(
                deuda=deuda,
                patrimonio=patrimonio,
                costo_deuda_pct=costo_deuda_pct,
                costo_patrimonio_pct=costo_patrimonio_pct,
                impuesto_pct=impuesto_pct
            )

            wacc = resultado["wacc_pct"]
            st.success(f"El WACC calculado es: {wacc:.2f}%")

            st.session_state.historico_wacc.append({
                "Función": funcion,
                "Deuda": deuda,
                "Patrimonio": patrimonio,
                "Costo deuda (%)": costo_deuda_pct,
                "Costo patrimonio (%)": costo_patrimonio_pct,
                "Impuesto (%)": impuesto_pct,
                "WACC (%)": wacc
            })

        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

    if len(st.session_state.historico_wacc) > 0:
        st.markdown("### Histórico de resultados")
        df_wacc = pd.DataFrame(st.session_state.historico_wacc)
        st.dataframe(df_wacc, use_container_width=True)

        if st.button("Limpiar histórico WACC"):
            st.session_state.historico_wacc = []
            st.rerun()


# =========================================================

elif pagina == "Ejercicio 4":
    st.title("Ejercicio 4 - Clase externa con CRUD")

    st.markdown("""
    En este ejercicio se utiliza la clase **ProyectoInversion** desde la libreria externa
    `libreria_clases_proyecto1.py`.

    Se implementan operaciones CRUD:
    - Crear
    - Leer
    - Actualizar
    - Eliminar
    """)

    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(
        ["Crear", "Leer", "Actualizar", "Eliminar"]
    )


    # -------------------------------
    with tab_crear:
        st.subheader("Crear proyecto de inversión")

        with st.form("form_crear_proyecto"):
            nombre_proyecto = st.text_input("Nombre del proyecto")
            inversion_inicial = st.number_input("Inversión inicial", min_value=0.0, step=1000.0)
            flujo_1 = st.number_input("Flujo año 1", step=1000.0)
            flujo_2 = st.number_input("Flujo año 2", step=1000.0)
            flujo_3 = st.number_input("Flujo año 3", step=1000.0)
            tasa_descuento_pct = st.number_input("Tasa de descuento (%)", min_value=0.0, max_value=100.0, step=0.1)

            crear = st.form_submit_button("Crear proyecto")

        if crear:
            try:
                if nombre_proyecto.strip() == "":
                    st.error("Debes ingresar el nombre del proyecto.")
                else:
                    flujos = [flujo_1, flujo_2, flujo_3]
                    
                    proyecto = ProyectoInversion(
                            nombre_proyecto=nombre_proyecto,
                            inversion_inicial=inversion_inicial,
                            flujos=flujos,
                            tasa_descuento_pct=tasa_descuento_pct
                        )

                    resumen = proyecto.resumen()

                    st.session_state.proyectos.append({
                        "Nombre": nombre_proyecto,
                       "Inversión inicial": inversion_inicial,
                        "Flujo año 1": flujo_1,
                        "Flujo año 2": flujo_2,
                        "Flujo año 3": flujo_3,
                        "Tasa descuento (%)": tasa_descuento_pct,
                        "VPN": resumen["vpn"],
                        "ROI (%)": resumen["roi_pct"],
                        "Payback años": resumen["payback_anios"],
                        "Decisión": resumen["decision"]
                    })

                    st.success("Proyecto creado correctamente.")
                    st.markdown("### Resultado del proyecto")

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric("VPN", f"{resumen['vpn']:.2f}")
                    col2.metric("ROI (%)", f"{resumen['roi_pct']:.2f}%")
                    col3.metric("Payback", f"{resumen['payback_anios']} años")
                    col4.metric("Decisión", resumen["decision"])
            except Exception as e:
                st.error(f"Error al crear proyecto: {e}")

    # -------------------------------
    with tab_leer:
        st.subheader(" Leer proyectos registrados")

        if len(st.session_state.proyectos) > 0:
            df_proyectos = pd.DataFrame(st.session_state.proyectos)
            st.dataframe(df_proyectos, use_container_width=True)
        else:
            st.warning("No hay proyectos registrados.")

 
    # -------------------------------
    with tab_actualizar:
        st.subheader("Actualizar proyecto")

        if len(st.session_state.proyectos) > 0:
            nombres = [p["Nombre"] for p in st.session_state.proyectos]
            proyecto_sel = st.selectbox("Selecciona el proyecto a actualizar", nombres)

            idx = nombres.index(proyecto_sel)
            proyecto_actual = st.session_state.proyectos[idx]

            with st.form("form_actualizar_proyecto"):
                nuevo_nombre = st.text_input("Nombre del proyecto", value=proyecto_actual["Nombre"])
                nueva_inversion = st.number_input("Inversión inicial", min_value=0.0, step=1000.0, value=float(proyecto_actual["Inversión inicial"]))
                nuevo_flujo_1 = st.number_input("Flujo año 1", step=1000.0, value=float(proyecto_actual["Flujo año 1"]))
                nuevo_flujo_2 = st.number_input("Flujo año 2", step=1000.0, value=float(proyecto_actual["Flujo año 2"]))
                nuevo_flujo_3 = st.number_input("Flujo año 3", step=1000.0, value=float(proyecto_actual["Flujo año 3"]))
                nueva_tasa = st.number_input("Tasa de descuento (%)", min_value=0.0, max_value=100.0, step=0.1, value=float(proyecto_actual["Tasa descuento (%)"]))

                actualizar = st.form_submit_button("Actualizar proyecto")

            if actualizar:
                try:
                    proyecto = ProyectoInversion(
                        nombre_proyecto=nuevo_nombre,
                        inversion_inicial=nueva_inversion,
                        flujos=[nuevo_flujo_1, nuevo_flujo_2, nuevo_flujo_3],
                        tasa_descuento_pct=nueva_tasa
                    )

                    resumen = proyecto.resumen()

                    st.session_state.proyectos[idx] = {
                        "Nombre": nuevo_nombre,
                        "Inversión inicial": nueva_inversion,
                        "Flujo año 1": nuevo_flujo_1,
                        "Flujo año 2": nuevo_flujo_2,
                        "Flujo año 3": nuevo_flujo_3,
                        "Tasa descuento (%)": nueva_tasa,
                        "VPN": resumen["vpn"],
                        "ROI (%)": resumen["roi_pct"],
                        "Payback años": resumen["payback_anios"],
                        "Decisión": resumen["decision"]
                    }

                    st.success("Proyecto actualizado correctamente.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error al actualizar proyecto: {e}")
        else:
            st.warning("No hay proyectos para actualizar.")

 
    # -------------------------------
    with tab_eliminar:
        st.subheader("Eliminar proyecto")

        if len(st.session_state.proyectos) > 0:
            nombres = [p["Nombre"] for p in st.session_state.proyectos]
            proyecto_eliminar = st.selectbox("Selecciona el proyecto a eliminar", nombres, key="eliminar_select")

            if st.button("Eliminar proyecto"):
                idx = nombres.index(proyecto_eliminar)
                st.session_state.proyectos.pop(idx)
                st.success("Proyecto eliminado correctamente.")
                st.rerun()
        else:
            st.warning("No hay proyectos para eliminar.")