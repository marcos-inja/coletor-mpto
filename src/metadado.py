from coleta import coleta_pb2 as Coleta


def captura(month, year):
    metadado = Coleta.Metadados()
    metadado.nao_requer_login = True
    metadado.nao_requer_captcha = True
    """
    Cada planilha tem um código único de acesso
    """
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.RASPAGEM_DIFICULTADA
    metadado.extensao = Coleta.Metadados.Extensao.ODS
    metadado.estritamente_tabular = False
    metadado.tem_matricula = True
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.formato_consistente = True
    metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    """
    Nessa data ocorre uma mudança nos formatos das planilhas,
    tanto as de remunerações quando as indenizatorias.
    """
    if (year == 2018 and month == 6) \
       or (year == 2019 and month in [4, 6, 9]) \
       or (year == 2021 and month == 1):
        metadado.formato_consistente = False
        
    return metadado