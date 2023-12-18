from funcoes import criar_conexao_oracle, executar_query, buscar_xml, formatar_numero_serie
from dotenv import load_dotenv
from pathlib import Path
import os

def extrair_xml_blob(conexao, notas_para_buscar):
    resultados = []

    # Faz a consulta apenas se a linha contém uma nota válida.
    for nota in [nota for nota in notas_para_buscar if '/' in nota]:
        nro_nf, serie = formatar_numero_serie(nota)

        query = "SELECT NFE_PROC_XML, ID_TAG_NFE FROM CSF_OWN.NOTA_FISCAL WHERE NRO_NF = :nro_nf AND SERIE = :serie"

        try:
            resultado = executar_query(conexao, query, {'nro_nf': nro_nf, 'serie': serie})

            if resultado is None:
                print(f"Erro ao decodificar o XML da nota {nota}. Não foi possivel identificar o encoding correto.")
                continue

            conteudo_xml = resultado[0][0].read().decode('utf-8')
            chave_xml = resultado[0][1]
            resultados.append((nota, conteudo_xml, chave_xml))

        except Exception as e:
            print(f"Erro ao extrair XML do banco para a nota {nota}: {str(e)}")

    return resultados

def preencher_xml(conteudo_xml, numero_nota, chave, diretorio_destino):
    nome_arquivo = f"{chave}.xml"
    caminho_arquivo = diretorio_destino / nome_arquivo

    try:
        # Escreve os dados do XML no arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo_xml)

    except Exception as e:
        print(f"Erro ao escrever XML em arquivo para a nota {numero_nota}: {str(e)}")

diretorio_destino = Path('/mnt/c/Users/breno.lima/Downloads/pasta_para_receber_xml_movidos_pelo_python')
notas_para_buscar = buscar_xml('notas.txt')

total_notas = len(notas_para_buscar)
print(f'Total de notas: {total_notas}')

load_dotenv()

with criar_conexao_oracle(os.getenv("ORACLE_USUARIO"), os.getenv("ORACLE_SENHA"), os.getenv("ORACLE_TNS_NAME")) as conexao:
    resultados = extrair_xml_blob(conexao, notas_para_buscar)

    for nota, conteudo_xml, chave in resultados:
        preencher_xml(conteudo_xml, nota, chave, diretorio_destino)
