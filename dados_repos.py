import requests, yaml
import pandas as pd
from math import ceil

class DadosRepositorios:
    
    def __init__(self, owner, acess_token):
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.acess_token = acess_token
        self.headers = {'Authorization': f'Bearer {self.acess_token}',
           'X-GitHub-Api-Version': '2022-11-28'
           }
        
    def lista_repositorios(self):
        repos_list = []

        response = requests.get(f'https://api.github.com/users/{self.owner}', headers=self.headers)
        qtd_repo = ceil(response.json()['public_repos'] / 30)

        for page_num in range(1, qtd_repo + 1):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)

        return repos_list

    def nomes_repos(self, repos_list):
        repos_name = []

        for page in repos_list:
            for repo in page:
                try:
                    repos_name.append(repo['name'])
                except:
                    pass

        return repos_name
    
    def nomes_linguagens(self, repos_list):
        repos_language = []

        for page in repos_list:
            for repo in page:
                try:
                    repos_language.append(repo['language'])
                except:
                    pass 
        return repos_language
    
    def cria_df_linguagens(self):

        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        dados = pd.DataFrame()
        dados['repository_name'] = nomes 
        dados['language'] = linguagens

        return dados
    
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

acess_token = config['acess_token']
    
amazon_rep = DadosRepositorios('amzn', acess_token)
ling_mais_usadas_amzn = amazon_rep.cria_df_linguagens()

netflix_rep = DadosRepositorios('netflix', acess_token)
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagens()

spotify_rep = DadosRepositorios('spotify', acess_token)
ling_mais_usadas_spotify = spotify_rep.cria_df_linguagens()

#Salvar dados

ling_mais_usadas_amzn.to_csv('dados/linguagens_amzn.csv')
ling_mais_usadas_netflix.to_csv('dados/linguagens_netflix.csv')
ling_mais_usadas_spotify.to_csv('dados/linguagens_spotify.csv')