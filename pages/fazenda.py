import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")

# Dados para visualização
data = pd.DataFrame(
    {
        "lat": [-21.837451728451956, -21.835367265852902],
        "lon": [-46.942263332259316, -46.953521598210884],
        "nome": ["Pivô 1", "Pivô 2"]
    }
)

try:
    ALL_LAYERS = {
        "Pivô": pdk.Layer(
            "ScatterplotLayer",  # Usei ScatterplotLayer para facilitar visualização
            data,
            get_position=["lon", "lat"],
            get_text=["nome"],
            get_fill_color=[200, 30, 0, 160],
            get_radius=400,
        ),

        "Nomes": pdk.Layer(
            "TextLayer",  # Usei ScatterplotLayer para facilitar visualização
            data,
            get_position=["lon", "lat"],
            get_text="nome",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'"
            
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
                    latitude=-21.84513567574486,
                    longitude=-46.93101373044637,
                    zoom=13,
                    pitch=50,
                ),
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")
except URLError as e:
    st.error(
        f"""
        **This demo requires internet access.**
        Connection error: {e.reason}
        """
    )
