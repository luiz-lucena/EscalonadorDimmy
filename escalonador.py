#!/usr/bin/env python3
import sys
import os
from typing import Optional

# ----------------------
# Estruturas de dados
# ----------------------

class Processo:
    def __init__(self, pid: int, nome: str, prioridade: int, ciclos: int, recurso: Optional[str]):
        self.id = int(pid)
        self.nome = nome
        self.prioridade = (int)prioridade # 1-Alta,2-Média,3-Baixa
        self.ciclos_necessarios = int(ciclos)
        self.recurso_necessarios = recurso if recurso and recurso.strip() != '' else None
        self.ja_solicitou_disco = False

    def __repr__(self):
            return f"P(id={self.id},nome={self.nome},pri={self.prioridade},ciclos={self.ciclos_necessarios},rec={self.recurso_necessarios})"

class Node:
        def __init__(self, processo: Processo):
                self.processo = processo
                self.next = None

class ListaDeProcessos:
        def __init__(self):
            self.head = Optional[Node] = None
            self.tail = Optional[Node] = None
            self.size = 0
            self.nome = nome

        def append(self, processo: Processo):
            node = Node(processo)
            if self.tail is None:
                self.head = node
                self.tail = node
            else:
                self.tail.next = node
                self.tail = node
            self.size += 1

        def pop_front(self) -> Optional[Processo]:
            if self.head is None:
                return None
            node = self.head
            self.head = node.next
            if self.head is None:
                self.tail = None
            node.next = None
            self.size -= 1
            return node.Processo

    def is_empty(self) -> bool:
        return self.size == 0

    def __len__(self):
        return self.size

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.processo
            cur = cur.next

    def __str__(self):
        procs = []
        cur = self.head
        while cur is not None:
            p = cur.processo
            procs.append(f"{p.nome}(id={p.id},c={ciclos_necessarios})")
            cur = cur.next
        return " -> ".join(procs) if procs else "(vazia)"

# ----------------------
# Escalonador
# ----------------------
class Scheduler
    def __init__(self):
        self.lista_alta = ListaDeProcessos("Alta")
        self.list_media = ListaDeProcessos("Média")
        self.lista_baixa = ListaDeProcessos("Baixa")
        self.lista_bloqueados = ListaDeProcessos("Bloqueados")
        self.contador_ciclos_alta = 0
        # logs
        self.ciclo_atual = 0

    def carregar_processos_de_arquivo(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # campos = id,nome,prioridade,ciclos,recurso
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 4:
                    continue
                pid = int(parts[0])
                nome = parts[1]
                prioridade = int(parts[2])
                ciclos = int(parts[3])
                recursos = parts[4] if len(parts) >= 5 else None
                p = Processo(pid, nome, prioridade, ciclos, recursos)
                if prioridade == 1
                    self.lista_alta.append(p)
                elif prioridade == 2:
                    self.list_media.append(p)
                else:
                    self.lista_baixa.append(p)
    def filas_vazias(self):
        return self.lista_alta.is_empty() and self.lista_media.is_empty() and self.lista_baixa.is_empty() and self.lista_bloqueados.is_empty()

    def imprimir_estado(self):
        print(f"Filas no início do ciclo {self.ciclo_atual}:")
        print(f"  Alta: {self.lista_alta}")
        print(f"  Média: {self.list_media}")
        print(f"  Baixa: {self.lista_baixa}")
        print(f"  Bloqueados: {self.lista_bloqueados}")
        print(f"  contador_ciclos_alta = {self.contador_ciclos_alta}")

    def executarCicloDeCPU(self):
        self.ciclo_atual += 1
        # 1) desbloqueia o processo mais antigo dos bloqueados
        desbloqueado = self.lista_bloqueados.pop_front()
        if desbloqueado is not None:
            # ao desbloquear, re-insere no final da lista original
            if desbloqueado.prioridade == 1:
                self.lista_alta.append(desbloqueado)
            elif desbloqueado.prioridade == 2:
                self.list_media.append(desbloqueado)
            else:
                self.lista_baixa.append(desbloqueado)
            print(f"[ciclo {self.ciclo_atual}] Desbloqueio: {desbloqueado.nome}(id={desbloqueado.id}) re-enfileirou na prioridade {desbloqueado.prioridade}")

            # 2) decidir qual processo executar
            escolhido = None
            fonte = None # "alta","media","baixa"

            # prevenção de inanição: se 5 altas executadas em sequência, executar uma média preferencialmente
            if self.contador_ciclos_alta >= 5:
                # ai ele tenta média
                escolhido = self.list_media.pop_front()
                fonte = "Média"
                if escolhido is None:
                    escolhido = self.lista_baixa.pop_front()
                    fonte = "Baixa" if escolhido else None
                if escolhido is not None:
                    print(f"[ciclo {self.ciclo_atual}] Regra anti-inanição aplicada. Selecionado da fila {fonte}: {escolhido.nome}(id={escolhido.id})")
                    self.contador_ciclos_alta = 0
            # execução padrão
            if escolhido is None:
                # prioridade alta
                escolhido = self.lista_alta.pop_front()
                fonte = "Alta"
                if escolhido is None
                    escolhido = self.list_media.pop_front()
                    fonte = "Média"
                if escolhido is None:
                    escolhido = self.lista_baixa.pop_front()
                    fonte = "Baixa" if escolhido else None
                if escolhido is not None:
                    print(f"[ciclo {self.ciclo_atual}] Selecionado da fila {fonte}: {escolhido.nome}(id={escolhido.id})")
            if escolhido is not None:
                print(f"[ciclo {self.ciclo_atual}] Nenhum processo disponível para executar.")
                return False # nada a ser executado

            # gerenciamento de recurso DISCO
            if escolhido.recurso_necessario == "DISCO" and not escolhido.ja_solicitou_disco:
                # primeira vez pedindo DISCO -> mover para bloqueados
                escolhido.ja_solicitou_disco = True
                self.lista_bloqueados.append(escolhido)
                print(f"[ciclo {self.ciclo_atual}] Processo {escolhido.nome}(id={escolhido.id}) solicitou DISCO pela primeira vez -> movido para bloqueados")
                # como ele não executou, não alterar contador de altas (não conta como execução)
                return True

            # 4) executar: diminui ciclos em 1
            escolhido.ciclos_necessarios -= 1
            print(f"[ciclo {self.ciclo_atual}] Executando {escolhido.nome}(id={escolhido.id}) -> ciclos restantes: {escolhido.ciclos_necessarios}")

            # atualizar contador de execução alta
            if fonte == "Alta":
                self.contador_ciclos_alta += 1
            else:
                # ai qualquer execução que não seja alta reinicia o computador
                self.contador_ciclos_alta = 0
            # 5) se terminou, reportar. se não terminou, re-enfileirar no final da lista de origem
            if escolhido.ciclos_necessarios <= 0:
                print(f"[ciclo {self.ciclo_atual}] Processo {escolhido.nome}(id={escolhido.id}) terminou execução e sai do sistema")
            else:
                # ai aqui re-insere no final da lista de prioridade original
                if escolhido.prioridade == 1:
                    self.lista_alta.append(escolhido)
                elif escolhido.prioridade == 2:
                    self.list_media.append(escolhido)
                else:
                    self.lista_baixa.append(escolhido)

            return True

# ----------------------
# Função principal CLI
# ----------------------