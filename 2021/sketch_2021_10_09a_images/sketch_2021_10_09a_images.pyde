import os  # para usar listdir, path.isfile, path.join

imagens = []  # lista que vai receber objetos PImage (Processing Image data)

def setup():
    size(400, 400)
    # Ponha as imagens na pasta /data/ dentro da pasta do seu sketch
    data_folder = sketchPath('data')  # não funciona fora do setup
    caminhos_arquivos = []
    for nome_arquivo in os.listdir(data_folder):
        caminho_arquivo = os.path.join(data_folder, nome_arquivo)
        if os.path.isfile(caminho_arquivo) and has_image_ext(caminho_arquivo):
            caminhos_arquivos.append(caminho_arquivo)
    for caminho_arquivo in caminhos_arquivos:
        img = loadImage(caminho_arquivo)
        imagens.append(img)
    noLoop()  # clique do mouse para redraw
        
def draw():
    background(0)
    # from random import choice
    # random_image = choice(imagens)
    i = int(random(10000)) % len(imagens)  
    random_image = imagens[i]
    f = 1
    if random_image.width > width:
        f = float(width) / random_image.width
    if random_image.height * f > height:
        f = float(height) / random_image.height
    imageMode(CENTER)
    image(random_image, width / 2, height / 2,
          random_image.width * f, random_image.height * f)
                     
def mouseClicked():
    redraw()
    
def has_image_ext(file_name):
    valid_ext = ('jpg', 'png', 'jpeg', 'gif', 'tif', 'tga')
    file_ext = file_name.split('.')[-1]
    return file_ext.lower() in valid_ext
