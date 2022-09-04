#! /usr/bin/python3

# [X] add this to terminal aliases
# [X] Where am I?
# Look for images
# rename image with folder name
# extra: flag to run generate_entries?

from pathlib import Path
from helpers import is_img_ext

def try_renaming_first_image(path):
    nome_pasta = path.name
    itens_diretorio = sorted(path.iterdir())
    # Procura imagens no diretório corrente
    imagens = [item for item in itens_diretorio
                if item.is_file() and is_img_ext(item.name)]
    # Imagens boas são as que tem o mesmo nome da pasta!
    imagens_boas = [path_imagem for path_imagem in imagens
                    if path_imagem.name.startswith(nome_pasta)]
    if imagens_boas:
        print('Não precisei fazer nada!')
    elif imagens:
        # vai renomear a primeira para ficar com o nome da pasta
        primeira_imagem = imagens[0]  
        ext = primeira_imagem.name.split('.')[-1]
        novo_nome = nome_pasta + '.' + ext
        primeira_imagem.rename(novo_nome)
        print(primeira_imagem.name + ' -> ' + novo_nome)
    else:
        print('Não encontrei imagens!')

path = Path.cwd()
try_renaming_first_image(path)

