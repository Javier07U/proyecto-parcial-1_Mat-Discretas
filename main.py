# Javier Urrego Ojeda
# 9009598
# Project 1 - Parte A

class evaluador:
    
    def __init__(self, archivo):
        self.archivo = archivo
        self.valores = {}
        self.formulas = []
        self.cargar_datos()
        self.ejecutar()

    def cargar_datos(self):    
        with open(self.archivo, "r") as file:
            lineas = file.readlines()

        n = int(lineas[0].strip())  
        i = 1

        while i <= n:
            partes = lineas[i].strip().split()
            if len(partes) == 2 and partes[1] in {"0", "1"}:
                self.valores[partes[0]] = int(partes[1])
            i += 1

        s = int(lineas[i].strip())
        i += 1

        while i < len(lineas):
            self.formulas.append(lineas[i].strip())
            i += 1

    def eliminar_espacios(self, formula):
        resultado = ""
        i = 0
        while i < len(formula):
            if formula[i] != " ":
                resultado += formula[i]
            i += 1
        return resultado

    def evaluar_formula(self, formula):
        valores_temporales = self.valores.copy()
        pila_operandos = []
        pila_operadores = []
        i = 0

        while i < len(formula):
            caracter = formula[i]

            if caracter in valores_temporales:
                pila_operandos.append(valores_temporales[caracter])
            
            else:
                if caracter == "!":
                    pila_operadores.append(caracter)
                else:
                    if caracter in {"&", "|"}:
                        while (pila_operadores and pila_operadores[-1] == "!"):
                            valor = pila_operandos.pop()
                            pila_operandos.append(1 if valor == 0 else 0)
                            pila_operadores.pop()
                        pila_operadores.append(caracter)

                    elif caracter == "(":
                        pila_operadores.append(caracter)

                    elif caracter == ")":
                        while pila_operadores and pila_operadores[-1] != "(":
                            operador = pila_operadores.pop()
                            if operador == "!":
                                valor = pila_operandos.pop()
                                pila_operandos.append(1 if valor == 0 else 0)
                            else:
                                if len(pila_operandos) >= 2:
                                    b = pila_operandos.pop()
                                    a = pila_operandos.pop()
                                    if operador == "&":
                                        pila_operandos.append(1 if a == 1 and b == 1 else 0)
                                    elif operador == "|":
                                        pila_operandos.append(1 if a == 1 or b == 1 else 0)

                        if pila_operadores and pila_operadores[-1] == "(":
                            pila_operadores.pop()

            i += 1

        while pila_operadores:
            operador = pila_operadores.pop()
            if operador == "!":
                valor = pila_operandos.pop()
                pila_operandos.append(1 if valor == 0 else 0)
            else:
                if len(pila_operandos) >= 2:
                    b = pila_operandos.pop()
                    a = pila_operandos.pop()
                    if operador == "&":
                        pila_operandos.append(1 if a == 1 and b == 1 else 0)
                    elif operador == "|":
                        pila_operandos.append(1 if a == 1 or b == 1 else 0)

        return pila_operandos[0] if pila_operandos else 0  

    def ejecutar(self):
        resultados = []
        i = 0
        while i < len(self.formulas):
            formula = self.eliminar_espacios(self.formulas[i])
            resultado = self.evaluar_formula(formula)
            resultados.append(str(resultado))
            i += 1

        print("Resultados:", ", ".join(resultados))


evaluador("a.txt")
