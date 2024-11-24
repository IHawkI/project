import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
df = pd.read_csv('https://raw.githubusercontent.com/IHawkI/graficas/refs/heads/main/dflimpio')

# CSS para ampliar el ancho del contenido y mostrar las métricas en una sola fila
st.markdown("""
    <style>
    .main .block-container {
        max-width: 100%;
        padding-top: 0; /* Quitar el espacio superior */
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .metric-container {
        display: flex;
        justify-content: flex-start;
        gap: 20px;
        flex-wrap: nowrap; /* Evitar que se vayan a una segunda fila */
    }
    .metric-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-family: sans-serif;
        width: 220px; /* Ancho fijo para que ocupen una fila */
        text-align: left;
    }
    .metric-title {
        font-size: 1rem;
        color: #ffa500;
        font-weight: bold;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración del título del dashboard
st.title("Dashboard de Análisis de ventas de dispositivos electronicos")

# Botones en la barra lateral
vista_general = st.sidebar.button("Vista General")
vista_filtrada = st.sidebar.button("Vista Filtrada")

# Vista General
if vista_general or not vista_filtrada:
    # Cuadros de métricas personalizados en una sola fila
    total_clientes = len(df)
    edad_promedio = f"{df['Age'].mean():.1f}"
    rating_promedio = f"{df['Rating'].mean():,.2f}"
    Cantidad_promedio = f"{df['Quantity'].mean():,.2f}"

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-box">
                <div class="metric-title">Total de Clientes</div>
                <div class="metric-value">{total_clientes}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Edad Promedio</div>
                <div class="metric-value">{edad_promedio}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Rating Promedio</div>
                <div class="metric-value">{rating_promedio}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Accesorios promedio</div>
                <div class="metric-value">{Cantidad_promedio}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Gráficos distribuidos en dos filas y cuatro columnas, alineados a la izquierda
    # Primera fila de gráficos
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        # Gráfico de Score Crediticio con los ajustes solicitados
        fig, ax = plt.subplots(figsize=(6, 5))

        # Histograma con colores diferenciados

        # Líneas punteadas rojas y más gruesas en los límites
        ax.axvline(550, color='red', linestyle='--', linewidth=2)
        ax.axvline(750, color='red', linestyle='--', linewidth=2)

        # Calcular porcentaje en el rango y desplazar el cuadro de texto
        en_rango = len(df[(df['Quantity'] >= 550) & (df['Total Price'] <= 800)])
        porcentaje = (en_rango / len(df)) * 100
        ax.text(0.3, 0.9, f"{porcentaje:.2f}% en el rango", transform=ax.transAxes,
                fontsize=12, color='black', ha='center', va='top',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        
        # Configuración de etiquetas y título
        ax.set_title("Precio total")
        ax.set_xlabel("Total Price")
        ax.set_ylabel("")
        ax.set_xticks([400, 500, 550, 600, 650, 700, 750, 800])

        st.pyplot(fig)

    
    with col2:
        # Gráfico de "Distribución por País" con colores de bandera, sin marco
        fig, ax = plt.subplots(figsize=(2, 3))
        
        colores_productos ={
            'Laptop': '#c60b1e',  
            'Smartphone': '#0055a4', 
            'Headphones': '#000000', 
            'Tablet':'#1A329d',
            'Smartwatch': '#410D2D',
            '0': '#FF0000'    
        }
        
        sns.countplot(data=df, x='Product Type', ax=ax, palette=colores_productos)
        ax.set_title("Distribución por Producto")
        ax.set_xlabel("")
        ax.set_ylabel("")

        # Quitar el marco
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Eliminar los valores del eje y
        ax.get_yaxis().set_visible(False)

        # Calcular el porcentaje de cada barra y agregar el valor dentro de cada barra
        total = len(df)
        for patch in ax.patches:
            height = patch.get_height()
            percentage = (height / total) * 100
            ax.text(patch.get_x() + patch.get_width() / 2, height / 2,
                    f'{percentage:.1f}%', ha='center', va='center', fontsize=14, color='white')

        st.pyplot(fig)
    
    with col3:
    # Crear los datos para el gráfico de pastel
     gender_counts1 = df['Gender'].value_counts()
    labels = gender_counts1.index  # Etiquetas (géneros)
    sizes = gender_counts1.values  # Tamaños (frecuencias)

    # Colores personalizados
    colors = {'Female': '#ff1493', 'Male': '#1e90ff', 'Not-specifierd': 'grey'}
    pie_colors = [colors[label] for label in labels]

    # Crear el gráfico de pastel
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        sizes, 
        labels=labels, 
        colors=pie_colors, 
        autopct='%1.1f%%', 
        startangle=90, 
        wedgeprops={'edgecolor': 'white'}
        )
    ax.set_title("Distribución por Género", fontsize=16)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    
    with col4:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.histplot(df['Payment Method'], bins=30, kde=True, color="#3070b8", ax=ax)
        ax.set_title("Distribución de metodos de pago")
        st.pyplot(fig)

    # Segunda fila de gráficos
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x='Order Status', ax=ax, palette="Set2")
        ax.set_title("Estado del pedido")
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x='Loyalty Member', ax=ax, palette="Set2")
        ax.set_title("Cantidad de clientes con membresia de lealtad")
        st.pyplot(fig)
    
    with col4:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x='Payment Method', ax=ax, palette="Set2")
        ax.set_title("Metodo de pago de los clientes")
        st.pyplot(fig)

# Vista Filtrada
elif vista_filtrada:
    st.header("Vista Filtrada - Análisis Detallado")

    # Filtros en la barra lateral para la vista filtrada
    pais_seleccionado = st.sidebar.selectbox("Selecciona el producto", df['Product-Type'].unique())
    genero_seleccionado = st.sidebar.selectbox("Selecciona el género", df['Gender'].unique())
    edad_seleccionada = st.sidebar.slider("Selecciona el rango de edad", 
                                          int(df['Age'].min()), 
                                          int(df['Age'].max()), 
                                          (int(df['Age'].min()), int(df['Age'].max())))

    # Filtrar el DataFrame con los criterios seleccionados
    df_filtrado = df[(df['Product-Type'] == pais_seleccionado) & 
                     (df['Gender'] == genero_seleccionado) & 
                     (df['Age'] >= edad_seleccionada[0]) & 
                     (df['Age'] <= edad_seleccionada[1])]

    # Panel General de la Vista Filtrada
    st.subheader("Estadísticas Generales")
    st.metric("Total de Clientes", len(df_filtrado))
    st.metric("Edad Promedio", f"{df_filtrado['Age'].mean():.1f}")
    st.metric("Rating Promedio", f"${df_filtrado['Rating'].mean():,.2f}")
    st.metric("Accesorios comprados", f"{(1 - df_filtrado['Add-on Total'].mean()) * 100:.2f}%")