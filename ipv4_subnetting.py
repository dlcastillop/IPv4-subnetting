from random import randint
from ipaddress import IPv4Address


def validar_ip(ip):
    """
    Comprueba si se ha introducido una dirección IPv4 con el formato válido.
    """
    try:
        IPv4Address(ip)
        return True
    except ValueError:
        return False


def validar_mascara(mascara):
    """
    Comprueba si se ha introducido una máscara de subred válida en cualquier formato.
    """
    try:
        mascara = int(mascara)
    except ValueError:
        if mascara == mascara_ddn(8) or mascara == mascara_ddn(9) or mascara == mascara_ddn(10):
            return True
        elif mascara == mascara_ddn(11) or mascara == mascara_ddn(12) or mascara == mascara_ddn(13):
            return True
        elif mascara == mascara_ddn(14) or mascara == mascara_ddn(15) or mascara == mascara_ddn(16):
            return True
        elif mascara == mascara_ddn(17) or mascara == mascara_ddn(18) or mascara == mascara_ddn(19):
            return True
        elif mascara == mascara_ddn(20) or mascara == mascara_ddn(21) or mascara == mascara_ddn(22):
            return True
        elif mascara == mascara_ddn(23) or mascara == mascara_ddn(24) or mascara == mascara_ddn(25):
            return True
        elif mascara == mascara_ddn(26) or mascara == mascara_ddn(27) or mascara == mascara_ddn(28):
            return True
        elif mascara == mascara_ddn(29) or mascara == mascara_ddn(30):
            return True
        else:
            return False
    else:
        if 8 <= mascara <= 30:
            return True
        else:
            return False


def validar_subnetting(ip):
    """
    Comprueba si la dirección IP introducida se le puede aplicar el proceso subnetting.
    """
    try:
        if IPv4Address('0.0.0.0') <= IPv4Address(ip) <= IPv4Address('0.255.255.255'):
            return False
        elif IPv4Address('127.0.0.0') <= IPv4Address(ip) <= IPv4Address('127.255.255.255'):
            return False
        elif IPv4Address('224.0.0.0') <= IPv4Address(ip) <= IPv4Address('255.255.255.255'):
            return False
        else:
            return True
    except ValueError:
        return False


def ip_aleatoria():
    """
    Genera aleatoriamente una dirección IPv4.
    """
    octeto1 = str(randint(0, 225))
    octeto2 = str(randint(0, 255))
    octeto3 = str(randint(0, 255))
    octeto4 = str(randint(0, 255))

    return f"{octeto1}.{octeto2}.{octeto3}.{octeto4}"


def mascara_ddn(mascara_prefijo):
    """
    Recibe una máscara en el formato de prefijo y la convierte al formato DDN.
    """
    mascara_prefijo = str(mascara_prefijo)
    if mascara_prefijo == "8":
        return '255.0.0.0'
    elif mascara_prefijo == "9":
        return '255.128.0.0'
    elif mascara_prefijo == "10":
        return '255.192.0.0'
    elif mascara_prefijo == "11":
        return '255.224.0.0'
    elif mascara_prefijo == "12":
        return '255.240.0.0'
    elif mascara_prefijo == "13":
        return '255.248.0.0'
    elif mascara_prefijo == "14":
        return '255.252.0.0'
    elif mascara_prefijo == "15":
        return '255.254.0.0'
    elif mascara_prefijo == "16":
        return '255.255.0.0'
    elif mascara_prefijo == "17":
        return '255.255.128.0'
    elif mascara_prefijo == "18":
        return '255.255.192.0'
    elif mascara_prefijo == "19":
        return '255.255.224.0'
    elif mascara_prefijo == "20":
        return '255.255.240.0'
    elif mascara_prefijo == "21":
        return '255.255.248.0'
    elif mascara_prefijo == "22":
        return '255.255.252.0'
    elif mascara_prefijo == "23":
        return '255.255.254.0'
    elif mascara_prefijo == "24":
        return '255.255.255.0'
    elif mascara_prefijo == "25":
        return '255.255.255.128'
    elif mascara_prefijo == "26":
        return '255.255.255.192'
    elif mascara_prefijo == "27":
        return '255.255.255.224'
    elif mascara_prefijo == "28":
        return '255.255.255.240'
    elif mascara_prefijo == "29":
        return '255.255.255.248'
    elif mascara_prefijo == "30":
        return '255.255.255.252'
    else:
        return None


def cadena_lista(cadena):
    """
    Convierte una cadena en el formato DDN a una lista.
    """
    ddn = ['', '', '', '']
    j = 0

    for i in range(len(cadena)):
        if cadena[i] != '.':
            ddn[j] += cadena[i]
        else:
            ddn[j] = int(ddn[j])
            j += 1
    ddn[3] = int(ddn[3])

    return ddn


def lista_cadena(lista):
    """
    Convierte una lista a una cadena en el formato DDN.
    """
    ip = ""

    for i in range(0, 4):
        ip += str(lista[i])
        if i < 3:
            ip += '.'

    return ip


def id_subred(ip, mascara):
    """
    Calcula el ID de subred a partir de una dirección IP y una máscara.
    """
    ip = cadena_lista(ip)
    mascara = cadena_lista(mascara)

    id = [0, 0, 0, 0]

    for i in range(0, 4):
        if mascara[i] == 255:
            id[i] = ip[i]
        elif mascara[i] == 0:
            id[i] = id[i]
        else:
            magico = 256 - mascara[i]
            id[i] = ip[i] - (ip[i] % magico)

    return lista_cadena(id)


def dir_broadcast(ip, mascara):
    """
    Calcula la dirección broadcast a partir de una dirección IP y una máscara.
    """
    ip = cadena_lista(ip)
    mascara = cadena_lista(mascara)

    broadcast = [255, 255, 255, 255]

    for i in range(0, 4):
        if mascara[i] == 255:
            broadcast[i] = ip[i]
        elif mascara[i] == 0:
            broadcast[i] = broadcast[i]
        else:
            magico = 256 - mascara[i]
            id = ip[i] - (ip[i] % magico)
            broadcast[i] = id + magico - 1

    return lista_cadena(broadcast)


def primera_dir(ip, mascara):
    """
    Calcula la primera dirección asignable a hosts a partir de una dirección IP y una máscara.
    """
    id = id_subred(ip, mascara)
    id = cadena_lista(id)
    id[3] = id[3] + 1
    return lista_cadena(id)


def ultima_dir(ip, mascara):
    """
    Calcula la última dirección asignable a hosts a partir de una dirección IP y una máscara.
    """
    broadcast = dir_broadcast(ip, mascara)
    broadcast = cadena_lista(broadcast)
    broadcast[3] = broadcast[3] - 1
    return lista_cadena(broadcast)
