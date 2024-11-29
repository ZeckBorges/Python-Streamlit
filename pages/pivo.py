import streamlit as st
import pydeck as pdk
import math

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Pivô Circular Dividido")
st.sidebar.header("Pivô Circular Dividido")

# Função para calcular pontos de uma circunferência
def generate_circle_points(center, radius, start_angle, end_angle, num_points=50):
    """Gera pontos de uma circunferência ou arco"""
    lat, lon = center
    points = []
    for i in range(num_points + 1):
        angle = math.radians(start_angle + (end_angle - start_angle) * i / num_points)
        points.append([
            lon + radius * math.cos(angle),  # Longitude
            lat + radius * math.sin(angle),  # Latitude
        ])
    return points

# Configuração do pivô
center = (-21.8365, -46.947)  # Centro do pivô (latitude, longitude)
radius = 0.01  # Raio do pivô em graus (aproximado)

# Gerar dois semicírculos
pivo_parte_1 = generate_circle_points(center, radius, 0, 180)  # Primeira metade
pivo_parte_2 = generate_circle_points(center, radius, 270, 360)  # Segunda metade
pivo_parte_3 = generate_circle_points(center, radius, 180, 270)

# Fechar os polígonos conectando ao centro
pivo_parte_1.append([center[1], center[0]])
pivo_parte_2.append([center[1], center[0]])
pivo_parte_3.append([center[1], center[0]])

try:
    ALL_LAYERS = {
        "Pivô Parte 1": pdk.Layer(
            "PolygonLayer",
            [{"coordinates": pivo_parte_1, "name": "Parte 1"}],
            get_polygon="coordinates",
            get_fill_color="[0, 128, 255, 100]",
            get_line_color="[0, 0, 0]",
            pickable=True,
        ),
        "Pivô Parte 2": pdk.Layer(
            "PolygonLayer",
            [{"coordinates": pivo_parte_2, "name": "Parte 2"}],
            get_polygon="coordinates",
            get_fill_color="[255, 128, 0, 100]",
            get_line_color="[0, 0, 0]",
            pickable=True,
        ),
        "Pivô Parte 3": pdk.Layer(
            "PolygonLayer",
            [{"coordinates": pivo_parte_3, "name": "Parte 3"}],
            get_polygon="coordinates",
            get_fill_color="[255, 128, 200, 100]",
            get_line_color="[0, 0, 0]",
            pickable=True,
        ),
    }

    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=pdk.ViewState(
                    latitude=center[0],
                    longitude=center[1],
                    zoom=14,
                    pitch=50,
                ),
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")
except Exception as e:
    st.error(f"An error occurred: {e}")
