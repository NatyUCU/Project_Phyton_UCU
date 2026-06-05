
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.info(
    "📊 Proyecto de Analítica de Datos - Exploración interactiva de egresos hospitalarios en Uruguay."
)
st.markdown("---")
st.title("🏥 Análisis de Egresos Hospitalarios en Uruguay")
st.markdown("""
Esta aplicación permite explorar los egresos hospitalarios de Uruguay
mediante filtros interactivos y visualizaciones dinámicas.
""")
st.markdown("---")

st.markdown("""
<style>

.main {
    background-color: #F5F9FC;
}

h1 {
    color: #1565C0;
}

h2 {
    color: #1976D2;
}

h3 {
    color: #1E88E5;
}

[data-testid="stSidebar"] {
    background-color: #E3F2FD;
}

</style>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd


df = pd.read_csv("data/processed/egresos_hospitalarios_limpio_GrupoC.csv")
st.write(df.columns)

st.write(df.head())

# Sidebar
st.sidebar.markdown("# Filtros")

st.sidebar.markdown(
    """
    Utilice los filtros para explorar los egresos hospitalarios.
    """
)

# Valores mínimo y máximo del año
min_año = int(df["AÑO"].min())
max_año = int(df["AÑO"].max())

# Slider
rango_años = st.sidebar.slider(
    "Seleccione rango de años",
    min_año,
    max_año,
    (min_año, max_año)
)

# Aplicar filtro
df_filtrado = df[
    (df["AÑO"] >= rango_años[0]) &
    (df["AÑO"] <= rango_años[1])
]

st.subheader("Datos filtrados")

st.dataframe(df_filtrado.head())
st.markdown("---")
# Frecuencia de egresos por diagnóstico
freq_diag = (
    df_filtrado
    .groupby("DIAGNOSTICO")
    .size()
    .reset_index(name="EGRESOS")
)
st.subheader("Indicadores Generales")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Egresos",
    len(df_filtrado)
)

col2.metric(
    "Diagnósticos",
    df_filtrado["DIAGNOSTICO"].nunique()
)

col3.metric(
    "Sectores",
    df_filtrado["SECTOR"].nunique()
)

col4.metric(
    "Regiones",
    df_filtrado["REGION"].nunique()
)
st.markdown("---")
st.subheader("Resumen Descriptivo")
# Calcular estadísticas

media = freq_diag["EGRESOS"].mean()

mediana = freq_diag["EGRESOS"].median()

desv_std = freq_diag["EGRESOS"].std()

rango = (
    freq_diag["EGRESOS"].max()
    - freq_diag["EGRESOS"].min()
)

q1 = freq_diag["EGRESOS"].quantile(0.25)

q2 = freq_diag["EGRESOS"].quantile(0.50)

q3 = freq_diag["EGRESOS"].quantile(0.75)
col1, col2, col3 = st.columns(3)

col1.metric(
    "Media",
    f"{media:.0f}"
)

col2.metric(
    "Mediana",
    f"{mediana:.0f}"
)

col3.metric(
    "Desv. Est.",
    f"{desv_std:.0f}"
)

col4, col5, col6, col7 = st.columns(4)

col4.metric("Rango", f"{rango:.0f}")
col5.metric("Q1", f"{q1:.0f}")
col6.metric("Q2", f"{q2:.0f}")
col7.metric("Q3", f"{q3:.0f}")
st.markdown("---")
st.subheader("Distribución de egresos por diagnóstico")

fig, ax = plt.subplots(figsize=(10,5))

sns.histplot(
    freq_diag["EGRESOS"],
    bins=20,
    kde=True,
    ax=ax
)

ax.set_title("Distribución de egresos")
ax.set_xlabel("Cantidad de egresos")
ax.set_ylabel("Frecuencia")

st.pyplot(fig)

freq_diag = freq_diag.sort_values(
    "EGRESOS"
).reset_index(drop=True)

freq_diag["RANK"] = range(
    1,
    len(freq_diag) + 1
)
st.markdown("---")
st.subheader("Dispersión de egresos por diagnóstico")

fig, ax = plt.subplots(figsize=(10,5))

sns.scatterplot(
    data=freq_diag,
    x="RANK",
    y="EGRESOS",
    ax=ax
)

ax.set_title(
    "Relación entre ranking y cantidad de egresos"
)

ax.set_xlabel(
    "Ranking de diagnósticos"
)

ax.set_ylabel(
    "Cantidad de egresos"
)

st.pyplot(fig)
st.markdown("---")
top_diag = (
    df_filtrado["DIAGNOSTICO"]
    .value_counts()
    .head(10)
)
st.subheader("Top 10 Diagnósticos")

fig, ax = plt.subplots(figsize=(10,6))

top_diag.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_xlabel("Cantidad de egresos")

st.pyplot(fig)
st.markdown("---")

region = (
    df_filtrado["REGION"]
    .value_counts()
)
fig, ax = plt.subplots(figsize=(8,5))

region.plot(
    kind="bar",
    ax=ax
)

st.pyplot(fig)
st.markdown("---")
genero = st.sidebar.multiselect(
    "Seleccione género",
    df["GENERO"].unique(),
    default=df["GENERO"].unique()
)
df_filtrado = df[
    (df["AÑO"] >= rango_años[0]) &
    (df["AÑO"] <= rango_años[1]) &
    (df["GENERO"].isin(genero))
]

st.markdown("---")

regiones_validas = sorted(
    df["REGION"]
    .dropna()
    .loc[df["REGION"] != "Sin Datos"]
    .unique()
)

region = st.sidebar.multiselect(
    "Seleccione región",
    regiones_validas,
    default=regiones_validas
)
(df["REGION"].isin(region))

st.subheader("Principales Hallazgos")
diag_top = (
    df_filtrado["DIAGNOSTICO"]
    .value_counts()
    .idxmax()
)
st.success(
    f"El diagnóstico más frecuente en los datos filtrados es: {diag_top}"
)
st.markdown("---")
st.subheader("📋 Conclusión")

st.markdown("""
Este dashboard interactivo permite explorar la información de egresos hospitalarios mediante filtros dinámicos y visualizaciones descriptivas.

A través del análisis realizado fue posible identificar patrones en la frecuencia de diagnósticos, observar la distribución de los egresos y analizar su comportamiento según los criterios seleccionados por la persona usuaria.

La herramienta constituye un apoyo para el análisis exploratorio de datos, facilitando la identificación de tendencias y características relevantes dentro del conjunto de información estudiado.
""")