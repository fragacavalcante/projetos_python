# coding: latin-1
import os,sys

def Valida_IP(ip):
        ip_decimal = ip.split('.')

        if ip_decimal.count('.') > 3:
                return 1
        
        for i in ip_decimal:
                if not i.isdigit():
                        return 1
                if int(i) > 255:
                        return 1

def Verifica_Classe(ip):
	octetos = ip.split('.')
	if int(octetos[0]) > 0 and int(octetos[0]) <= 127 :
		return 1
	elif int(octetos[0]) >=128 and int(octetos[0]) <=191 :
		return 2
	elif int(octetos[0]) >=192 and int(octetos[0]) <=223 :
		return 3
	elif int(octetos[0]) >=224 and int(octetos[0]) <=239 :
		return 4
        elif int(octetos[0]) >=240 and int(octetos[0]) <=247 :
		return 5
	else :
                return 9

def Calcula_Partes_Subrede_Host(ip,mascara):
	bits_mascara = ""
	classe_ip = 0
	mascara_octetos = mascara.split('.')

    # Converte a mascara em decimal para binario e ajusta em 8 bits
      
	for i in mascara_octetos:
		bits_mascara += bin(int(i))[2:].rjust(8,'0') # o valor 2 utilizado no slice é para retirar os caracteres '0b' que aparecem na conversão para binário
                        
	classe_ip = Verifica_Classe(ip)

    # 	Retorna a quantidade de bits de subrede e de host (subrede, host)
    
	if classe_ip == 1 :
		return (int(bits_mascara.count('1')) - 8, int(bits_mascara.count('0')))
	if classe_ip == 2 :
		return (int(bits_mascara.count('1')) - 16, int(bits_mascara.count('0')))
	if classe_ip == 3 :
		return (int(bits_mascara.count('1')) - 24, int(bits_mascara.count('0')))
	    
	    
def Calcula_Quantidade_Subredes(ip, mascara):
        bits_subrede, bits_host = Calcula_Partes_Subrede_Host(ip,mascara)
        subredes = 2 ** int(bits_subrede)
        return subredes

def Calcula_Quantidade_Hosts_Subrede(ip,mascara):
        bits_subrede, bits_host = Calcula_Partes_Subrede_Host(ip,mascara)
        hosts = (2 ** int(bits_host)) - 2
        return hosts

def Calcula_Subrede_Especifica(ip,mascara):
        classe_ip = Verifica_Classe(ip)
        bits_subrede, bits_host = Calcula_Partes_Subrede_Host(ip,mascara)
        ip_binario = ""  # irá armazenar o endereço ip em formato binario (32 bits)
        subrede_binario = "" # esta variavel ira armazenar em binário somente a parte de subrede do endereco IP
        ip_decimal = ip.split('.')
        tamanho_octeto=8
        octetos1 = []
        octetos2 = []
                
        for i in ip_decimal:
		ip_binario += bin(int(i))[2:].rjust(8,'0') # o valor 2 utilizado no slice é para retirar os caracteres '0b' que aparecem na conversão para binário
        
        if classe_ip == 1:
                parte_rede = ip.split('.')[0:1]
        elif classe_ip == 2:
                parte_rede = ip.split('.')[0:2]
        elif classe_ip == 3:
                parte_rede = ip.split('.')[0:3]

        subrede_binario = ip_binario[tamanho_octeto * classe_ip :(tamanho_octeto * classe_ip) + bits_subrede]
        parte_host = ip_binario[(tamanho_octeto * classe_ip) + bits_subrede:]
        
        endereco_subrede = ip_binario[0:(tamanho_octeto * classe_ip) + bits_subrede] + '0' * len(parte_host)
        endereco_broadcast_subrede = ip_binario[0:(tamanho_octeto * classe_ip) + bits_subrede] + '1' * len(parte_host)
                
        for i in range(0,len(endereco_subrede),tamanho_octeto):
                octetos1.append(int(endereco_subrede[ i : int(i+tamanho_octeto) ] , 2))                      

        for i in range(0,len(endereco_broadcast_subrede),tamanho_octeto):
                octetos2.append(int(endereco_broadcast_subrede[ i : int(i+tamanho_octeto) ] , 2))                      

        subrede =  str(int(subrede_binario,2)+1)
        endereco_ip_rede_dec = "".join([str(octetos1[0]),'.',str(octetos1[1]),'.',str(octetos1[2]),'.',str(octetos1[3])])
        endereco_ip_inicial_dec = "".join([str(octetos1[0]),'.',str(octetos1[1]),'.',str(octetos1[2]),'.',str(octetos1[3]+1)])
        endereco_ip_final_dec = "".join([str(octetos2[0]),'.',str(octetos2[1]),'.',str(octetos2[2]),'.',str(octetos2[3]-1)])
        endereco_ip_broadcast_dec = "".join([str(octetos2[0]),'.',str(octetos2[1]),'.',str(octetos2[2]),'.',str(octetos2[3])])

        print '      Subrede'.ljust(25), 'Inicial'.ljust(20), 'Final'.ljust(20), 'Broadcast'
        print str(subrede).ljust(4), endereco_ip_rede_dec.ljust(20), endereco_ip_inicial_dec.ljust(20), endereco_ip_final_dec.ljust(20), endereco_ip_broadcast_dec
            

