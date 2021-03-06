from Vertice import *

# Colocar grafo ponderado!
class Graph: 
    def __init__(self, **kwargs):
        self.__vertices = [] # Coloque a estrutura de dados aqui e no del!
        self.__verInd = []

        iteravel = kwargs.get("iteravel", None)
        self.__ponderado = kwargs.get("ponderado", False)
        self.__direcionado = kwargs.get("direcionado", False)
        self.__negativo = False

        if iteravel:
            if not self.ponderado:
                for i in iteravel:
                    if type(i).__name__ in ['tuple', 'list']:
                        for j in i[1:]: self.addAresta(i[0], j)
                    else: self.addVertice(i)
            else:
                for i in iteravel:
                    if type(i).__name__ in ['tuple', 'list']:
                        vertice, aresta, peso = i
                        self.addAresta(vertice, aresta, peso)
                    else: self.addVertice(i)

    def addVertice(self, vertice, aresta = None):
        if vertice not in self.verInd:
            self.vertices.append(Vertice(vertice))
            self.verInd.append(vertice)
        if aresta != None: self.addAresta(vertice, aresta)
    def addAresta(self, vertice, outro, peso = None):
        if vertice not in self.verInd:
            self.addVertice(vertice)
        if outro not in self.verInd:
            self.addVertice(outro)
        if not self.arestaDe(vertice, outro):
            if not self.ponderado: self.getVertice(vertice).append(self.getVertice(outro))
            else:
                if peso < 0: self.__negativo = True
                self.getVertice(vertice).append(self.getVertice(outro), peso)
        if not self.direcionado and not self.arestaDe(outro, vertice):
            if not self.ponderado: self.getVertice(outro).append(self.getVertice(vertice))
            else:
                self.getVertice(outro).append(self.getVertice(vertice), peso)

    def removeVertice(self, vertice):
        if vertice in self.verInd:
            objeto = self.getVertice(vertice)
            if not self.ponderado:
                for i in self.vertices:
                    if objeto in i.adjacentes:
                        i.adjacentes.remove(objeto)
            else:
                for i in self.vertices:
                    for j in range(len(i.adjacentes)):
                        if i[j][0] == objeto:
                            i.adjacentes.pop(j)
            self.vertices.remove(objeto)
            self.verInd.remove(vertice)
    def removeAresta(self, vertice, aresta):
        vertice = self.getVertice(vertice)
        aresta = self.getVertice(aresta)
        if vertice != None:
            vertice.remove(aresta)
        if not self.direcionado and aresta != None:
            aresta.remove(vertice)

    def arestaDe(self, vertice, aresta):
        if vertice in self.verInd:
            lista = self.getVertice(vertice).adjacentes
            if not self.ponderado:
                for i in lista:
                    if vertice == i.id: return True
            else:
                for i in range(len(lista)):
                    if vertice == lista[i][0].id: return True
        return False
    def getVertice(self, vertice):
        if vertice in self.verInd: return self.vertices[self.verInd.index(vertice)]
        else: return None

    def buscaEmLargura(self, vertice = None):
        if len(self.vertices) == 0:
            return []
        else:
            if vertice == None:
                vertice = self.vertices[0]
            visitados = []
            visitar = [vertice]
            for vertice in visitar:
                visitados.append(vertice) 
                for aresta in vertice.adjacentes:
                    if not self.ponderado:
                        if aresta not in visitar:
                            visitar.append(aresta)
                    else:
                        if aresta[0] not in visitar:
                            visitar.append(aresta[0])
            return [x.id for x in visitados]

    def buscaEmProfundidade(self, vertice = None):
        if len(self.vertices) == 0: return []
        if vertice == None:
            vertice = self.vertices[0]
        selecionados = []
        self.visita(vertice, selecionados)
        return [x.id for x in selecionados] 
    def visita(self, vertice, selecionados):
        selecionados.append(vertice)
        for i in vertice.adjacentes:
            if not self.ponderado:   
                if i not in selecionados:
                    self.visita(i, selecionados)
            else:
                if i[0] not in selecionados:
                    self.visita(i[0], selecionados)
        
    def dijkstra(self, origem): # Ele funciona com negativos psoakops
        if self.ponderado and type(origem).__name__ == "Vertice":
            relatorios = []
            visitar = [origem]
            anterior = {}
            pesos = {}

            for i in self.vertices:
                anterior[i] = None
                pesos[i] = float('inf')
            pesos[origem] = 0
            anterior[origem] = origem

            for i in visitar:
                for j in i.adjacentes:
                    if j[0] not in visitar:
                        visitar.append(j[0])    
                    novo = pesos[i] + j[1]
                    if pesos[j[0]] > novo:
                        anterior[j[0]] = i
                        pesos[j[0]] = novo
                relatorios.append((i,anterior.copy()))
            return relatorios # Todos os passos, se devolver anterior será o resultado.

    def bellmanFord(self, origem):
        if self.ponderado and type(origem).__name__ == "Vertice":
            relatorios = []
            vertices = [origem] + [x for x in self.vertices if x != origem]
            anterior = {}
            dist = {}

            for i in self.vertices:
                anterior[i] = None
                dist[i] = float('inf')
            dist[origem] = 0
            anterior[origem] = origem

            i = 0
            antigo = {}
            while anterior != antigo:
                antigo = anterior.copy()
                for vertice in vertices:
                    if anterior[vertice] != None:
                        for aresta in vertice.adjacentes:
                            old = dist[aresta[0]]
                            dist[aresta[0]] = min([old, dist[vertice] + aresta[1]])
                            if old != dist[aresta[0]]:
                                anterior[aresta[0]] = vertice
                if i != 0: relatorios.append((i, anterior.copy()))
                i += 1
            return relatorios

    def prim(self, vertice):
        if self.ponderado and type(vertice).__name__ == 'Vertice' and not self.direcionado:
            relatorios = []
            visitar = [vertice] # Todos os que precisam visitar.
            arestas = []
            pesos = {vertice:(vertice, 0, vertice)} # Resultado de todas as pesos.

            for ver in visitar:
                for aresta in ver.adjacentes:
                    if aresta[0] not in visitar: visitar.append(aresta[0])
            for i in visitar:
                if i not in pesos: pesos[i] = (Vertice(), float('inf'), Vertice())
            visitar = [vertice]
            cont = 0
            antigo = {}
            while antigo != pesos:
                antigo = pesos.copy()
                for j in range(cont, len(visitar)): # Adiciona novas arestas
                    for i in visitar[j].adjacentes:
                        objeto = (i[0], i[1], visitar[j])
                        if objeto not in arestas:
                            arestas.append(objeto)
                    cont += 1
                arestas = self.minimo(arestas)
                while arestas != []:
                    if arestas[0][1] < pesos[arestas[0][0]][1] and arestas[0][0] != pesos[arestas[0][2]][2]:
                        pesos[arestas[0][0]] = arestas[0]
                        if pesos[arestas[0][0]][0] not in visitar:
                            visitar.append(pesos[arestas[0][0]][0])
                        relatorios.append(pesos[arestas[0][0]])
                        break
                    arestas.pop(0)
                    arestas = self.minimo(arestas)
            return relatorios
                
    def minimo(self, lista):
        for i in range(len(lista)):
            if lista[i][1] < lista[0][1]:
                lista[0], lista[i] = lista[i], lista[0]
        return lista

    def kruskal(self, vertice = None):
        if self.ponderado and not self.direcionado:
            relatorios = []
            arestas = [] # Todas as arestas
            if vertice == None: vertice = self.vertices[0]
            vertices = [vertice]
            pesos = {} 

            # Caso for disconexo
            for ver in vertices:
                for aresta in ver.adjacentes:
                    if aresta[0] not in vertices: vertices.append(aresta[0])

            for i in vertices: # Pega todas as arestas
                for j in i.adjacentes:
                    if j + (i,) not in arestas and (i, j[1], j[0]) not in arestas:
                        arestas.append(j + (i,))
            
            while len(pesos) != len(vertices) and arestas != []:
                arestas = self.minimo(arestas)
                menor = arestas.pop(0)
                if menor[0] not in pesos:
                    relatorios.append(menor)
                    pesos[menor[0]] = menor
                elif menor[2] not in pesos: # Vai que né...
                    relatorios.append(menor)
                    pesos[menor[2]] = menor
            
            return relatorios

    def isDirecionado(self): return self.direcionado
    def isPonderado(self): return self.ponderado
    def __getitem__(self, item):
        for i in self.vertices:
            if i.id == item:
                return i
    def __str__(self): return '\n'.join([str(x) for x in self.vertices])
    def __repr__(self): 
        referenciados = []
        string = 'iteravel = ['
        for x in self.vertices:
            if len(x.adjacentes) != 0:
                string += "(" + str(x.id)
                for y in x.adjacentes:
                    referenciados.append(y.id)
                    string += ', ' + str(y.id)
                string += "), "
            elif x.id not in referenciados:
                string += str(x.id) + ", "
            referenciados.append(x.id)
        string = string[:-2] + '], '
        string += "ponderado = True, " if self.ponderado else ''
        string += 'direcionado = True' if self.direcionado else ''
        return "Graph(" + string[:-2] + ")"

    def getVertices(self): return self.__vertices
    vertices = property(getVertices, )

    def getVerInd(self): return self.__verInd
    verInd = property(getVerInd, )

    def getDirecionado(self): return self.__direcionado
    def setDirecionado(self, novo): 
        if type(novo).__name__ == 'bool': self.__direcionado = novo
    direcionado = property(getDirecionado, setDirecionado, )

    def getPonderado(self): return self.__ponderado
    ponderado = property(getPonderado, )
    
    def getNegativo(self): return self.__negativo
    negativo = property(getNegativo, )

