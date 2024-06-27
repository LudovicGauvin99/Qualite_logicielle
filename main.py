import os
import openai
import sys
import json
from github import Github

def main():
    # Récupération des variables d'environnement
    github_token = os.getenv('GITHUB_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai_api_model = os.getenv('OPENAI_API_MODEL', 'gpt-3.5-turbo')
    exclude_patterns = os.getenv('exclude', '**/*.json, **/*.md').split(',')

    # Initialisation des clients GitHub et OpenAI
    g = Github(github_token)
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    pr = repo.get_pull(int(os.getenv('GITHUB_REF').split('/')[-1]))

    # Récupération des diffs des commits
    diffs = []
    for file in pr.get_files():
        if any(file.filename.endswith(pattern) for pattern in exclude_patterns):
            continue
        diffs.append(file.patch)

    # Appel à l'API OpenAI pour analyser les diffs
    openai.api_key = openai_api_key
    prompt = "\n\n".join(diffs)
    response = openai.Completion.create(
        engine=openai_api_model,
        prompt=prompt,
        max_tokens=150
    )

    # Ajout des commentaires générés à la pull request
    comments = response.choices[0].text.strip()
    if comments:
        pr.create_issue_comment(comments)

if __name__ == "__main__":
    main()
