import json
import string
import hash_table
import trie

tamanho_tabela = 10000

### Função responsável em tratas as informações do arquivo JSON e indexar de acordo com a estrutura selecionada e chamando a função salvar_indice
### será gerado um arquivo txt com os documentos indexados

def indexar_arquivo(escolha):
    if escolha == 1:
        tabela = [None] * tamanho_tabela
    else:
        arvore = trie.no('R', None)
    lista_documentos = []
    doc_id = 0
    arquivo = open('dataset.json', 'r')
    for item in arquivo:
        data = json.loads(item)
        conteudo = data['headline'] + ' ' + data['short_description']
        conteudo = conteudo.lower()
        conteudo = conteudo.translate(str.maketrans('áâãàäéêëíóõôöúüç', 'aaaaaeeeioooouuc'))
        novo_conteudo = ''
        for ch in conteudo:
            valor_ascii = ord(ch)
            if valor_ascii == 32 or (valor_ascii > 96 and valor_ascii < 123) or (valor_ascii > 47 and valor_ascii < 58):
                novo_conteudo += ch
        contagem = dict()
        for p in novo_conteudo.split():
            if p in contagem:
                contagem[p] += 1
            else:
                contagem[p] = 1
        lista_documentos.append((data['link'],  len(contagem), novo_conteudo))
        if escolha == 1:
            tabela = hash_table.inserir(tabela, contagem, doc_id)
        else:
            arvore = trie.inserir(arvore, contagem, doc_id)
        doc_id += 1
        if doc_id%1000 == 0:
            print('Número de documentos carregados ' + str(doc_id))
    if escolha == 1:
        hash_table.salvar_indice(tabela, lista_documentos)
    else:
        trie.salvar_indice(arvore, lista_documentos)
    