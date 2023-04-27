import PySimpleGUI as sg
import requests
import datetime


requisicao = requests.get(f'https://api.exchangerate-api.com/v4/latest/BRL')
Moedas = requisicao.json()['rates']
ListaDeMoedas = list(Moedas)

sg.theme('dark grey 9')

layout = [
    [sg.Text('Valor: ', font='Verdana 11'), sg.Input(key="ValorOrigem", size=(13, 12)),sg.Text('Moeda de Origem: ', font='Verdana 11'), sg.Combo(
    ListaDeMoedas, size=(13, 9), default_value='BRL', key="moeda_origem"),
        sg.Text('Moeda Conversão: ', font='Verdana 11'), sg.Combo(ListaDeMoedas, size=(13, 9), default_value='USD', key="moeda_convertida")],
    [sg.Frame('Conversão', font='Verdana 13', expand_x=True, layout=[[sg.Multiline('', key='ConversaoOutput', s=(None, 5), expand_x=True, disabled=True)]])],
    [sg.Button('Converter', key="botão"), sg.Button('Limpar', key="clean"), sg.Button('Cancelar'), sg.Text('', key="logInfo", font='Verdana 11')],
]

window = sg.Window('Conversor de moedas', layout)
while True:
    event, values = window.read()
    if event == 'Cancelar' or event == sg.WIN_CLOSED:
        break
    if event == 'botão' and values['ValorOrigem'].strip() == '':
        sg.popup('Insira um valor para conversão.')
    elif not values['ValorOrigem'].isdigit():
        sg.popup('O valor deve conter somente números.')
    elif event == 'botão':
        Moedas = {k: v / Moedas[values["moeda_origem"]] for k, v in Moedas.items()}
        valor_convertido = float(values["ValorOrigem"]) * Moedas[values["moeda_convertida"]]
        valor_convertido = round(valor_convertido, 2)
        hora_atual = datetime.datetime.now().strftime("Data: %Y-%m-%d")
        output_message = f'Valor Convertido: {valor_convertido}\nConversão: {values["moeda_origem"]} Para: {values["moeda_convertida"]}\n{hora_atual}'
        window['ConversaoOutput'].update(value=output_message)
        valor_atual = round(Moedas[values["moeda_convertida"]], 2)
        window['logInfo'].update(value=f"1 {values['moeda_convertida']} = {valor_atual:.2f} {values['moeda_origem']}")
    elif event == 'clean':
        window['ConversaoOutput'].update(value='')
        window['logInfo'].update(value='')
