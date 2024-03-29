
import Levenshtein
from .nome import Nome

def distanciaString( nome0:str, nome1:str):
    """
    Aplica a função
    """
    return Levenshtein.distance( nome0 , nome1 )
def distanciaNome( nome0 , nome1 ):
    """
        Calcula a pontuação de 0 a 1.
        Verifica se tiver nomes iguais
    """
    flagNomeReduzido = False
    valor = 0
    if len( nome0.listNome ) > 1 and len( nome1.listNome ) > 1:
        #caso for maior que 1
        for apo0 in nome0.listNomeGrandes:
            for apo1 in nome1.listNomeGrandes:
                if esseNomesSaoIguais( apo0 , apo1 ) == True:
                    valor = casouUmNome( nome0, nome1, apo0, apo1 )
    else:
        #caso for menor que 1 ( nome unico ) 
        if existeNomeIgual( nome0.listNome, nome1.listNome ) == True:
            if len( nome0.listNome ) == 1 and len( nome1.listNome ) == 1:
                valor = 0.7
            else:
                valor = 0.3
    return valor

def esseNomesSaoIguais( nome0, nome1 ):
    """
    def usado para classificar se é a mesma função, pode ter um erro {0,1}<2
    """
    return distanciaString( nome0 , nome1 ) < 2

def casouUmNome(nome0, nome1, apo0, apo1):
    '''
    verica se existe uma forma de casamento
    '''

    listApo0 = nome0.listNome[:]
    listApo1 = nome1.listNome[:]

    listApo0.remove(apo0)
    listApo1.remove(apo1)

    # primeiro teste tem nome grande igual
    if existeNomeIgual( listApo0, listApo1 ) == True:
        return 1 # tem dois nomes iguais
    quant = quantidadePrimeiraLetraIgual( listApo0, listApo1 )
    if quant > 0:
        if quant == 1:
            return 0.6  # tem uma abreviasão igual
        else:
            return 0.8  # tem mais de uma

    return 0.1 # só um nome igual
def existeNomeIgual(lista0:list, lista1:list):
    '''
    Percore todos os nome e verifica se existe um grande com distancia menor que 2
    '''
    for nome0 in lista0:
        if len( nome0 ) > 1: # nome não unicio
            for nome1 in lista1:
                if len( nome1) > 1:
                    flag = esseNomesSaoIguais( nome0 , nome1 )
                    if flag == True:
                        return True
    return False
def quantidadePrimeiraLetraIgual( lista0:list, lista1:list):
    '''
    Percorre os nomes verificando se tem nome parecido
    '''
    cont = 0
    apoList1 = lista1[:]
    for nome0 in lista0:
        apo0 = nome0[0]
        for nome1 in apoList1:
            apo1 = nome1[0]
            if apo0 == apo1:
                cont += 1    
                apoList1.remove( nome1)
                break
    return cont

def nomeEstaNesseGrupo( nomeCompara, grupo ):
    nomeComparaBase = nomeCompara.base
    for nomeGrupo in grupo:
        if nomeComparaBase == nomeGrupo.base:
            return True
    return False


class CasamentoNome:
    def __init__(self):
        
        self.nomes = list()                 #lista da todos os nomes
        self.hashCasamento = dict()         #caso já classificou
        self.grupos = list()                #os diversos grupos

    def __julgando( self , nome ):
        """
            julga dando o melhor caso que tem armazenado
        """
       
        nomeBase = nome.base
        if nomeBase in self.hashCasamento.keys():
            index = self.hashCasamento[ nomeBase ]
            return [ index, 1 ]
        """
            Tenta encontrar o melhor caso entre os diversos pela média dos casos próximos
        """
        maximoLocal = -1     #indice do maior elemento
        valorMaximo = 0 #valor do indice maximo
        valor = 0       #valor para comparar

        for i in range( len( self.grupos ) ):
            grupo = self.grupos[ i ]
            
            #aplicando a média
            valor = 0
            for apoNome in grupo:
                apoSoma = distanciaNome( nome, apoNome )             
                valor += apoSoma
            valor = valor / len( grupo )
            # fim da média 

            if valor > valorMaximo: #trocando os valores pelos novos
                valorMaximo = valor     
                maximoLocal = i
        
        return [ maximoLocal, valorMaximo ]

    def julgandoAdicioandoPorObjNome( self, nome, parametro = 0.2 ):
        """
            Usado para adicionar elementos "Treino", os dados vao sendo adicionados com o tempo
            O método vai gerando "grupos" de nomes que tem como objetivo separar os diversos nomes
            O custo deve ser O(n), onde n é tamanho da quantidade nomes
        """
       
        apo = self.__julgando( nome )
        maximo = apo[ 0 ]
        valorMaximo = apo[ 1 ]

        if maximo == -1 or valorMaximo < parametro:
            """
                caso não passar o valor de parametro ele gera um novo grupo, ou seja,
                um novo nome, esse algoritmo é bem lento para adicionar nome novos.
            """
            maximo =  len( self.grupos )    
            nomeBase = nome.base
            self.hashCasamento[ nomeBase ] = maximo

            self.grupos.append( set() )
            self.grupos[ maximo ].add( nome )
        else:
            grupo = self.grupos[ maximo ]
            if nomeEstaNesseGrupo( nome , grupo ) == False:
                self.hashCasamento[ nome.base ] = maximo
                grupo.add( nome )
        return maximo

    def julgandoAdicioandoPorStr( self, nome:str, parametro = 0.2 ):
        """
            pega a string e já gera o objStr
        """
        apo = Nome( nome )
        return self.julgandoAdicioandoPorObjNome( apo , parametro)
        

    def julgandoPorObj( self , nome ):
        """
            retorna o grupo pelo nome
        """
        apo = self.__julgando( nome )
        return apo[ 0 ] 
    def julgandoPorStr( self, nome:str):
        """
            retorna o grupo pelo obj que foi gerado no momento
        """
        nomeApo = Nome( nome )
        apo = self.julgandoPorObj( nomeApo )
        return apo
    
    def getNome( self, index:int ):
        """
            Pega o maior nome do grupo apartir do id
        """
        grupo = self.grupos[ index ]
        maiorNome = ""
        for objNome in grupo:
            nomeBase = objNome.base
            if len( maiorNome ) < len( nomeBase ):
                maiorNome = nomeBase
        return maiorNome
    
    def getTodosOsNomes( self, index:int ):
        """
            Pega o maior nome do grupo apartir do id
        """
        grupo = self.grupos[ index ]
        maiorNome = "["
        for objNome in grupo:
            nomeBase = objNome.base
            #if len( maiorNome ) < len( nomeBase ):
            maiorNome += nomeBase + ";"
        return maiorNome.rstrip(";") + "]"