if __name__ == "__main__":
    """
    g = Graph(iteravel = [("A", "B", 2), ("A", "C", 3), ("A", "D", 3), ("B", "C", 4), ("B", "E", 3), ("C", "D", 5), ("C", "E", 1), ("D", "F", 7), ("E", "F", 8), ("F", "G", 9)], ponderado = True)
    menores = g.kruskal()
    for i in menores:
        print(f"{i.id} -- {menores[i][2].id} com peso {menores[i][1]}")
    """
    """
    g = Graph(iteravel = [("A", "B", 2), ("A", "C", 3), ("A", "D", 3), ("B", "C", 4), ("B", "E", 3), ("C", "D", 5), ("C", "E", 1), ("C", "F", 6) ("D", "F", 7), ("E", "F", 8), ("F", "G", 9)], ponderado = True)
    relatorio = g.prim(g.getVertice("A"))
    for i in relatorio:
        print(i)"""
    """
    g = Graph(iteravel = [(1, 2, -6), (2, 8, 8), (8, 7, 15), (8, 12, 11), (8, 9, 11), (2, 22, 1), (22, 1, 0)], ponderado = True, direcionado = True)
    lista = g.dijkstra(g.getVertice(1))
    for tuplas in lista:
        print(f"When was {tuplas[0].id}")
        dic = tuplas[1]
        for i in tuplas[1]:
            print(f"{i.id} : {dic[i] if dic[i] == None else dic[i].id}")
    
    print("\nBELLMAN\n")
    lista = g.bellmanFord(g.getVertice(1))
    for tuplas in lista:
        print(f"When was {tuplas[0]}")
        dic = tuplas[1]
        for i in tuplas[1]:
            print(f"{i.id} : {dic[i] if dic[i] == None else dic[i].id}")
    """