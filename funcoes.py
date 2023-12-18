import cx_Oracle

# Função para criar uma conexão com o Oracle.
def criar_conexao_oracle(usuario, senha, tns_name):
    try:
        # Tenta estabelecer a conexão.
        conexao = cx_Oracle.connect(f'{usuario}/{senha}@{tns_name}')
        return conexao
    
    except cx_Oracle.Error as e:
        # Levanta uma exceção se houver um erro ao conectar.
        raise ValueError(f"Erro ao conectar ao Oracle: {e}")

# Função que irá executar o comando SQL.
def executar_query(conexao, query, params=None):
    try:
        cursor = conexao.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        resultado = cursor.fetchall()
        cursor.close()

        return resultado

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Erro ao executar a consulta: {error.code} - {error.message}")
        raise

# Função que cria uma lista com todas as notas.
def buscar_xml(lista_de_notas):
    with open(lista_de_notas, 'r') as notas_para_buscar:
        # Lê as notas do arquivo e remove espaços em branco.
        lista_de_notas = [linha.strip() for linha in notas_para_buscar]

    return lista_de_notas

def formatar_numero_serie(nota):
    nro_nf = nota[:-3] if '/' in nota[:-2] else nota[:-2]
    serie = nota[-2:] if '/' in nota[:-2] else nota[-1]
    
    return nro_nf, serie