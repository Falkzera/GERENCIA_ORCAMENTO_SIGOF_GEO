Coletar via API, informações de novos processos

Coletar número desse processo e alocar em um visualizador de processos novos
Avisar necesisdae de preenchimento destes novos processos


-
Aba de resumo autoamtico com selectbox para selecionar o numero do processo e gerar o resumo.

-
Visualização gráfica / dashboard do executado (entender mais sobre)


-
Mostrar o usuario que cadastrou o processo
Quem foi que cadastrou o processo?
Quando cadastrou?
Quando alterou?
Quem alterou?
Quem removeu?
Quando removeu?

Editar processo será uma Aba especifica



modificar a logica do codigo a baixo, removendo a logica de implementacao atraves de uploader, e adicionadno apenas o dataframe com o nome:

(st.session_state.base)
no qual devera coletar o mesmo e selecionar a coluna N do Processo, colocando em um selectbox essa coluna, ao usuario selecionar o numero do processo, o mesmo deverá ser feito o resumo


-  Colocar   um background cores seplag





Para o calculo correto do limite, iria facilitar muito, se fosse preenchido um campo de "Entra no LIMITE?" SIM ou NÃO



para resetar qualquer valor use 
    if "base" in st.session_state:
        del st.session_state["base"]

