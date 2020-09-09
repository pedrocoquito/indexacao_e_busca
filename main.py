from leitor_json import indexar_arquivo
import hash_table
import trie

### IMPORTANTE!
### PARA QUE O PROGRAMA EXECUTE SEM PROBLEMAS É NECESSÁRIO REALIZAR A INDEXAÇÃO OU QUE O ARQUIVO POSSUA O(S) ARQUIVOS:
### indice_hash.txt e/ou indice_trie.txt


# A função pode indexar um novo arquivo, dependendo da opção selecionada pelo usuário
# Após isso já será realizado o carregamento para memória do arquivo indexado e o usuário poderá efetuar buscas
def programa_principal(escolha): 
    if escolha == 1:
        tabela, documentos = hash_table.carregar_indice()
    else:
        arvore, documentos = trie.carregar_indice()
    while True:
        busca = input('\nDigite sua busca: (0 para sair) ')
        if busca == '0':
            break
        busca = busca.lower()
        busca = busca.translate(str.maketrans('áâãàäéêëíóõôöúüç', 'aaaaaeeeioooouuc'))
        nova_busca = ''
        for ch in busca:
            valor_ascii = ord(ch)
            if valor_ascii == 32 or (valor_ascii > 96 and valor_ascii < 123) or (valor_ascii > 47 and valor_ascii < 58):
                nova_busca += ch
        busca = nova_busca.split()
        if len(busca) > 2:
            print('\nErro! Digite no máximo 2 palavras!')
        else:
            if escolha == 1:
                hash_table.busca(tabela, documentos, busca)
            else:
                trie.busca(arvore, documentos, busca)
            
realizar_parser = int(input('Deseja indexar um novo arquivo? \n\nCaso sim, coloque o arquivo na pasta do programa (É importante que o arquivo tenha nome dataset de extensão json!) \n\nDigite 1 para sim \nDigite 2 para não \n\nEscolha:'))
escolha = int(input('Qual estrutura você deseja utilizar? \n\nDigite 1 para tabela de hash \nDigite 2 para trie \n\nEscolha:'))

if realizar_parser == 1:
    indexar_arquivo(escolha)

programa_principal(escolha)