def Calcula_Faixa_Enderecos_Subredes(ip, mascara):
        classe_ip = Verifica_Classe(ip)
        bits_subrede, bits_host = Calcula_Partes_Subrede_Host(ip,mascara)
        quantidade_subredes = Calcula_Quantidade_Subredes(ip, mascara)
        parte_host_bin = '0' * bits_host
        parte_host_broadcast_bin = '1' * bits_host
        tamanho_octeto=8
        numero_subrede=1
        
        if classe_ip == 1:
                parte_rede = ip.split('.')[0:1]
        elif classe_ip == 2:
                parte_rede = ip.split('.')[0:2]
        elif classe_ip == 3:
                parte_rede = ip.split('.')[0:3]
                      
        print '       Subrede'.ljust(25), 'Inicial'.ljust(20), 'Final'.ljust(20), 'Broadcast'

        #Exibe a lista de todas as subredes, com o seu respectivo ID, endereço de rede, endereço inicial, final e Broadcast
        
        for i in range(quantidade_subredes):
                # o valor 2 utilizado no slice é para retirar os caracteres '0b' que aparecem na conversão para binário
                parte_subrede_bin = str(bin(i))[2:].rjust(bits_subrede,'0')     # Transforma a parte de subrede em binario e ajusta com 0s se necessrio
                endereco_rede_subrede = parte_subrede_bin + parte_host_bin      # Endereco de rede da subrede
                endereco_broadcast_subrede =  parte_subrede_bin + parte_host_broadcast_bin      # Endereco de broadcast da subrede
                octetos1 = []
                octetos2 = []

                #Monta endereco de Rede
                for i in range(0,len(endereco_rede_subrede),tamanho_octeto):
                        octetos1.append(int(endereco_rede_subrede[ i : int(i+tamanho_octeto) ] , 2))                      
                ip_subrede1 = parte_rede + octetos1
                
                # Monta endereco de Broadcast
                for i in range(0,len(endereco_broadcast_subrede),tamanho_octeto):
                        octetos2.append(int(endereco_broadcast_subrede[ i : int(i+tamanho_octeto) ] , 2))                        
                ip_subrede2 = parte_rede + octetos2
                
                # Formata os IPs adequadamente para exibir na tela

                endereco_ip_rede_dec = "".join([str(ip_subrede1[0]),'.',str(ip_subrede1[1]),'.',str(ip_subrede1[2]),'.',str(ip_subrede1[3])])
                
                endereco_ip_inicial_dec = "".join([str(ip_subrede1[0]),'.',str(ip_subrede1[1]),'.',str(ip_subrede1[2]),'.',str(ip_subrede1[3]+1)])
             
                endereco_ip_final_dec = "".join([str(ip_subrede2[0]),'.',str(ip_subrede2[1]),'.',str(ip_subrede2[2]),'.',str(ip_subrede2[3]-1)])
               
                endereco_ip_broadcast_dec = "".join([str(ip_subrede2[0]),'.',str(ip_subrede2[1]),'.',str(ip_subrede2[2]),'.',str(ip_subrede2[3])])

                print str(numero_subrede).ljust(4), endereco_ip_rede_dec.ljust(20), endereco_ip_inicial_dec.ljust(20), endereco_ip_final_dec.ljust(20), endereco_ip_broadcast_dec

                # Aumentar em cada iteração o valor da subrede que está sendo impressa
                numero_subrede += 1
                                        
                # A cada iteração as listas devem ser limpas
                octetos1[:]=[]
                octetos2[:]=[]

def Limpar_Tela():
        print '\n' * 100


def Tela_Inicial():
        
        while True:
                print '1 - Calcular faixa de subredes'
                print '2 - Encontrar faixa de endereços para uma subrede específica'
                print '3 - Calcular quantidade de subredes'
                print '4 - Calcular quantidade de hosts por subrede'
                print '5 - Verificar classe do endereço IP'
                print '6 - Sair'
                
                opcao = raw_input('\t\tDigite a opção desejada:')
                print '\n' * 100
                if opcao == '1':
                        ip = raw_input('Digite o endereço IP da rede:')
                        mascara = raw_input('Digite a máscara:')
                elif opcao == '6':
                        print '\n' * 100
                        print 'Saindo'
                        break

                if Valida_IP(ip) == 1 or Valida_IP(mascara) == 1 :
                        print 'Endereço Inválido'
                else:
                        Calcula_Faixa_Enderecos_Subredes(ip,mascara)
                                        
                voltar = raw_input('Deseja voltar a tela inicial (S/N):').upper()
                Limpar_Tela()
                
                if voltar == 'N':
                        Limpar_tela()
                        print 'Saindo...'
                        break
