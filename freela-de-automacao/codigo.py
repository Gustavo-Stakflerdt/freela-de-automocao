# pandas -> bases de dados
# os -> arquivos do computador
# pywin32 -> enviar email
import os
from datetime import datetime
import pandas as pd
import win32com.client as win32

caminho = "bases"
arquivos = os.listdir(caminho)
print(arquivos)

tabela_consolidada = pd.DataFrame()

for nome_arquivo in arquivos:
    tabela_vendas = pd.read_csv(os.path.join(caminho, nome_arquivo))
    tabela_vendas["Data de Venda"] = pd.to_datetime("01/01/1900") + pd.to_timedelta(tabela_vendas["Data de Venda"],
                                                                                    unit="d")
    tabela_consolidada = pd.concat([tabela_consolidada, tabela_vendas])

tabela_consolidada = tabela_consolidada.sort_values(by="Data de Venda")
tabela_consolidada = tabela_consolidada.reset_index(drop=True)
tabela_consolidada.to_excel("Vendas.xlsx", index=False)

outlook = win32.Dispatch('outlook.application')
email = outlook.CreateItem(0)
email.To = "guthriller@gmail.com"
data_hoje = datetime.today().strftime("%d/%m/%Y")
email.Subject = f"Relatório de Vendas - {data_hoje}"
email.Body = f"""
Prezados,

Segue em anexo o Relatório de Vendas de {data_hoje} atualizado.
Qualquer coisa estou à disposição.
Abs,
Gustavo
"""

caminho = os.getcwd()
anexo = os.path.join(caminho, "Vendas.xlsx")
email.Attachments.Add(anexo)

email.Send()
