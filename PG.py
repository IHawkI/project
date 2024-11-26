import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset desde la URL
df = pd.read_csv('https://raw.githubusercontent.com/IHawkI/graficas/refs/heads/main/dflimpio')

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
st.title("Dashboard de Análisis de ventas de dispositivos electrónicos")

vista_general = st.sidebar.button("Vista General")
vista_filtrada = st.sidebar.button("Vista Filtrada")

if vista_general or not vista_filtrada:
    total_clientes = len(df)
    edad_promedio = f"{df['Age'].mean():.1f}"
    cantidad_promedio = f"{df['Quantity'].mean():,.2f}"
    promedio_accesorios = f"{(df['Add-on Total'].mean()):.2f}"

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
                <div class="metric-title">Cantidad de productos comprados promedio</div>
                <div class="metric-value">{cantidad_promedio}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Accesorios comprados promedio</div>
                <div class="metric-value">{promedio_accesorios}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        df.groupby('Loyalty Member')['Add-on Total'].sum().plot(kind='bar', ax=ax)
        plt.title('Relación entre Accesorios Comprados y Membresía de Lealtad')
        plt.xlabel('Membresía de Lealtad')
        plt.ylabel('Cantidad de Accesorios Comprados')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        
        colores_productos = {
            'Laptop': '#c60b1e',  
            'Smartphone': '#0055a4', 
            'Headphones': '#000000', 
            'Tablet': '#1A329d',
            'Smartwatch': '#410D2D',
            '0': '#FF0000'    
        }
        
        sns.countplot(data=df, x='Product Type', ax=ax, palette=colores_productos)
        ax.set_title("Distribución por Producto")
        ax.set_xlabel("")
        ax.set_ylabel("")

        ax.get_yaxis().set_visible(False)

        total = len(df)
        for patch in ax.patches:
            height = patch.get_height()
            percentage = (height / total) * 100
            ax.text(patch.get_x() + patch.get_width() / 2, height / 2,
                    f'{percentage:.1f}%', ha='center', va='center', fontsize=12, color='white')

        st.pyplot(fig)
    
    with col3:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x='Gender', ax=ax, palette={'Female': '#ff1493', 'Male': '#1e90ff', 'Not-specified': 'Grey'})
        ax.set_title("Distribución por Género")
        ax.set_xlabel("")
        ax.set_ylabel("")
        
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.get_yaxis().set_visible(False)

        for patch in ax.patches:
            height = patch.get_height()
            percentage = (height / total) * 100
            ax.text(patch.get_x() + patch.get_width() / 2, height / 2,
                    f'{percentage:.1f}%', ha='center', va='center', fontsize=14, color='white')

        st.pyplot(fig) 
    
    with col4:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(data=df, x='Payment Method', ax=ax, color='skyblue', edgecolor='black')
        ax.set_title("Distribución de Métodos de Pago", fontsize=14)
        ax.set_xlabel("Método de Pago")
        ax.set_ylabel("Cantidad")
        
        for patch in ax.patches:
            height = patch.get_height()
            percentage = (height / total) * 100
            ax.text(patch.get_x() + patch.get_width() / 2, height / 2,
                    f'{percentage:.1f}%', ha='center', va='center', fontsize=14, color='white')
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
        sns.countplot(data=df, x='Loyalty Member', ax=ax, palette="Set1")
        ax.set_title("Cantidad de clientes con membresía de lealtad")
        st.pyplot(fig)
    
    with col3:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x='Shipping Type', ax=ax, palette="Set2")
        ax.set_title("Tipo de transporte")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='center')
        st.pyplot(fig)
    
    with col4:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.histplot(data=df, x='Unit Price', ax=ax, kde=True, color='green')
        ax.set_title("Distribución del Precio Unitario")
        ax.set_xlabel("Precio Unitario")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

# Vista Filtrada
elif vista_filtrada:
    st.header("Vista Filtrada - Análisis Detallado")

    # Filtros en la barra lateral para la vista filtrada
    producto_seleccionado = st.sidebar.selectbox("Selecciona el producto", df['Product Type'].unique())
    genero_seleccionado = st.sidebar.selectbox("Selecciona el género", df['Gender'].unique())
    edad_seleccionada = st.sidebar.slider("Selecciona el rango de edad", 
                                          int(df['Age'].min()), 
                                          int(df['Age'].max()), 
                                          (int(df['Age'].min()), int(df['Age'].max())))

    # Filtrar el DataFrame con los criterios seleccionados
    df_filtrado = df[(df['Product Type'] == producto_seleccionado) & 
                     (df['Gender'] == genero_seleccionado) & 
                     (df['Age'] >= edad_seleccionada[0]) & 
                     (df['Age'] <= edad_seleccionada[1])]

    st.write(df_filtrado)