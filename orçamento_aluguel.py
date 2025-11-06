import csv

def solicitar_dados_cliente():
    """
    Coleta as informações do cliente de forma interativa e validada.
    """
    print("=============================================")
    print("==   Gerador de Orçamento de Aluguel   ==")
    print("=============================================\n")

    dados = {}

    while True:
        try:
            tipo = int(input(
                "Escolha o tipo de locação:\n"
                "1 - Apartamento (R$ 700,00 / 1 Quarto)\n"
                "2 - Casa (R$ 900,00 / 1 Quarto)\n"
                "3 - Estúdio (R$ 1.200,00)\n"
                "Opção: "
            ))
            if tipo in [1, 2, 3]:
                dados['tipo_imovel'] = tipo
                break
            else:
                print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    if dados['tipo_imovel'] in [1, 2]: 
        while True:
            quartos_str = input("Deseja com 2 quartos? (s/n): ").lower()
            if quartos_str in ['s', 'n']:
                dados['dois_quartos'] = (quartos_str == 's')
                break
            else:
                print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")
        
        while True:
            garagem_str = input("Deseja incluir vaga de garagem? (s/n): ").lower()
            if garagem_str in ['s', 'n']:
                dados['garagem'] = (garagem_str == 's')
                break
            else:
                print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

        if dados['tipo_imovel'] == 1: 
            while True:
                criancas_str = input("Possui crianças? (s/n): ").lower()
                if criancas_str in ['s', 'n']:
                    dados['tem_criancas'] = (criancas_str == 's')
                    break
                else:
                    print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

    elif dados['tipo_imovel'] == 3: 
        dados['vagas_estudio'] = 0
        while True:
            estacionamento_str = input("Deseja incluir 2 vagas de estacionamento por R$ 250,00? (s/n): ").lower()
            if estacionamento_str in ['s', 'n']:
                if estacionamento_str == 's':
                    dados['vagas_estudio'] = 2
                    while True:
                        vagas_extra_str = input("Deseja adicionar mais vagas por R$ 60,00 cada? Se sim, digite a quantidade. Se não, digite 0: ")
                        try:
                            vagas_adicionais = int(vagas_extra_str)
                            if vagas_adicionais >= 0:
                                dados['vagas_extra'] = vagas_adicionais
                                break
                            else:
                                print("Por favor, digite um número positivo ou zero.")
                        except ValueError:
                            print("Entrada inválida. Por favor, digite um número.")
                else:
                    dados['vagas_extra'] = 0
                break
            else:
                print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

    while True:
        try:
            parcelas = int(input("\nO valor do contrato é de R$ 2.000,00. Em quantas vezes deseja parcelar? (1 a 5): "))
            if 1 <= parcelas <= 5:
                dados['parcelas_contrato'] = parcelas
                break
            else:
                print("Número de parcelas inválido. Por favor, escolha entre 1 e 5.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    return dados


def calcular_orcamento(dados_cliente):
    """
    Calcula o valor do aluguel mensal e do contrato com base nas escolhas do cliente.
    """
    aluguel_mensal = 0
    desconto_aplicado = 0.0

    if dados_cliente['tipo_imovel'] == 1:
        aluguel_mensal = 700.00
        if dados_cliente.get('dois_quartos', False):
            aluguel_mensal += 200.00
        
        if not dados_cliente.get('tem_criancas', False): 
            desconto_aplicado = aluguel_mensal * 0.05
            aluguel_mensal -= desconto_aplicado

        if dados_cliente.get('garagem', False):
            aluguel_mensal += 300.00
        
    elif dados_cliente['tipo_imovel'] == 2:
        aluguel_mensal = 900.00
        if dados_cliente.get('dois_quartos', False):
            aluguel_mensal += 250.00
        if dados_cliente.get('garagem', False):
            aluguel_mensal += 300.00

    elif dados_cliente['tipo_imovel'] == 3:
        aluguel_mensal = 1200.00
        if dados_cliente.get('vagas_estudio', 0) > 0:
            aluguel_mensal += 250.00
        if dados_cliente.get('vagas_extra', 0) > 0:
            aluguel_mensal += dados_cliente['vagas_extra'] * 60.00

    valor_contrato = 2000.00
    parcelas = dados_cliente['parcelas_contrato']
    valor_parcela_contrato = valor_contrato / parcelas

    return aluguel_mensal, valor_parcela_contrato, parcelas, desconto_aplicado

def apresentar_resultado(aluguel, parcela_contrato, num_parcelas, desconto):
    """
    Exibe o resultado do orçamento formatado na tela.
    """
    print("\n---------------------------------------------")
    print("---     ORÇAMENTO FINAL     ---")
    print("---------------------------------------------\n")
    
    if desconto > 0:
        print(f"Desconto de 5% (sem crianças) aplicado: - R$ {desconto:.2f}")

    print(f"Valor do Aluguel Mensal Orçado: R$ {aluguel:.2f}")
    print("\n--- Detalhes do Contrato Imobiliário ---")
    print(f"Valor Total do Contrato: R$ 2.000,00")
    print(f"Pagamento em {num_parcelas}x de R$ {parcela_contrato:.2f}")
    print("\n*Este valor será somado ao aluguel durante os primeiros meses.")
    print("---------------------------------------------")

def gerar_csv(aluguel, parcela_contrato, num_parcelas):
    """
    Gera um arquivo .csv com as 12 parcelas do orçamento.
    """
    nome_arquivo = "orcamento_aluguel.csv"
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            
            escritor.writerow(["Mês", "Valor da Parcela (R$)"])
            
            for mes in range(1, 13):
                if mes <= num_parcelas:
                    valor_total_mes = aluguel + parcela_contrato
                else:
                    valor_total_mes = aluguel
                
                valor_formatado_br = f"{valor_total_mes:.2f}".replace('.', ',')
                escritor.writerow([mes, valor_formatado_br])
        
        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso!")
        print("Ele contém o detalhamento das 12 parcelas do seu orçamento.")
        
    except IOError:
        print(f"Erro: Não foi possível escrever no arquivo '{nome_arquivo}'.")

def main():
    """
    Função principal que executa o fluxo do programa.
    """
    dados = solicitar_dados_cliente()
    aluguel_mensal, valor_parcela_contrato, num_parcelas_contrato, desconto = calcular_orcamento(dados)
    apresentar_resultado(aluguel_mensal, valor_parcela_contrato, num_parcelas_contrato, desconto)
    gerar_csv(aluguel_mensal, valor_parcela_contrato, num_parcelas_contrato)

if __name__ == "__main__":
    main()
