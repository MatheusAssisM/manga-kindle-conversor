from PIL import Image
from os import  listdir, remove, mkdir, path
from PyPDF2 import PdfFileMerger, PdfFileReader
from progress.bar import Bar


def converter_image_to_pdf(arquivo, pasta_manga):
    """
    converte os arquivos em pdf
    """
    if isinstance(arquivo, dict):
        with Bar('Convertendo imagem em PDF', max = len(arquivo.keys())) as bar:
            for capitulo, imagens in arquivo.items():
                for imagem in range(len(imagens)):
                    img = Image.open(f"{pasta_manga}/{imagens[imagem]}").convert("RGB")
                    img.save(f"{pasta_manga}/{str(capitulo)}/{imagens[imagem]}.pdf")
                bar.next()

def get_capitulos(paginas):
    """
    separa todos os capitulos do manga
    """
    num_capitulos = set(list(map(lambda x: x.split("_")[0], paginas)))
    capitulos = dict(map(lambda x: (str(x), [] ), num_capitulos))

    with Bar("Separando capítulos", max=len(paginas)) as bar:
        for pagina in paginas:
            num_pagina = pagina.split("_")[0]
            if num_pagina in num_capitulos:
                capitulos[str(num_pagina)].append(pagina)
            bar.next()
    return capitulos

def criar_pastas_capitulos(capitulos, pasta_manga):
    """
    criar as pastas que irão conter os PDF's dos capitulos
    """
    with Bar("Criando pastas para os capítulos", max=len(capitulos.keys())) as bar:
        def criar_pastas_by_item(x):
            mkdir(f"{pasta_manga}/{str(x)}/")
            bar.next()
        list(map(criar_pastas_by_item, capitulos.keys()))

def remover_imagens(pasta_manga):
    """
    Remove as imagens jpg
    """
    imagens = list(filter(
        lambda x: True if x.endswith(".jpg") else False, 
        listdir(pasta_manga)
        ))

    with Bar("Removendo imagens", max=len(imagens)) as bar:
        def remover_imagem(x):
            remove(f"{pasta_manga}/{x}")
            bar.next()

        list(map(remover_imagem,imagens))

def juntar_paginas_pdf(pasta_manga, /):
    """
    Junta todos os pdfs em um unico pdf
    """
    mergerPDF = PdfFileMerger()

    pastas_com_pdf = list(map(
        lambda x:  float(x) if "." in x else int(x), 
        listdir(pasta_manga)
        ))
    pastas_com_pdf.sort(key= lambda x: x)
    pastas_com_pdf = list(map(lambda x: str(x), pastas_com_pdf))

    with Bar('Juntando páginas', max=len(pastas_com_pdf)) as bar:
        for folder in pastas_com_pdf:
            sorted_pdfs = listdir(f"{pasta_manga}/{folder}")
            sorted_pdfs.sort(
                key= lambda x: int(x.split("_")[1].split(".")[0])
            )
            for pdf in sorted_pdfs:
                mergerPDF.append(PdfFileReader(f"{pasta_manga}/{folder}/{pdf}"))
            bar.next()

    print("Convertendo em PDF...")
    mergerPDF.write(f"{pasta_manga}/{pasta_manga}.pdf")
    print("Finalizado!")

def get_imagens_organizadas(pasta_manga):
    with Bar("Buscando imagens", max= len(listdir(pasta_manga))) as bar:    
        def is_file(x):
            bar.next()
            if path.isfile(f"{pasta_manga}/{x}"): return True
            return False
        imagens_organizadas = list(filter(is_file, listdir(pasta_manga)))
    imagens_organizadas.sort(key=lambda x: x.split("_")[1].split(".")[0])
    imagens_organizadas.sort(key=lambda x: x.split("_")[0])
    return imagens_organizadas

def run(pasta_manga):
    _imagens = get_imagens_organizadas(pasta_manga)
    _capitulos = get_capitulos(_imagens)
    criar_pastas_capitulos(_capitulos, pasta_manga)
    converter_image_to_pdf(_capitulos, pasta_manga)
    remover_imagens(pasta_manga)
    juntar_paginas_pdf(pasta_manga)
    