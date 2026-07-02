import os
import re
import random
import math

SENHA_ATUAL = "123"

def mdc(a, b):
    # Calcula o MDC entre dois números usando o algoritmo de Euclides
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    # Implementa o algoritmo de Euclides estendido para encontrar coeficientes de Bézout
    # Usado para calcular o inverso modular
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    # Calcula o inverso modular de 'a' módulo 'm'
    # Essencial para a geração da chave privada RSA
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    else:
        return x % m

def eh_primo(n):
    # Verifica se um número é primo usando o método de divisão por tentativa
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Testa divisibilidade apenas por ímpares até a raiz quadrada de n
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def gerar_primo(bits=16):
    # Gera um número primo aleatório com o tamanho especificado em bits
    while True:
        p = random.randrange(2**(bits-1), 2**bits)
        if eh_primo(p):
            return p

def validar_forca_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r"[a-z]", senha):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    if not re.search(r"[0-9]", senha):
        return False, "A senha deve conter pelo menos um número."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False, "A senha deve conter pelo menos um caractere especial."
    return True, "Senha válida."

def verificar_senha():
    senha = input("Digite a senha: ")
    return senha == SENHA_ATUAL

def escrever_mensagem():
    # Cria um arquivo de texto com a mensagem do usuário
    id = input("Digite o ID da mensagem: ")
    mensagem = input("Digite a mensagem: ")
    with open(f"{id}.txt", "w") as arquivo:
        arquivo.write(mensagem)
    print("\nMensagem salva com sucesso!")

def criptografar():
    # Implementa o algoritmo RSA para criptografar uma mensagem
    id = input("Digite o ID da mensagem para criptografar: ")
    try:
        # Tenta abrir o arquivo com a mensagem original
        with open(f"{id}.txt", "r") as arquivo:
            mensagem = arquivo.read()
    except FileNotFoundError:
        print("\nErro: Mensagem não encontrada!")
        return
    if not verificar_senha():
        print("\nErro: Senha incorreta!")
        return
    
    print("\n=== Opções de Geração de Chaves ===")
    print("1. Gerar chaves automaticamente")
    print("2. Fornecer valores de p e q manualmente")
    opcao_chave = input("\nEscolha uma opção: ")
    
    bits = 16
    
    if opcao_chave == '1':
        # Gera automaticamente os números primos p e q
        p = gerar_primo(bits)
        q = gerar_primo(bits)
        while q == p:
            q = gerar_primo(bits)
        print(f"\nValores gerados automaticamente:")
        print(f"p = {p}")
        print(f"q = {q}")
    elif opcao_chave == '2':
        # Permite ao usuário fornecer os números primos p e q
        try:
            p = int(input("\nDigite o valor de p (número primo): "))
            if not eh_primo(p):
                print("\nErro: O valor de p não é um número primo!")
                return
                
            q = int(input("Digite o valor de q (número primo diferente de p): "))
            if not eh_primo(q):
                print("\nErro: O valor de q não é um número primo!")
                return
                
            if p == q:
                print("\nErro: Os valores de p e q devem ser diferentes!")
                return
        except ValueError:
            print("\nErro: Os valores devem ser números inteiros!")
            return
    else:
        print("\nOpção inválida!")
        return
    
    # Calcula os parâmetros RSA
    n = p * q  # Módulo n = p * q
    phi = (p - 1) * (q - 1)  # Função totiente de Euler
    e = 65537  # Expoente público comum (primo de Fermat)
    while mdc(e, phi) != 1:
        e = random.randrange(3, phi, 2)
    d = modinv(e, phi)  # Expoente privado
    
    # Converte a mensagem para números e criptografa
    msg_ints = [ord(char) for char in mensagem]
    cifrado = [str(pow(m, e, n)) for m in msg_ints]
    
    # Salva a mensagem criptografada com a chave privada embutida
    with open(f"{id}.enc", "w") as arquivo:
        arquivo.write(f"{d},{n}\n")
        arquivo.write(' '.join(cifrado))
    
    # Remove o arquivo original
    os.remove(f"{id}.txt")
    print("\nMensagem criptografada com sucesso!")
    print(f"Chave pública: (e={e}, n={n})")
    print(f"Chave privada: (d={d}, n={n})")

def descriptografar():
    id = input("Digite o ID da mensagem para descriptografar: ")
    try:
        # Abre o arquivo criptografado e extrai a chave privada e o texto cifrado
        with open(f"{id}.enc", "r") as arquivo:
            linhas = arquivo.readlines()
            chave_privada = linhas[0].strip()
            texto_cifrado = ' '.join(linhas[1:]).strip().split()
    except FileNotFoundError:
        print("\nErro: Mensagem criptografada não encontrada!")
        return
    except IndexError:
        print("\nErro: Formato de arquivo inválido!")
        return
    
    if not verificar_senha():
        print("\nErro: Senha incorreta!")
        return
    
    try:
        # Extrai os componentes da chave privada
        d, n = chave_privada.split(',')
        d, n = int(d), int(n)
        # Descriptografa cada caractere da mensagem
        msg_ints = [pow(int(c), d, n) for c in texto_cifrado]
        mensagem = ''.join([chr(m) for m in msg_ints])
    except Exception as e:
        print(f"\nErro ao descriptografar: {e}")
        return
    
    # Salva a mensagem descriptografada e remove o arquivo criptografado
    with open(f"{id}.txt", "w") as arquivo:
        arquivo.write(mensagem)
    os.remove(f"{id}.enc")
    print("\nMensagem descriptografada com sucesso!")

def alterar_senha():
    global SENHA_ATUAL
    print("\n=== Alterar Senha ===")
    if not verificar_senha():
        print("\nErro: Senha atual incorreta!")
        return
    nova_senha = input("\nDigite a nova senha: ")
    confirmar_senha = input("Confirme a nova senha: ")
    if nova_senha != confirmar_senha:
        print("\nErro: As senhas não coincidem!")
        return
    valida, mensagem = validar_forca_senha(nova_senha)
    if not valida:
        print(f"\nErro: {mensagem}")
        return
    SENHA_ATUAL = nova_senha
    print("\nSenha alterada com sucesso!")

def limpar_todas_mensagens():
    confirmacao = input("Tem certeza que deseja apagar todas as mensagens? (s/n): ").lower()
    if confirmacao != 's':
        print("Operação cancelada.")
        return
    for arquivo in os.listdir():
        if arquivo.endswith(".txt") or arquivo.endswith(".enc"):
            os.remove(arquivo)
    print("Todas as mensagens foram removidas com sucesso!")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    while True:
        limpar_tela()
        print("\n=== Menu Principal ===")
        print("1. Escrever nova mensagem")
        print("2. Criptografar mensagem")
        print("3. Descriptografar mensagem")
        print("4. Alterar senha")
        print("5. Limpar todas as mensagens")
        print("6. Sair")
        opcao = input("\nEscolha uma opção: ")
        if opcao == '1':
            limpar_tela()
            escrever_mensagem()
        elif opcao == '2':
            limpar_tela()
            criptografar()
        elif opcao == '3':
            limpar_tela()
            descriptografar()
        elif opcao == '4':
            limpar_tela()
            alterar_senha()
        elif opcao == '5':
            limpar_tela()
            limpar_todas_mensagens()
        elif opcao == '6':
            print("\nSaindo do programa...")
            break
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    limpar_tela()
    menu()