from shiny import App, ui, render, reactive
import pandas as pd

# CSS embutido
css_estiloso = """
<style>
    body {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        font-family: 'Segoe UI', sans-serif;
        color: #f0f0f0;
        margin: 0;
        padding: 20px;
    }

    h2 {
        text-align: center;
        color: #ffffff;
        text-shadow: 1px 1px 4px #000;
        margin-bottom: 30px;
    }

    label {
        font-weight: 600;
        font-size: 1rem;
        color: #e0e0e0;
    }

    .shiny-input-container {
        margin-bottom: 15px;
    }

    input[type="text"],
    input[type="number"] {
        width: 100%;
        padding: 10px;
        border-radius: 8px;
        border: none;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.3);
        background-color: #f9f9f9;
        color: #333;
        font-size: 0.95rem;
    }

    .form-group {
        margin-bottom: 20px;
    }

    hr {
        border-top: 2px solid #ffffff33;
        margin: 30px 0;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background-color: #ffffff;
        color: #333;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 12px rgba(0,0,0,0.3);
    }

    th, td {
        padding: 12px 16px;
        text-align: center;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #2a5298;
        color: #fff;
        font-weight: bold;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    tr:hover {
        background-color: #e9f5ff;
    }
</style>
"""

# Interface com CSS embutido
app_ui = ui.page_fluid(
    ui.HTML(css_estiloso),  # CSS incluso aqui
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

# Lógica do servidor
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

# Executar o app
app = App(app_ui, server)
