from random import choice
from time import sleep
import unicodedata
from pathlib import Path
import os

os.system('')
print('\033[2J\033[H', end='')

BASE = Path(__file__).parent
arquivo = BASE / 'termonal-palavras.txt'
vitorias = 0


def acerto(letra):
    return f'\033[32m{letra}\033[0m '


def erro(letra):
    return f'\033[31m{letra}\033[0m '


def quase(letra):
    return f'\033[33m{letra}\033[0m '


def remover_acentos(texto):
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')


def ver():
    abc = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
    abctemp = abc
    for letra in abc:
        if letra in lista_dentro:
            abctemp = abctemp.replace(letra, f'\033[32m{letra}\033[0m')

        elif letra in lista_quase:
            abctemp = abctemp.replace(letra, f'\033[33m{letra}\033[0m')

        elif letra in lista_fora:
            abctemp = abctemp.replace(letra, f'\033[31m{letra}\033[0m')

    print(f'{abctemp}')


def sortear():
    with open(arquivo, "r", encoding='utf-8') as f:
        conteudo_str = f.read().upper()

    conteudo = conteudo_str.split()
    segredo = str(choice(conteudo))
    segredo_sem_acento = remover_acentos(segredo)
    lista_fora = ''
    lista_dentro = ''
    lista_quase = ''
    tentativa = 0
    palavras_jogadas = []

    return segredo, segredo_sem_acento, lista_fora, lista_dentro, lista_quase, tentativa, conteudo, conteudo_str, palavras_jogadas


segredo, segredo_sem_acento, lista_fora, lista_dentro, lista_quase, tentativa, conteudo, conteudo_str, palavras_jogadas = sortear()
roubo = False
palavras_sem_acento = remover_acentos(conteudo_str).split()

try:
    while True:

        print()
        ver()
        print('\033[2A', end='')
        contagem = {}

        for letra in list(segredo_sem_acento):
            if letra in contagem:
                contagem[letra] += 1
            else:
                contagem[letra] = 1

        chute = input('\033[2K').replace(' ', '').upper()
        chute_sem_acento = remover_acentos(chute)

        if chute == str(999):
            break

        elif chute == 'MOSTRAR':
            print(f'\033[2K{segredo}')
            roubo = True

        elif len(chute) > 5 or len(chute) < 5:
            print('\033[2KInsira palavras de 5 letras.')
            sleep(1)
            print('\033[1A\033[2K\033[1A\033[2K', end='')

        elif chute_sem_acento == segredo_sem_acento and not roubo:
            print('\033[1A\033[2K', end='')
            for letra in segredo:
                print(acerto(letra), end='')
            print()
            vitorias += 1
            print(
                f'\033[2K> Acertou após: {tentativa + 1} tentativas!\n> Você ganhou {vitorias} vezes\n> Nova palavra sorteada!')
            segredo, segredo_sem_acento, lista_fora, lista_dentro, lista_quase, tentativa, conteudo, conteudo_str, palavras_jogadas = sortear()

        elif chute_sem_acento == segredo_sem_acento and roubo:
            print('\033[1A\033[2K', end='')
            for letra in segredo:
                print(acerto(letra), end='')
            print()
            print(
                f'\033[2K> Você roubou, vitoria desconsiderada.\n> Você ganhou {vitorias} vezes\n> Nova palavra sorteada!')
            segredo, segredo_sem_acento, lista_fora, lista_dentro, lista_quase, tentativa, conteudo, conteudo_str, palavras_jogadas = sortear()
            roubo = False

        elif chute_sem_acento in palavras_jogadas:
            print('\033[2KPalavra já jogada.')
            sleep(1)
            print(f'\033[1A\033[2K\033[1A\033[2K', end='')

        elif chute_sem_acento in palavras_sem_acento:
            palavras_jogadas.append(chute_sem_acento)
            local = palavras_sem_acento.index(chute_sem_acento)
            tentativa += 1
            resultado = [None] * 5

            for i in range(5):
                if chute_sem_acento[i] == segredo_sem_acento[i]:
                    resultado[i] = acerto(conteudo[local][i])
                    contagem[chute_sem_acento[i]] -= 1

                    if chute_sem_acento[i] not in lista_dentro:
                        lista_dentro += chute_sem_acento[i]

            for i in range(5):
                if resultado[i] is not None:
                    continue

                letra = chute_sem_acento[i]

                if letra in contagem and contagem[letra] > 0:
                    resultado[i] = quase(conteudo[local][i])
                    contagem[letra] -= 1

                    if letra not in lista_quase and letra not in lista_dentro:
                        lista_quase += letra
                        lista_fora = lista_fora.replace(letra, '')

                else:
                    resultado[i] = erro(conteudo[local][i])
                    if letra not in lista_fora and letra not in lista_dentro and letra not in lista_quase:
                        lista_fora += letra

            print(f'\033[1A\033[2K', end='')
            print(''.join(resultado))

        else:
            print('\033[2KPalavra inválida')
            sleep(1)
            print(f'\033[1A\033[2K\033[1A\033[2K', end='')


except (KeyboardInterrupt, EOFError):
    print()

print(f'\n\nA palavra secreta era: {segredo}')
print('Jogo encerrado.\nObrigado por jogar!')

try:
    input('\nPressione ENTER para sair.')
except (KeyboardInterrupt, EOFError):
    pass
