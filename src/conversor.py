from PIL import Image
from os import  listdir, remove, mkdir, path

def converter(arquivo, pasta_manga):
    """
    converte os arquivos em pdf
    """
    print("Convertendo...")
    if isinstance(arquivo, dict):
        for capitulo, imagens in arquivo.items():
            for imagem in range(len(imagens)):
                img = Image.open(f"{pasta_manga}/{imagens[imagem]}").convert("RGB")
                img.save(f"{pasta_manga}/{str(capitulo)}/{imagens[imagem]}.pdf")
        print("Convertido! Até mais.")

def separar_capitulos(paginas):
    """
    separa todos os capitulos do manga
    """
    print("Separando capitulos...")
    num_capitulos = set(list(map(lambda x: int(x.split("_")[0]), paginas)))
    capitulos = dict(map(lambda x: (str(x), [] ), num_capitulos))

    for pagina in paginas:
        num_pagina = int(pagina.split("_")[0])
        if num_pagina in num_capitulos:
            capitulos[str(num_pagina)].append(pagina)
    return capitulos

def criar_pastas_capitulos(capitulos, pasta_manga):
    """
    criar as pastas que irão conter os PDF's dos capitulos
    """
    print("Criando pastas para os capitulos...")
    list(map(lambda x: mkdir(f"{pasta_manga}/{str(x)}/"), capitulos.keys()))

def run(pasta_manga):
    #busca todas as imagens dentro da pasta informada
    print("Buscando imagens...")
    imagens = list(filter(lambda x: path.isfile(f"{pasta_manga}/{x}") if x else False, listdir(pasta_manga)))

    #coloca tudo na ordem correta
    print("Organizando...")
    imagens.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
    imagens.sort(key=lambda x: int(x.split("_")[0]))

    capitulos = separar_capitulos(imagens)
    criar_pastas_capitulos(capitulos, pasta_manga)
    converter(capitulos, pasta_manga)
