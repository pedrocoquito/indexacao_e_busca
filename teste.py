from random_words import RandomWords
from leitor_json import indexar_arquivo
import math
import psutil
import time
import hash_table
import trie

#Este arquivo estão as funções de busca modificadas, sem a parte de "printar" os resultados para não ter o gasto da função print sendo calculado.

def busca_hashtable(tabela, documentos, busca):
    tamanho = len(tabela)
    relevancia = dict()
    for termo in busca:
        contador = 0
        ponteiro = tabela[hash_table.h(termo, tamanho)]
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

def busca_trie(raiz_arvore, documentos, busca):
    relevancia = dict()
    for termo in busca:
        contador = 0
        ponteiro = raiz_arvore
        tamanho_palavra = len(termo)
        for i in range (0, tamanho_palavra):
            ponteiro = ponteiro.lista_filhos[trie.indice(termo[i])]
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

def teste_trie():
    rw = RandomWords()
    arquivo = open('tempo_memoria_trie10k2.txt', 'w')
    memoria_usada = psutil.virtual_memory().used
    arvore, documentos = trie.carregar_indice()
    arquivo.write('Memória utilizada: '+str(psutil.virtual_memory().used - memoria_usada) + '\n')
    comeco = time.time()
    for i in range (0, 1000): 
        palavra = rw.random_word()
        if i%100 == 0:
            agora = time.time()
            arquivo.write(str(i)+' - '+str(agora - comeco) + '\n')
        busca_trie(arvore, documentos, palavra)
    final = time.time()
    arquivo.write('Tempo total: '+str(final - comeco))

def teste_hashtable():
    rw = RandomWords()
    arquivo = open('tempo_memoria_hash10k2.txt', 'w')
    memoria_usada = psutil.virtual_memory().used
    tabela, documentos = hash_table.carregar_indice()
    arquivo.write('Memória utilizada: '+str(psutil.virtual_memory().used - memoria_usada) + '\n')
    comeco = time.time()
    for i in range (0, 10000): 
        palavra = rw.random_word()
        palavra = palavra +' '+ rw.random_word()
        if i%1000 == 0:
            agora = time.time()
            arquivo.write(str(i)+' - '+ str(agora - comeco) + '\n')
        busca_hashtable(tabela, documentos, palavra)
    final = time.time()
    arquivo.write('Tempo total: '+str(final - comeco))

### As chamadas para função de teste estão comentadas para não haver risco de rodar (caso o programa rode pelo arquito teste.py) estas sem necessidade! ###

#teste_trie()
#teste_hashtable()






