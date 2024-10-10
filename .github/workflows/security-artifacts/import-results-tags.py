import requests

def get_all_findings(test_id, api_key, defectdojo_url):
    findings = []
    url = f"{defectdojo_url}/api/v2/findings/"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    params = {
        'test': test_id,
        'limit': 1000  # Define o limite máximo por página, você pode ajustar conforme necessário
    }

    while url:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        findings.extend(data['results'])
        url = data['next']  # Atualiza a URL para a próxima página

    return findings

def add_tag_to_findings(test_id, tags, api_key, defectdojo_url):
    findings = get_all_findings(test_id, api_key, defectdojo_url)
    for finding in findings:
        finding_id = finding['id']
        existing_tags = finding['tags']
        new_tags = list(set(existing_tags + tags))
        update_url = f"{defectdojo_url}/api/v2/findings/{finding_id}/"
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "tags": new_tags
        }
        update_response = requests.patch(update_url, headers=headers, json=data)
        if update_response.status_code == 200:
            print(f"Tag added to finding {finding_id}")
        else:
            print(f"Failed to update finding {finding_id}: {update_response.status_code}")

def upload_scan_to_defectdojo(file_path, scan_type, engagement_id, api_key, defectdojo_url, test_title, tags):
    url = f"{defectdojo_url}/api/v2/import-scan/"
    headers = {
        "Authorization": f"Token {api_key}"
    }
    files = {
        'file': open(file_path, 'rb')
    }
    data = {
        'scan_type': scan_type,
        'engagement': engagement_id,
        'test_title': test_title
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 201:
        print("Upload successful!")
        test_id = response.json()['test']
        add_tag_to_findings(test_id, tags, api_key, defectdojo_url)
    else:
        print(f"Failed to upload: {response.status_code}")
        print(response.json())

# Upload Semgrep
upload_scan_to_defectdojo(
    file_path='semgrep-report.json',
    scan_type='Semgrep JSON Report',
    engagement_id=1,
    api_key='3e2f18d5fae2b5ff203c19d75363d07162bbcc0c',
    defectdojo_url='http://localhost:8080',
    test_title='site',
    tags=['produtos-internos', 'auto-serviço']
)

# Upload Trivy
upload_scan_to_defectdojo(
    file_path='trivy-report.json',
    scan_type='Trivy Scan',
    engagement_id=1,
    api_key='3e2f18d5fae2b5ff203c19d75363d07162bbcc0c',
    defectdojo_url='http://localhost:8080',
    test_title='site',
    tags=['produtos-internos', 'auto-serviço']
)
