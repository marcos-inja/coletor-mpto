# coding: utf8
import sys
import os

from coleta import coleta_pb2 as Coleta

from headers_keys import (CONTRACHEQUE_JAN_MAY_2018,
                          INDENIZACOES_JAN_MAY_2018,
                          CONTRACHEQUE_JUN_FORWARD_2018,
                          INDENIZACOES_JUN_FORWARD_2018,
                          CONTRACHEQUE_APR_MAY_2019,
                          INDENIZACOES_APR_MAY_2019,
                          INDENIZAÇÕES_JUN_TO_AUG_2019,
                          CONTRACHEQUE_2020,
                          INDENIZACOES_2020,
                          CONTRACHEQUE_2021,
                          INDENIZACOES_2021, HEADERS)
import number


def parse_employees(fn, chave_coleta, categoria, base):
    employees = {}
    counter = 1
    for row in fn:
        matricula = str(row[base[0]])
        name = row[base[1]]
        function = str(row[base[2]])
        location = str(row[base[3]])
        
        if "TOTAL GERAL" in str(matricula):
            break

        if not number.is_nan(name) and not number.is_nan(matricula) and name != "0" \
           and (name != "Nome" and name != "NOME") and "Unnamed" not in name:
            membro = Coleta.ContraCheque()
            membro.id_contra_cheque = chave_coleta + "/" + str(counter)
            membro.chave_coleta = chave_coleta
            membro.matricula = matricula
            membro.nome = name
            membro.funcao = function
            membro.local_trabalho = location
            membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            membro.ativo = True
            
            membro.remuneracoes.CopyFrom(
                cria_remuneracao(row, categoria)
            )
          
            employees[matricula] = membro
            counter += 1
            
    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        # Caso o valor seja negativo, ele vai transformar em positivo:
        remuneracao.valor = float(abs(number.format_value(row[value])))

        if (categoria == CONTRACHEQUE_JAN_MAY_2018 \
            or categoria == CONTRACHEQUE_JUN_FORWARD_2018 \
            or categoria == CONTRACHEQUE_APR_MAY_2019
           ) and value in [11, 12, 13]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")

        elif categoria == CONTRACHEQUE_2020 and value in [16, 18, 20]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")

        elif categoria == CONTRACHEQUE_2021 and value in [15, 17, 19]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")  
        else: 
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")

        CONTRACHEQUE_JAN_MAY_2018
        CONTRACHEQUE_JUN_FORWARD_2018
        CONTRACHEQUE_APR_MAY_2019
        if (
            categoria == CONTRACHEQUE_JAN_MAY_2018 \
            or categoria == CONTRACHEQUE_JUN_FORWARD_2018 \
            or categoria == CONTRACHEQUE_APR_MAY_2019
           ) and value in [4]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        elif (
            categoria == CONTRACHEQUE_2020 \
            or categoria == CONTRACHEQUE_2021 
           ) and value in [6]:
           remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        remu_array.remuneracao.append(remuneracao)

    return remu_array


def update_employees(fn, employees, categoria, mat):
    for row in fn:
        matricula = str(row[mat])
        if matricula in employees.keys():
            emp = employees[matricula]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[matricula] = emp
    return employees


def parse(data, chave_coleta, month, year):
    employees = {}
    folha = Coleta.FolhaDePagamento()

    # Puts all parsed employees in the big map

    # 1 for January, 2 for February, 3 for March, 4 for April and 5 for May
    if year == "2018" and month in ["01", "02", "03", "04", "05"]:
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_JAN_MAY_2018, [1, 3, 5, 7]))
        update_employees(data.indenizatorias, employees, INDENIZACOES_JAN_MAY_2018, 1)

    elif (year == "2018" and month in ["06", "07", "08", "09", "10", "11", "12"]) or (
          year == "2019" and month in ["01", "02", "03"]
         ):
         employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_JUN_FORWARD_2018, [1, 3, 5, 7]))
         update_employees(data.indenizatorias, employees, INDENIZACOES_JUN_FORWARD_2018, 1)
    
    elif year == "2019" and month in ["04", "05"]:
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_APR_MAY_2019, [1, 2, 4, 6]))
        update_employees(data.indenizatorias, employees, INDENIZACOES_APR_MAY_2019, 1)

    elif year == "2019" and month in ["06", "07", "08"]:
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_2020, [0, 1, 3, 4]))
        update_employees(data.indenizatorias, employees, INDENIZAÇÕES_JUN_TO_AUG_2019, 0)
    elif year == "2021":
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_2021, [0, 1, 2, 3]))
        update_employees(data.indenizatorias, employees, INDENIZACOES_2021, 0)
    else:
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_2020, [0, 1, 2, 3]))
        update_employees(data.indenizatorias, employees, INDENIZACOES_2020, 0)


    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha
