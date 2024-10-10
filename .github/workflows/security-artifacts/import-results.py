import requests

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
        'test_title': test_title,
        'tags': tags
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 201:
        print("Upload successful!")
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
    test_title='internet-banking',
    tags='transações,banking'
)

# Upload Trivy
upload_scan_to_defectdojo(
    file_path='trivy-report.json',
    scan_type='Trivy Scan',
    engagement_id=1,
    api_key='3e2f18d5fae2b5ff203c19d75363d07162bbcc0c',
    defectdojo_url='http://localhost:8080',
    test_title='internet-banking',
    tags='transações,banking'
)
