# -*- coding: latin-1 -*-
import os
import sys

def validaIP(ip):
		ip_decimal = ip.split('.')
		separador_decimal =  ip.count('.')
		
		if separador_decimal != 3:
			return 1

		for i in ip_decimal:
			if not i.isdigit():
				return 1
			if int(i) > 255 or int(i) < 0:
				return 1

def verificaClasse(ip):
		octetos = ip.split('.')
		if int(octetos[0]) > 0 and int(octetos[0]) <= 127:
			return 1
		elif int(octetos[0]) >=128 and int(octetos[0]) <=191:
			return 2
		elif int(octetos[0]) >=192 and int(octetos[0]) <=223:
			return 3
		elif int(octetos[0]) >=224 and int(octetos[0]) <=239:
			return 4
		elif int(octetos[0]) >=240 and int(octetos[0]) <=247:
			return 5
		else :
			return 9

def calculaPartesSubredeHost(ip,mascara):
	bits_mascara = ""
	classe_ip = 0
	mascara_octetos = mascara.split('.')

	# Converte a mascara em decimal para binario e ajusta em 8 bits
	  
	for i in mascara_octetos:
		bits_mascara += bin(int(i))[2:].rjust(8,'0') # o valor 2 utilizado no slice � para retirar os caracteres '0b' que aparecem na convers�o para bin�rio
						
	classe_ip = verificaClasse(ip)

	# 	Retorna a quantidade de bits de subrede e de host (subrede, host)
	
	if classe_ip == 1:
		return (int(bits_mascara.count('1')) - 8, int(bits_mascara.count('0')))
	if classe_ip == 2:
		return (int(bits_mascara.count('1')) - 16, int(bits_mascara.count('0')))
	if classe_ip == 3:
		return (int(bits_mascara.count('1')) - 24, int(bits_mascara.count('0')))
		
		
def calculaQuantidadeSubredes(ip, mascara):
	bits_subrede, bits_host = calculaPartesSubredeHost(ip,mascara)
	subredes = 2 ** int(bits_subrede)
	return subredes

def calculaQuantidadeHostSubrede(ip,mascara):
	bits_subrede, bits_host = calculaPartesSubredeHost(ip,mascara)
	hosts = (2 ** int(bits_host)) - 2
	return hosts

def calculaSubredeEspecifica(ip,mascara):
	classe_ip = verificaClasse(ip)
	bits_subrede, bits_host = calculaPartesSubredeHost(ip,mascara)
	ip_binario = ""  # ir� armazenar o endere�o ip em formato binario (32 bits)
	subrede_binario = "" # esta variavel ira armazenar em bin�rio somente a parte de subrede do endereco IP
	ip_decimal = ip.split('.')
	tamanho_octeto=8
	octetos1 = []
	octetos2 = []
				
	for i in ip_decimal:
		ip_binario += bin(int(i))[2:].rjust(8,'0') # o valor 2 utilizado no slice � para retirar os caracteres '0b' que aparecem na convers�o para bin�rio

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

	print ('      Subrede'.ljust(25), 'Inicial'.ljust(20), 'Final'.ljust(20), 'Broadcast')
	print (str(subrede).ljust(4), endereco_ip_rede_dec.ljust(20), endereco_ip_inicial_dec.ljust(20), endereco_ip_final_dec.ljust(20), endereco_ip_broadcast_dec)
			

def calculaFaixaEnderecosSubredes(ip, mascara):
	classe_ip = verificaClasse(ip)
	bits_subrede, bits_host = calculaPartesSubredeHost(ip,mascara)
	quantidade_subredes = calculaQuantidadeSubredes(ip, mascara)
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
					  
	print ('       Subrede'.ljust(25), 'Inicial'.ljust(20), 'Final'.ljust(20), 'Broadcast')

	#Exibe a lista de todas as subredes, com o seu respectivo ID, endere�o de rede, endere�o inicial, final e Broadcast
		
	for i in range(quantidade_subredes):
		# o valor 2 utilizado no slice � para retirar os caracteres '0b' que aparecem na convers�o para bin�rio
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

		print (str(numero_subrede).ljust(4), endereco_ip_rede_dec.ljust(20), endereco_ip_inicial_dec.ljust(20), endereco_ip_final_dec.ljust(20), endereco_ip_broadcast_dec)

		# Aumentar em cada itera��o o valor da subrede que est� sendo impressa
		numero_subrede += 1
										
		# A cada itera��o as listas devem ser limpas
		octetos1[:]=[]
		octetos2[:]=[]

def limparTela():
	print ('\n' * 100)

def qualClasse(ip):
	classe = verificaClasse(ip)
	if classe == 1:
		return ("Classe A")
	elif classe == 2:
		return ("Classe B")
	elif classe == 3:
		return ("Classe C")
	elif classe == 4:
		return ("Classe D")
	elif classe == 5:
		return ("Classe E")	
	else:
		return ("Endere�o Inv�lido")

def telaInicial():
	limparTela()
	mascara = '255.0.0.0'

	while True:
		print ('1 - Calcular faixa de subredes')
		print ('2 - Encontrar faixa de endere�os para uma subrede espec�fica')
		print ('3 - Calcular quantidade de subredes')
		print ('4 - Calcular quantidade de hosts por subrede')
		print ('5 - Verificar classe do endere�o IP')
		print ('6 - Sair')
				
		opcao = input('\t\tDigite a op��o Desejada:')
		
		if opcao.isdigit():
			opcao = int(opcao)
		else:
			limparTela()
			continue	

		if opcao == 6:
			limparTela()
			print ('Saindo')
			break
		elif opcao >= 6:
			limparTela()
			continue
		
		limparTela()
		ip = input("Digite o endere�o IP da rede:")

		if opcao != 5:
			mascara = input('Digite a m�scara:')

		if validaIP(ip) != 1 or validaIP(mascara) != 1:	
			if opcao == 1:
				calculaFaixaEnderecosSubredes(ip,mascara)
			elif opcao == 2:
				calculaSubredeEspecifica(ip, mascara)
			elif opcao == 3:
				print(calculaQuantidadeSubredes(ip, mascara), 'Subrede(s)')
			elif opcao == 4:
				print(calculaQuantidadeHostSubrede(ip, mascara), 'Host(s)')		
			elif opcao == 5:
				print (qualClasse(ip))
		else:
			print ('Endere�o Inv�lido')
		
		voltar = input('Deseja voltar a tela inicial (S/N):').upper()
		limparTela()
				
		if voltar == 'N':
			limparTela()
			print ('Saindo...')
			break

telaInicial()