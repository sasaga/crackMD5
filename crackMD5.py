#!/usr/bin/env python
# -*- coding: utf-8 -*-
#autor samir sanchez garnica @sasaga92
import argparse
import socket
import sys
import platform
import os.path
from time import time, strftime
from datetime import datetime
import hashlib
from hashlib import md5


def script_colors(color_type, text):
    color_end = '\033[0m'

    if color_type.lower() == "r" or color_type.lower() == "red":
        red = '\033[91m'
        text = red + text + color_end
    elif color_type.lower() == "lgray":
        gray = '\033[2m'
        text = gray + text + color_end
    elif color_type.lower() == "gray":
        gray = '\033[90m'
        text = gray + text + color_end
    elif color_type.lower() == "strike":
        strike = '\033[9m'
        text = strike + text + color_end
    elif color_type.lower() == "underline":
        underline = '\033[4m'
        text = underline + text + color_end
    elif color_type.lower() == "b" or color_type.lower() == "blue":
        blue = '\033[94m'
        text = blue + text + color_end
    elif color_type.lower() == "g" or color_type.lower() == "green":
        green = '\033[92m'
        text = green + text + color_end
    elif color_type.lower() == "y" or color_type.lower() == "yellow":
        yellow = '\033[93m'
        text = yellow + text + color_end
    elif color_type.lower() == "c" or color_type.lower() == "cyan":
        cyan = '\033[96m'
        text = cyan + text + color_end
    elif color_type.lower() == "cf" or color_type.lower() == "cafe":
        cafe = '\033[52m'
        text = cafe + text + color_end
    else:
        return text
    return  text

def banner_welcome():
    banner = '''

                              ██████╗██████╗  █████╗  ██████╗██╗  ██╗███╗   ███╗██████╗ ███████╗
                             ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝████╗ ████║██╔══██╗██╔════╝
                             ██║     ██████╔╝███████║██║     █████╔╝ ██╔████╔██║██║  ██║███████╗
                             ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██║╚██╔╝██║██║  ██║╚════██║
                             ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗██║ ╚═╝ ██║██████╔╝███████║
                              ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝
                                                                                    version: 1.0
                                                                    Autor: Samir Sanchez Garnica
                                                                                       @sasaga92
                                                                     
    '''
    return script_colors('lgray',banner)

def convertMS5Hash(my_string,ini,fin):
    m = hashlib.md5()
    m.update(my_string)
    return m.hexdigest().encode('utf-8')[ini:fin]


def main():
    print banner_welcome()
    parser = argparse.ArgumentParser()
    parser.add_argument("--wordlist", dest="wordlist", help="introduce el path del diccionario", required=True)
    parser.add_argument("--range", dest="range", help="rango de recorte del hash inicial,final", required=True)
    parser.add_argument("--hash_file", dest="hash_file", help="introducir hash MD5 modificado a crackear", required=True)

    args = parser.parse_args()
    range_part = str(args.range).split(",")

    now = datetime.now() 
    time_actual =  " Time Local: ",now.strftime('%H:%M:%S %Y/%m/%d')

    tiempo_inicial = time()
    
    credenciales_search = {}

    archivo_hashes = open(args.hash_file, 'r')
    archivo_passwords = open(args.wordlist, 'r')
 
    num_archivo_hashes =  len(archivo_hashes.readlines())
    num_archivo_passwords =  len(archivo_passwords.readlines())
    
    archivo_hashes.close()
    archivo_passwords.close()

    print script_colors("g", "[+] ") + script_colors("c", "Iniciando cracking: ") + script_colors("c",time_actual[0]) + script_colors("red",time_actual[1]) + script_colors("c", " Numero de HASHES:") + script_colors("yellow",str(num_archivo_hashes)) + script_colors("c", " Numero de CONTRASEÑAS:") + script_colors("yellow",str(num_archivo_passwords))

    if args.wordlist and args.hash_file and args.range:
        with open(args.wordlist,'r') as infile:
            for line in infile:
                password = line.strip('\r\n')
                password_hasheado = convertMS5Hash(password,int(range_part[0]),int(range_part[1]));
                try:
                   with open(args.hash_file, 'r') as inhashes:
                     for hashes in inhashes:
                        hash_clean = hashes.strip('\r\n')

                        if password_hasheado == hash_clean:
                            credenciales_search[password_hasheado] = [password]
                except:
                    pass
        tiempo_final = time()
        tiempo_ejecucion = tiempo_final - tiempo_inicial

        if not credenciales_search:
            print script_colors("lgray","[-] no se encontraron CREDENCIALES para el crackeo de los  HASHES :( ");
        else:
            for hashes in credenciales_search:
                print script_colors("lgray","[+] HASH encontrado: ")  + script_colors("lgray","credenciales:[") + script_colors("cf", str(hashes)) +  ":" + script_colors("g", str(credenciales_search[hashes][0])) + "]"+script_colors("b"," Contraseña Correcta")

        print script_colors("lgray","crackeo realizado en: ") + script_colors("c", str(int(tiempo_ejecucion))) + script_colors("lgray"," Segundos")
    else:
        print script_colors("yellow","[-] ") + script_colors("c", "Requiere parametros obligatorios ")
        exit(0)


if __name__ == '__main__':
    main()
