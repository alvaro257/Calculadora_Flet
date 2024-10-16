import flet as ft
from flet import colors
import re

# Variaveis globais
memoria = 0
recuperacao_memoria = False

def main(page: ft.Page):
    
    page.title = 'Calculadora'
    page.bgcolor = '#000'
    page.window.resizable = False
    page.window.maximizable = False
    page.window.width = 266
    page.window.height = 505
    
    # Display que exibe o resultado
    resultado = ft.Text(value = '', color = '#f5f6f7', size=20)
    display = ft.Row(
        width=266,
        controls=[resultado],
        alignment= 'end'
    )
    
    # Funcao para formatar o resultado, evitando valores terminados em .0
    def formatar_resultado(n):
        if n.is_integer():
            return str(int(n))
        else:
            return str(n)

    # Funcao responsavel por realizar todos os calculos
    def calcular(e):
        global memoria
        global recuperacao_memoria
        
        # Captura o botao selecionado a partir o event
        botao_selecionado = e.control.content.value
        
        # Substitui (ao inves de concatenar) a expressao pelo numero digitado após recuperacao memoria = True
        if recuperacao_memoria:
            resultado.value = botao_selecionado
            recuperacao_memoria = False
        else:
            resultado.value += botao_selecionado 
        resultado.update()
        
        # Sistema de memoria
        
        # Limpa a memoria
        if botao_selecionado == 'MC':
            memoria = 0
            resultado.value = ''
            resultado.update()
            print(memoria)
        
        # Recupera a memoria
        elif botao_selecionado == 'MR':
            recuperacao_memoria = True
            resultado.value = formatar_resultado(memoria)
            resultado.update()

        # Subtrai a memoria
        elif botao_selecionado == 'M-':
            resultado.value = resultado.value[:-2]
            resultado.update()
            if resultado.value == '':
                pass
            else:
                try:
                    memoria-= float(resultado.value)
                    resultado.value = ''
                    resultado.update()
                    print(memoria)
                except:
                    resultado.value = 'Erro'
                    resultado.update()
        
        # Adiciona a memoria
        elif botao_selecionado == 'M+':
            resultado.value = resultado.value[:-2]
            resultado.update()
            if resultado.value == '':
                pass
            else:
                try:
                    memoria+= float(resultado.value)
                    resultado.value = ''
                    resultado.update()
                    print(memoria)
                except:
                    resultado.value = 'Erro'
                    resultado.update()
        
        # Botao que limpa a expressao por completo
        elif botao_selecionado == 'C':
            resultado.value = ''
            resultado.update()

        # Botao que limpa a expressao de tras pra frente, caracter por caracter
        elif botao_selecionado == 'Del':
            resultado.value = resultado.value[:-4]
            resultado.update()
        
        # Resolve calculo de porcentagem
        elif botao_selecionado == '%':
            simbolo = re.search(r'[^.\d]', resultado.value).group()
            resultado.value = resultado.value[:-1]
            
            try:
                if simbolo == '%':
                    resultado.value = str(float(resultado.value) / 100)
                    resultado.update()
                elif simbolo == '(':
                    parentese = resultado.value.find('(')
                    numero = resultado.value[parentese+1:]
                    resultado.value = '(' + str(float(numero) / 100)
                    resultado.update()
                else:
                    posicao_simbolo = resultado.value.find(simbolo)
                    anterior = resultado.value[:posicao_simbolo]
                    sucessor = resultado.value[posicao_simbolo+1:]
                    
                    if simbolo == '+' or simbolo == '-':
                        resultado.value = anterior + simbolo + anterior + '*' + sucessor + '/100'
                    else:
                        resultado.value = anterior + simbolo + '(' + sucessor + '/100' + ')'
                    
                    resultado.value = formatar_resultado(eval(resultado.value))
                    resultado.update()
            except:
                resultado.value = 'Erro'
                resultado.update()
            
        # Resolve calculo de raiz2
        elif botao_selecionado == '√':
            resultado.value = resultado.value[:-1]
            if resultado.value:
                try:
                    numero = float(resultado.value)
                    if numero >= 0:
                        res = numero ** 0.5
                        resultado.value = str(formatar_resultado(res))
                        resultado.update()
                    else:
                        resultado.value = 'Erro'
                        resultado.update()
                except:
                    resultado.value = 'Erro'
                    resultado.update()
            else:
                resultado.value = '0'
                resultado.update()
            
        # Inverte o sinal do numero
        elif botao_selecionado == '±':
            resultado.value = resultado.value[:-1]
            if resultado.value.startswith('-'):
                resultado.value = resultado.value[1:]
            else:
                resultado.value = '-' + resultado.value
            resultado.update()

        # Calcula a expressao na tela apos selecionar =
        elif botao_selecionado == '=':
            resultado.value = resultado.value[:-1]
            
            # Resolve multiplicacao implicita de parenteses
            novo_valor = []
            for i in range(len(resultado.value)):
                if resultado.value[i] == '(' and i > 0:
                    if( resultado.value[i-1].isdigit() or resultado.value[i-1] == ')' ):
                        novo_valor.append('*')
                novo_valor.append(resultado.value[i])
            resultado.value = ''.join(novo_valor)
            
            # Substitui os simbolos invalidos e calcula a expressao formatada
            resultado.value = resultado.value.replace('x', '*').replace('÷', '/').replace('^', '**')
            try:
                resultado.value = eval(resultado.value)
                resultado.value = formatar_resultado(resultado.value)
                resultado.update()
            except:
                resultado.value = 'Erro'
                resultado.update()
    
    # Dicionario de botoes
    botoes = [
        {'value': 'MC', 'font': colors.BLACK, 'bg': colors.BLUE_GREY_100},
        {'value': 'MR', 'font': colors.BLACK, 'bg': colors.BLUE_GREY_100},
        {'value': 'M-', 'font': colors.BLACK, 'bg': colors.BLUE_GREY_100},
        {'value': 'M+', 'font': colors.BLACK, 'bg': colors.BLUE_GREY_100},
        {'value': 'C', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '(', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': ')', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': 'Del', 'font': colors.WHITE, 'bg': colors.ORANGE},
        {'value': '%', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '^', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '√', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '÷', 'font': colors.WHITE, 'bg': colors.ORANGE},
        {'value': '9', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '8', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '7', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': 'x', 'font': colors.WHITE, 'bg': colors.ORANGE},
        {'value': '6', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '5', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '4', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '-', 'font': colors.WHITE, 'bg': colors.ORANGE},
        {'value': '3', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '2', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '1', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '+', 'font': colors.WHITE, 'bg': colors.ORANGE},
        {'value': '±', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '0', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '.', 'font': colors.WHITE, 'bg': colors.WHITE12},
        {'value': '=', 'font': colors.WHITE, 'bg': colors.ORANGE}
    ]
    
    # Criando cada botao a partir do dicionario de botoes
    botao = [
        ft.Container(
        content=ft.Text(value=botao['value'], color = botao['font']),
        width=50,
        height=50,
        bgcolor= botao['bg'],
        border_radius= 100,
        alignment=ft.alignment.center,
        on_click = calcular
        ) for botao in botoes
    ]
    
    # Criando a linha que contem os botoes
    adicionar_botoes = ft.Row(
        width=300,
        wrap=True,
        controls=botao,
        alignment= 'end'
    )
    
    # Adicionando todos os elementos a tela
    page.add(display, adicionar_botoes)

ft.app(target = main)