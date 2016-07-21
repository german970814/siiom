from wand.image import Image
import os


def pdf_to_png(archivo, extencion='png'):
    """
    Funcion que se encarga de pasar los archivos de pdf en png y agruparlos en carpetas
    """
    CARPETA_PDF_TO_IMAGE = '/pdf2img/'
    __accepted__ = ['png', 'jpg', 'JPEG', 'gif', 'IMAGE', 'PNJ', 'ico', 'jpeg', 'bmp', 'BMP']

    if len(extencion.split('.')) > 1:
        extencion = extencion.split('.')[len(extencion) - 1]

    if os.path.exists(archivo._get_path()):

        file_especifications = archivo.name.split('/')
        # area = file_especifications[1]
        # registro = file_especifications[2]
        file_name = file_especifications[len(file_especifications) - 1]

        imagen = Image(filename=archivo._get_path())

        ruta = '/'
        _rutas = archivo._get_path().split('/')

        while ruta == '/':
            if os.path.isdir(ruta.join(_rutas)):
                ruta = ruta.join(_rutas)
            else:
                del _rutas[len(_rutas) - 1]

        if file_name.split('.')[len(file_name.split('.')) - 1] not in __accepted__:
            if not os.path.exists(ruta + CARPETA_PDF_TO_IMAGE):
                os.mkdir(ruta + CARPETA_PDF_TO_IMAGE, 0755)
                if not os.path.exists(ruta + CARPETA_PDF_TO_IMAGE):
                    raise IndexError("Directory was not created yet")

            imagen.save(filename=ruta + CARPETA_PDF_TO_IMAGE + file_name.split('.')[0] + '.' + extencion)

        _return_ruta = ruta + CARPETA_PDF_TO_IMAGE
        return _return_ruta

    return None
