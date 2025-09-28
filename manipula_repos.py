import requests, base64, yaml

class ManipulaRepositorio:

    def __init__(self, username, acess_token):
        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.acess_token = acess_token
        self.headers = {'Authorization': f'Bearer {self.acess_token}',
           'X-GitHub-Api-Version': '2022-11-28'
           }
        
    def cria_repo(self, nome_repo):
        data = {
            'name': nome_repo,
            'description':'Dados dos repositórios de algumas empresas',
            'private': False
        }

        response = requests.post(f"{self.api_base_url}/user/repos",
                                  json=data, headers=self.headers)
        
        print(f'status_code criação do repositório: {response.status_code}')

    def add_arquivo(self, nome_repo, caminho_arquivo):
        with open(caminho_arquivo, 'rb') as f:
            file_content = f.read()

        encoded_content = base64.b64encode(file_content)

        url = f'{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{caminho_arquivo}'
        data = {
            'message': 'Adicionando um novo arquivo',
            'content': encoded_content.decode('utf-8')
        }

        response = requests.put(url, json=data, headers=self.headers)

        print(f'status_code upload do arquivo: {response.status_code}')

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

acess_token = config['acess_token']

novo_repo = ManipulaRepositorio('michellvagner', acess_token)

nome_repo = 'linguagens-repositorios-empresas'
novo_repo.cria_repo(nome_repo)

novo_repo.add_arquivo(nome_repo, './dados/linguagens_amzn.csv')
novo_repo.add_arquivo(nome_repo, './dados/linguagens_netflix.csv')
novo_repo.add_arquivo(nome_repo, './dados/linguagens_spotify.csv')