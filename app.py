from shiny import App, ui, render, reactive
import pandas as pd

app_ui = ui.page_fluid(
    ui.h2("Sistema de Cálculo de Aluguel de Veículo"),

    ui.input_text("nome", "Nome do Carro:"),
    ui.input_text("modelo", "Modelo:"),
    ui.input_text("cor", "Cor:"),
    ui.input_text("placa", "Placa:"),
    ui.input_numeric("valor_diaria", "Valor da Diária (R$):", value=100),
    ui.input_numeric("valor_km", "Valor por KM Rodado (R$):", value=1),
    ui.input_numeric("kms_rodados", "Quilômetros Rodados:", value=0),
    ui.input_numeric("dias_alugados", "Dias Alugados:", value=1),

    ui.hr(),
    ui.output_table("tabela_resultado")
)

def server(input, output, session):
    @reactive.Calc
    def calcular():
        total_diarias = input.valor_diaria() * input.dias_alugados()
        total_kms = input.valor_km() * input.kms_rodados()
        total_geral = total_diarias + total_kms

        df = pd.DataFrame([{
            "Nome": input.nome(),
            "Modelo": input.modelo(),
            "Cor": input.cor(),
            "Placa": input.placa(),
            "Diária (R$)": f"{input.valor_diaria():.2f}",
            "Dias": input.dias_alugados(),
            "Total Diária (R$)": f"{total_diarias:.2f}",
            "Valor por KM (R$)": f"{input.valor_km():.2f}",
            "KM Rodados": input.kms_rodados(),
            "Total KM (R$)": f"{total_kms:.2f}",
            "Total Geral (R$)": f"{total_geral:.2f}"
        }])

        return df

    @output
    @render.table
    def tabela_resultado():
        return calcular()

app = App(app_ui, server)
