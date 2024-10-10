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

    print(f"{tag.capitalize()} - {total_vulns} vulnerabilidades encontradas")
    print(f"Críticas: {severity_count['Critical']}")
    print(f"Altas: {severity_count['High']}")
    print(f"Médias: {severity_count['Medium']}")
    print(f"Baixas: {severity_count['Low']}")

if __name__ == "__main__":
    # Configuração do argparse para receber a tag como parâmetro
    parser = argparse.ArgumentParser(description="Script para buscar e contar vulnerabilidades por tag.")
    parser.add_argument('tag', type=str, help="Tag para buscar vulnerabilidades")
    
    # Parse dos argumentos
    args = parser.parse_args()
    tag_to_search = args.tag
    
    # Busca os findings filtrados por tag
    findings = get_findings_by_tag_and_date(tag_to_search)
    display_findings_summary(findings, tag_to_search)
