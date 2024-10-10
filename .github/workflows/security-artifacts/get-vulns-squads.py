import requests
import argparse
from datetime import datetime, timedelta

base_url = 'http://localhost:8080/api/v2'
api_token = '3e2f18d5fae2b5ff203c19d75363d07162bbcc0c'
headers = {
    'Authorization': f'Token {api_token}',
    'Content-Type': 'application/json'
}

# Função para buscar findings filtrados por tags e data, com suporte a paginação
def get_findings_by_tag_and_date(tag):
    findings_url = f'{base_url}/findings/'
    findings = []
    params = {
        'tags': tag,
        'active': 'true',  # Filtra apenas findings ativos
        'limit': 1000,  # Define um limite alto para cada página
        'offset': 0  # Inicia o offset em 0
    }

    while True:
        try:
            # Fazendo a requisição GET à API
            response = requests.get(findings_url, headers=headers, params=params)
            # Verifica se a resposta foi bem-sucedida
            if response.status_code == 200:
                data = response.json()
                findings.extend(data['results'])
                
                # Verifica se há mais páginas de resultados
                if data['next']:
                    # Incrementa o offset para a próxima página
                    params['offset'] += params['limit']
                else:
                    break  # Sai do loop se não houver mais páginas
            else:
                print(f'Erro ao buscar findings: {response.status_code} - {response.text}')
                return None
        
        except Exception as e:
            print(f'Erro: {e}')
            return None

    return findings

# Função para exibir os findings e contagem de severidade
def display_findings_summary(findings, tag):
    if not findings:
        print("Nenhuma vulnerabilidade encontrada.")
        return

    severity_count = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}

    for finding in findings:
        severity = finding['severity']
        if severity in severity_count:
            severity_count[severity] += 1

    total_vulns = sum(severity_count.values())

    print(f"{tag.replace('-', ' ')} - {total_vulns} vulnerabilidades encontradas")

if __name__ == "__main__":

    print('')    
    # Busca os findings de produtos internos
    findings = get_findings_by_tag_and_date('transações')
    display_findings_summary(findings, '>> transações')

    # Busca os findings de transações
    findings = get_findings_by_tag_and_date('banking')
    display_findings_summary(findings, 'banking')

    # Busca os findings de transações
    findings = get_findings_by_tag_and_date('bnpl')
    display_findings_summary(findings, 'bnpl')

    print()

    findings = get_findings_by_tag_and_date('produtos-internos')
    display_findings_summary(findings, '>> produtos-internos')

    # Busca os findings de transações
    findings = get_findings_by_tag_and_date('sistemas')
    display_findings_summary(findings, 'sistemas')

    # Busca os findings de transações
    findings = get_findings_by_tag_and_date('auto-serviço')
    display_findings_summary(findings, 'auto-serviço')