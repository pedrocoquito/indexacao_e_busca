from lista_encadeada import no_lista
import math

class no:
    def __init__ (self, p, pr):
        self.palavra = p
        self.prox = pr
        self.lista = None

def h(palavra, tamanho_tabela):
    valor_hash = 7
    for c in palavra:
        valor_hash = valor_hash * 31 + ord(c)
    return valor_hash%tamanho_tabela

def inserir(tabela, doc, doc_id): 
    tamanho = len(tabela)
    for p in doc:
        pos = h(p, tamanho)
        if tabela[pos] is None:
            tabela[pos] = no(p, None)
            termo = tabela[pos]
        else:
            termo = tabela[pos]
            while termo.prox is not None:
                if termo.palavra == p:
                    break
                else:
                    termo = termo.prox
            if termo.palavra != p:
                termo.prox = no(p, None)
                termo = termo.prox
        novo_item = no_lista(doc[p], doc_id, termo.lista)
        termo.lista = novo_item
    return tabela

def salvar_indice(tabela, lista_documentos):
    print('\n Salvando índice no arquivo \n')
    arquivo = open('indice_hash.txt', 'w')
    tamanho = len(tabela)
    arquivo.write(str(tamanho) + '\n')
    for i in range(0, tamanho):
        termo = tabela[i]
        numero_de_palavras = 0
        while termo is not None:
            numero_de_palavras += 1
            termo = termo.prox 
        arquivo.write(str(numero_de_palavras) + '\n')
        termo = tabela[i]
        while termo is not None:
            arquivo.write(termo.palavra + ' ')
            doc = termo.lista
            while doc is not None:
                arquivo.write(str(doc.count) + ' ' + str(doc.doc_id))
                doc = doc.prox
                if doc is not None:
                    arquivo.write(' ')
            arquivo.write('\n')
            termo = termo.prox
    quantidade = len(lista_documentos)
    arquivo.write(str(quantidade) + '\n')
    for i in range(0, quantidade):
        arquivo.write(lista_documentos[i][0] + '\n' + str(lista_documentos[i][1]) + '\n' + lista_documentos[i][2] + '\n')

def carregar_indice(): 
    print('Carregando arquivo...')
    arquivo = open("indice_hash.txt", 'r')
    tamanho_tabela = int(arquivo.readline())
    tabela = [None] * tamanho_tabela
    documentos = []
    for i in range (0, tamanho_tabela):
        numero_de_termos = int(arquivo.readline())
        for j in range (0, numero_de_termos):
            lista = arquivo.readline().split()
            tabela[i] = no(lista[0], tabela[i])
            tamanho_lista = len(lista)
            for k in range (1, tamanho_lista, 2):
                tabela[i].lista = no_lista(int(lista[k]), int(lista[k+1]), tabela[i].lista)
    numero_de_documentos = int(arquivo.readline())
    for i in range (0, numero_de_documentos):
        endereco = arquivo.readline()
        termos_distintos = int(arquivo.readline())
        titulo_resumo = arquivo.readline()
        documentos.append((endereco, termos_distintos, titulo_resumo))
    return tabela, documentos

def busca(tabela, documentos, busca): 
    tamanho = len(tabela)
    relevancia = dict()
    for termo in busca:
        contador = 0
        ponteiro = tabela[h(termo, tamanho)]
        while ponteiro is not None:
            if ponteiro.palavra == termo:
                break
            ponteiro = ponteiro.prox
        if ponteiro is not None:
            doc = ponteiro.lista
            while doc is not None:
                contador += 1
                doc = doc.prox
            doc = ponteiro.lista
            while doc is not None:
                if doc.doc_id in relevancia:
                    relevancia[doc.doc_id] += doc.count/contador
                else:
                    relevancia[doc.doc_id] = doc.count/contador
                doc = doc.prox
    for doc in relevancia:
        relevancia[doc] *= math.log10(len(documentos))/documentos[doc][1]
    lista_documentos = sorted(relevancia.items(), key = lambda item: item[1])
    print('\n Resultados: \n')
    if len(lista_documentos) < 20:
        num_docs = len(lista_documentos)
    else:
        num_docs = 20
    for i in range (0, num_docs):
        print(str(i+1) + ' - ' + documentos[lista_documentos[i][0]][0] +'\n' + documentos[lista_documentos[i][0]][2])