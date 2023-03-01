import streamlit as st
import folium
from streamlit_folium import folium_static

# Define o usuário e senha padrão (para fins de teste)
username = "user"
password = "pass"

# Define o título do aplicativo
st.title("Mapas de teste")

# Define as opções de mapa
maps = {
    "Mapa de Curitiba": {
        "location": [-25.4284, -49.2733],
        "markers": [
            {"location": [-25.4375, -49.2654],
             "popup": "Universidade Federal do Paraná"},
            {"location": [-25.4425, -49.2377], "popup": "Jardim Botânico"},
            {"location": [-25.4216, -49.2632], "popup": "Ópera de Arame"},
            {"location": [-25.4289, -49.2727],
             "popup": "Pedreira Paulo Leminski"}
        ]
    },
    "Mapa de Itajaí": {
        "location": [-26.9097, -48.6616],
        "markers": [
            {"location": [-26.9187, -48.6559], "popup": "Marina Itajaí"},
            {"location": [-26.9866, -48.6317], "popup": "Praia Brava"},
            {"location": [-26.9111, -48.6629], "popup": "Mercado Público"},
            {"location": [-26.9074, -48.6614], "popup": "Teatro Municipal"}
        ]
    }
}


# Define a página de login
def login():
    st.subheader("Por favor, faça o login")
    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")
    if st.button("Login"):
        if user == username and pwd == password:
            st.session_state.is_authenticated = True
        else:
            st.error("Usuário ou senha incorretos")


# Define a página de logout
def logout():
    st.session_state.is_authenticated = False


# Verifica se o usuário está autenticado
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if not st.session_state.is_authenticated:
    login()
    st.stop()
else:
    st.write("Bem-vindo!")
    logout_button = st.button("Logout")
    if logout_button:
        logout()
        st.stop()


# Define a página que mostra os mapas
def maps_page():
    # Cria o widget de seleção de mapa
    choice = st.selectbox("Selecione um mapa", list(maps.keys()))

    # Define os parâmetros da nova página
    params = {"mapa": choice}

    # Redireciona o usuário para a nova página
    st.experimental_set_query_params(**params)

    # Define a página que mostra o mapa selecionado
    if "mapa" in st.experimental_get_query_params():
        choice = st.experimental_get_query_params()["mapa"][0]
        st.header(choice)
        m = folium.Map(location=maps[choice]["location"], zoom_start=12)

        # Adiciona os marcadores do mapa
        for marker in maps[choice]["markers"]:
            folium.Marker(
                location=marker["location"],
                popup=marker["popup"]
            ).add_to(m)

        # Renderiza o mapa
        folium_static(m)


# Define as opções do menu lateral
options = {
    "Mapa de teste": maps_page,
    "Mapa de teste 2": maps_page
}

# Define o título do menu lateral
st.sidebar.title("Menu")

# Cria o widget de seleção de opção
choice = st.sidebar.radio("Selecione uma opção", list(options.keys()))

# Executa a opção selecionada
options[choice]()
