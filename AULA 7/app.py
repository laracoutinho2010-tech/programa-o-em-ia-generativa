import streamlit as st

# Título
st.title("Analisador de Reclamações")

# Campo para o usuário escrever
texto = st.text_area(
    "Digite as reclamações dos clientes:"
)

# Botão
if st.button("Analisar"):

    if texto.strip() == "":
        st.error("Digite uma reclamação antes de analisar.")

    else:
        # Deixa tudo em letras minúsculas
        texto = texto.lower()

        # Remove alguns sinais
        texto = texto.replace(".", "")
        texto = texto.replace(",", "")
        texto = texto.replace("!", "")
        texto = texto.replace("?", "")

        # Separa as palavras
        palavras = texto.split()

        # Dicionário para contar as palavras
        contador = {}

        for palavra in palavras:

            if palavra not in contador:
                contador[palavra] = 1
            else:
                contador[palavra] += 1

        # Ordena da maior para a menor frequência
        resultado = sorted(
            contador.items(),
            key=lambda item: item[1],
            reverse=True
        )

        st.subheader("Palavras mais frequentes")

        # Mostra as 10 primeiras
        for palavra, quantidade in resultado[:10]:
            st.write(
                "🔹", palavra, "-", quantidade, "vezes"
            )