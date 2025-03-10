# Javier Urrego Ojeda
# 9009598
# Project 1 - Parte B

class evaluar:
    
    def __init__(self, archivo):
        self.archivo = archivo
        self.formulas = []
        self.atomicos = []
        self.cargar()
        self.ejecutar()

    def cargar(self):    
        with open(self.archivo, "r") as file:
            lineas = file.readlines()

        s = int(lineas[0].strip())  
        i = 1

        while i <= s:
            self.formulas.append(lineas[i].strip())
            i += 1

        self.atomicos = self.extraer()

    def extraer(self):
        atomos = []
        i = 0
        while i < len(self.formulas):
            j = 0
            while j < len(self.formulas[i]):
                caracter = self.formulas[i][j]
                if "a" <= caracter <= "z" and caracter not in atomos:
                    atomos.append(caracter)
                j += 1
            i += 1
        return atomos

    def generar(self):

        valor = []
        
        total = 2 ** len(self.atomicos) 
        i = 0
        while i < total:
            valores = {}  
            j = 0
            while j < len(self.atomicos):
                if (i // (2 ** j)) % 2 == 0:
                    valores[self.atomicos[j]] = 0  
                else:
                    valores[self.atomicos[j]] = 1  
                j += 1
            valor.append(valores)
            i += 1

        return valor


    def evaluarF(self, formula, valores):
        pila = []
        operadores = []
        i = 0

        while i < len(formula):
            caracter = formula[i]

            if "a" <= caracter <= "z":
                pila.append(valores[caracter])

            else:
                if caracter == "!":
                    operadores.append(caracter)
                else:
                    if caracter in {"&", "|"}:
                        while operadores and operadores[-1] == "!":
                            valor = pila[-1]
                            pila[-1] = 1 if valor == 0 else 0
                            operadores.pop()
                        operadores.append(caracter)

                    elif caracter == "(":
                        operadores.append(caracter)

                    elif caracter == ")":
                        while operadores and operadores[-1] != "(":
                            operador = operadores.pop()

                            if operador == "!":
                                valor = pila[-1]
                                pila[-1] = 1 if valor == 0 else 0
                            else:
                                if len(pila) >= 2:
                                    b = pila.pop()
                                    a = pila.pop()
                                    if operador == "&":
                                        pila.append(1 if a == 1 and b == 1 else 0)
                                    elif operador == "|":
                                        pila.append(1 if a == 1 or b == 1 else 0)

                        if operadores and operadores[-1] == "(":
                            operadores.pop()

            i += 1

        while operadores:
            operador = operadores.pop()
            if operador == "!":
                valor = pila[-1]
                pila[-1] = 1 if valor == 0 else 0
            else:
                if len(pila) >= 2:
                    b = pila.pop()
                    a = pila.pop()
                    if operador == "&":
                        pila.append(1 if a == 1 and b == 1 else 0)
                    elif operador == "|":
                        pila.append(1 if a == 1 or b == 1 else 0)

        return pila[0] if pila else 0

    def det_tip(self, formula):
        valor = self.generar()
        resultados = []
        i = 0
        while i < len(valor):
            resultado = self.evaluarF(formula, valor[i])
            resultados.append(resultado)
            i += 1
        
        if all(res == 1 for res in resultados):
            return 1  #si es tautología
        if all(res == 0 for res in resultados):
            return 0  #si es contradicción
        return -1  #si es contingencia

    def ejecutar(self):
        resultados = []
        i = 0
        while i < len(self.formulas):
            resultado = self.det_tip(self.formulas[i])
            resultados.append(str(resultado))
            i += 1

        print("Resultados:", ", ".join(resultados))

evaluar("b.txt")
