import re


def clean_direccion(string):
    """
    Funcion que busca limpiar la direccion, para que pueda ser ubicada por el buscador
    en el mapa
    """

    # Posibles palabras
    # kra, cra, carrera, calle, clle, calle, cll, cl
    # favor diligenciar, PENDIENTE, DIAGONAL, REGISTRAR, -, --, NN

    digit = re.compile(r'(\d{1,3})([a-zA-Z]{1})?(\d{1})?')

    # Lo primero es verificar que tenga numeros la direccion
    numbers = digit.findall(string)
    if numbers != [] and digit.search(string) is not None:
        regex_carrera = re.compile(r'([cC](([aArReE]{5,6})|([rRaA]{2})|([rR]{1,2})))|([kK](([aArReE]{5,6})|([rRaA]{2})|([rR]{1,2})))')
        regex_calle = re.compile(r'([cC](([lL]{1,2})|([aAlLeE]{2,4})))')

        regex_all = re.compile(r'([cC](([aArReE]{5,6})|([rRaA]{2})|([rR]{1,2})))|([kK](([aArReE]{5,6})|([rRaA]{2})|([rR]{1,2})))|([cC](([lL]{1,2})|([aAlLeE]{2,4})))')

        formato = regex_all.search(string)

        if formato is not None:
            match = formato.group()
            if regex_calle.search(match) is not None:
                formato = 'Calle'
            elif regex_carrera.search(match) is not None:
                formato = 'Carrera'
            else:
                raise ValueError('Match Not Found With %s' % string)

            try:
                return '{formato} {numero1} # {numero2} {ciudad}'.format(
                    formato=formato, numero1=''.join(numbers[0]),
                    numero2=''.join(numbers[1]), ciudad='Barranquilla'
                )
            except IndexError:
                pass
        else:
            pass
    return ''


# if any(not x for x in [regex_calle.match(string), regex_carrera.match(string)]):
#     if regex_carrera.match(string) is not None:
#         try:
#             return 'Carrera %s # %s Barranquilla' % (numbers[0], numbers[1])
#         except IndexError:
#             pass
#     elif regex_calle.match(string) is not None:
#         try:
#             return 'Calle %s # %s Barranquilla' % (numbers[0], numbers[1])
#         except IndexError:
#             pass
# else:
