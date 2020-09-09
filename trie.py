from lista_encadeada import no_lista
import math

class no:
    def __init__ (self, p, l):
        self.caracter = p
        self.lista_filhos = [None] * 36
        self.lista = l
    
def indice(caracter):
    valor_ascii = ord(caracter)
    if valor_ascii < 97:
        return valor_ascii - 48
    return valor_ascii - 87

def inserir(raiz_arvore, doc, doc_id): 
    for p in doc:
        ponteiro = raiz_arvore
        for c in p:
            ind = indice(c)
            if ponteiro.lista_filhos[ind] is None:
                ponteiro.lista_filhos[ind] = no(c, None)
            ponteiro = ponteiro.lista_filhos[ind]
        novo_item = no_lista(doc[p], doc_id, ponteiro.lista)
        ponteiro.lista = novo_item
    return raiz_arvore

def arvore_para_lista(raiz_arvore):
    if raiz_arvore is None:
        return [('#', None)]
    lista = []
    lista.append((raiz_arvore.caracter, raiz_arvore.lista))
    for f in raiz_arvore.lista_filhos:
        lista.extend(arvore_para_lista(f))
    return lista

def lista_para_arvore(lista, pos):
    if pos[0] == len(lista):
        return None
    if lista[pos[0]][0] == '#':
        pos[0] += 1
        return None
    arvore = no(lista[pos[0]][0], lista[pos[0]][1])
    pos[0] += 1
    for i in range (0, 36):
        arvore.lista_filhos[i] = lista_para_arvore(lista, pos)
    return arvore

def salvar_indice(raiz_arvore, lista_documentos):
    print('\n Salvando índice no arquivo \n')
    arquivo = open('indice_trie.txt', 'w')
    lista = arvore_para_lista(raiz_arvore)
    arquivo.write(str(len(lista)) + '\n')
    for caracter, ponteiro in lista:
        arquivo.write(caracter)
        if ponteiro is not None:
            arquivo.write(' ')
        doc = ponteiro
        while doc is not None:
            arquivo.write(str(doc.count) +' '+ str(doc.doc_id))
            doc = doc.prox
            if doc is not None:
                arquivo.write(' ')
        arquivo.write('\n')
    quantidade = len(lista_documentos)
    arquivo.write(str(quantidade) + '\n')
    for i in range(0, quantidade):
        arquivo.write(lista_documentos[i][0] + '\n' + str(lista_documentos[i][1]) + '\n' + lista_documentos[i][2] + '\n')

def carregar_indice(): 
    print('Carregando arquivo...')
    arquivo = open("indice_trie.txt", 'r')
    quantidade_nos = int(arquivo.readline())
    lista = []
    documentos = []
    for i in range(0, quantidade_nos):
        linha = arquivo.readline().split()
        tamanho = len(linha)
        ponteiro = None
        if tamanho > 1:
            for j in range (1, tamanho, 2):
                ponteiro = no_lista(int(linha[j]), int(linha[j+1]), ponteiro)
        lista.append((linha[0], ponteiro))
    num_documentos = int(arquivo.readline())
    for i in range (0, num_documentos):
        endereco = arquivo.readline()
        termos_distintos = int(arquivo.readline())
        titulo_resumo = arquivo.readline()
        documentos.append((endereco, termos_distintos, titulo_resumo))
    return lista_para_arvore(lista, [0]), documentos

def busca(raiz_arvore, documentos, busca): 
    relevancia = dict()
    for termo in busca:
        contador = 0
        ponteiro = raiz_arvore
        tamanho_palavra = len(termo)
        for i in range (0, tamanho_palavra):
            ponteiro = ponteiro.lista_filhos[indice(termo[i])]
            if ponteiro is None:
                break
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
        print(str(i+1) + ' - ' + documentos[lista_documentos[i][0]][0] + '\n' + documentos[lista_documentos[i][0]][2])
        