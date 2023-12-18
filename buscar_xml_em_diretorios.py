from funcoes import buscar_xml, formatar_numero_serie
from datetime import datetime
from pathlib import Path
import shutil

diretorio_origem = Path('/mnt/c/Users/breno.lima/Downloads')
diretorio_destino = Path(f'{diretorio_origem}/pasta_para_receber_xml_movidos_pelo_python')
notas_adicionadas = len(list(diretorio_destino.glob("*.xml")))

notas_para_buscar = buscar_xml('notas.txt')

total_notas = len(notas_para_buscar)
print(f'Total de notas: {total_notas}')

# Para cada XML dentro do diretório de origem:
for xml in diretorio_origem.rglob("*.xml"):
    if notas_adicionadas == total_notas:
        print('Todas as notas foram movidas.')
        break

    # Só vasculha arquivos com a data de modificação maior ou igual a definida anteriormente:
    if xml.stat().st_mtime >= datetime(2023, 11, 1).timestamp():
        # Abre o XML
        with open(xml, 'rb') as nota:
            # Lê o conteúdo
            conteudo_xml = nota.read().decode('utf-8')
            
            # Para cada linha em notas.txt:
            for nota in notas_para_buscar:
                numero_nota, serie = formatar_numero_serie(nota)
                # Se as tags de número da nota e série estão dentro do XML:
                if f'<nNF>{numero_nota}</nNF>' in conteudo_xml and f'<serie>{serie}</serie>' in conteudo_xml:
                    # Define o caminho do XML dentro da pasta de destino.
                    destino_arquivo = diretorio_destino / xml.name

                    # Se a nota ainda não está no diretório definido de destino, copia o XML para lá.
                    if not destino_arquivo.exists():
                        shutil.copy(xml, destino_arquivo)
                        print(f'Nota {nota[:-2]}/{nota[-1]} copiada para a pasta de destino.')
                        notas_adicionadas += 1