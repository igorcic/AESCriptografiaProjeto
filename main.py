import crypto
from crypto import Criptografia
import cv2 as cv
import cv2

def read_arq(num):
    retorno = []
    aux = ''

    if num == 1:
        arq = open("chave.txt")

    else:
        arq = open("nonce.txt")

    txt = arq.read()
    '''
        O byte do arquivo eh lido ate que apareca um espaco, entao esse byte eh transformado de string em um inteiro 
        de 0 a 255 e coloca
    '''
    for i in range(len(txt)):
        if txt[i] == ' ':
            retorno.append(int(float(aux)))
            aux = ''

        else:
            aux += txt[i]

    return retorno


def print_img(original, final, op1):
    aux1 = original
    aux2 = 0

    for i in range(len(original)):
        for j in range(len(original[i])):
            for k in range(3):
                aux1[i][j][k] = final[aux2]
                aux2 = aux2 + 1

    op = int(input('Deseja mostrar imagem na tela:\n' '    1-sim\n' '    2-nao\n'))

    if op == 1:
        cv2.imshow('resultado', aux1)
        cv2.waitKey(0)

    if op1 == 1:
        cv2.imwrite('cifrada.png', aux1)

    else:
        cv2.imwrite('imagem_final.png', aux1)


def salva_hash(chavenonce, op):
    if op == 1:
        arq = open("chave.txt", "w+")
    else:
        arq = open("nonce.txt", "w+")

    for num in chavenonce:
        arq.write(str(num))
        arq.write(" ")

    arq.close()


def trata_chave(chave):
    if len(chave) < 16:
        while len(chave) < 16:
            chave += b'\x00'

    elif len(chave) > 16:
        chave = chave[:16]

def capturar_foto():
    # Inicializa a câmera (use 0 para a câmera padrão)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera")
        return None

    # Captura um quadro da câmera
    ret, frame = cap.read()

    # Fecha a câmera
    cap.release()

    if not ret:
        print("Erro ao capturar a foto")
        return None

    # Salva a imagem capturada com o nome "cifra.png"
    cv2.imwrite("cifra.png", frame)

    return frame


def main():
    chave = []
    chaveaux = []
    noncekey = []
    word = []
    crypto1 = Criptografia(chave, 0)
    print('\nATENÇÃO - PROCEDIMENTO PASSO A PASSO:\n'
          'Para criptografar uma imagem:\n'
          'Passo 1: Certifique-se de criar uma imagem com o nome "cifra.png".\n'
          'Passo 2: Coloque a imagem "cifra.png" no mesmo diretório onde este programa está localizado.\n'
          'Passo 3: Execute o programa e escolha a opção de criptografia (por exemplo, digitando 1).\n'
          'Passo 4: Aguarde o processo de criptografia ser concluído.\n'
          'Passo 5: O resultado cifrado será salvo como "cifrada.png" no mesmo diretório.\n'
          '\n'
          'Para descriptografar uma imagem:\n'
          'Passo 1: Certifique-se de criar uma imagem com o nome "cifrada.png".\n'
          'Passo 2: Coloque a imagem "cifrada.png" no mesmo diretório onde este programa está localizado.\n'
          'Passo 3: Execute o programa e escolha a opção de descriptografia (por exemplo, digitando 2).\n'
          'Passo 4: Aguarde o processo de descriptografia ser concluído.\n'
          'Passo 5: O resultado descriptografado será salvo como "descifrada.png" no mesmo diretório.\n')

    option1 = int(input('Escolha um modo:\n\n1:ECB -> Adequado para criptografia de blocos independentes\n2:CTR -> Adequado para criptografia de fluxo de dados\n'))
    print(
        'Se ainda nao existir essa imagem com esse nome o programa entrara em erro.\n')
    op2 = int(input('1:Cifrar\n2:Decifrar\n'))

    if op2 == 1:
        print("Escolha uma opção:")
        print("1: Capturar foto para criptografia")
        print("2: Usar imagem existente")
        op_capture = int(input("Opção: "))

        if op_capture == 1:
            # Capturar uma foto
            frame = capturar_foto()

            if frame is None:
                return
            else:
                # Salvar a imagem capturada como "cifra.png"
                cv2.imwrite("cifra.png", frame)
                word = frame
        elif op_capture == 2:
            word = cv2.imread('cifra.png')
        else:
            print("Opção inválida")
            return
        print('ATENÇÃO: NO ARQUIVO, SOMENTE SÃO ACEITOS NÚMEROS INTEIROS SEPARADOS POR ESPAÇO')
        opk = int(input('Chave a ser usada:\n\n0: arquivo.txt\n1: Chave própria\n2: Chave aleatória\n'))

    else:
        word = cv2.imread('cifrada.png')
        opk = int(input('Chave a ser usada:\n\n0:arquivo.txt\n1:Chave propria\n'))

    if opk == 0:
        chave = read_arq(1)

    elif opk == 1:
        chaveaux = input(
            'Digite a chave, somente os 16 primeiros bytes da palavra serao considerados.')
        chave = bytes(chaveaux, 'utf-8')

    elif opk == 2:
        crypto1 = Criptografia(chave,1)
        chave = crypto1.nonce()

    if option1 == 2 and op2 == 2:
        noncekey = read_arq(2)

    elif option1 == 2:
        noncekey = crypto1.nonce()
        salva_hash(noncekey, 2)

    rodadas = int(input('Digite o numero de rodadas:\n'))

    trata_chave(chave)
    salva_hash(chave, 1)
    crypto1.key_expansion(chave, rodadas)

    if option1 == 1:
        wordfinal = crypto1.ECB(word, rodadas, op2)

    elif option1 == 2:
        wordfinal = crypto1.CTR(word, rodadas, noncekey)

    print_img(word, wordfinal, op2)


if __name__ == '__main__':
    main()
