#!/usr/bin/env python3
import sys
import os
from typing import Optional

# ----------------------
# Estruturas de dados
# ----------------------

# Classe que representa um processo
class Processo:
    def __init__(self, pid: int, nome: str, prioridade: int, ciclos: int, recurso: Optional[str]):
        self.id = int(pid) # identificador único
        self.nome = nome # nome do processo
        self.prioridade = int(prioridade)  # 1-Alta,2-Média,3-Baixa
        self.ciclos_necessarios = int(ciclos) #ciclos restantes para terminar
        self.recurso_necessarios = recurso if recurso and recurso.strip() != '' else None # recursos necessários
        self.ja_solicitou_disco = False # flag para controlar primeiro acesso ao DISCO

    def __repr__(self):
        return f"P(id={self.id},nome={self.nome},pri={self.prioridade},ciclos={self.ciclos_necessarios},rec={self.recurso_necessarios})"

# Nó da lista encadeada (cada nó guarda um processo)
class Node:
    def __init__(self, processo: Processo):
        self.processo = processo
        self.next = None # ponteiro para o próximo nó

# Implementação da lista de processos (Encadeada)
class ListaDeProcessos:
    def __init__(self, nome: str):
        self.head = None # primeiro nó
        self.tail = None # último nó
        self.size = 0 # quantidade de elementos
        self.nome = nome # nome da fila (Alta, Média, Baixa, Bloqueados)

    def append(self, processo: Processo):
        # Adiciona um processo ao final da lista
        node = Node(processo)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def pop_front(self) -> Optional[Processo]:
        # Remove e retorna o primeiro processo da lista
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        node.next = None
        self.size -= 1
        return node.processo

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
            procs.append(f"{p.nome}(id={p.id},c={p.ciclos_necessarios})")
            cur = cur.next
        return " -> ".join(procs) if procs else "(vazia)"


# ----------------------
# Escalonador (gerencia as listas de prioridades e bloqueados)
# ----------------------
class Scheduler:
    def __init__(self):
        # filas de prioridades e bloqueados, uma lista para cada prioridade
        self.lista_alta = ListaDeProcessos("Alta")
        self.lista_media = ListaDeProcessos("Média")
        self.lista_baixa = ListaDeProcessos("Baixa")
        self.lista_bloqueados = ListaDeProcessos("Bloqueados") # lista de bloqueados
        self.contador_ciclos_alta = 0 # usado para prevenção de inanição
        # logs
        self.ciclo_atual = 0 # contador de ciclos

    def carregar_processos_de_arquivo(self, path: str):
        # Lê processos de um CSV e adiciona nas filas corretas
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
                if prioridade == 1:
                    self.lista_alta.append(p)
                elif prioridade == 2:
                    self.lista_media.append(p)
                else:
                    self.lista_baixa.append(p)

    def filas_vazias(self):
        # Retorna True se todas as filas estão vazias
        return (
            self.lista_alta.is_empty()
            and self.lista_media.is_empty()
            and self.lista_baixa.is_empty()
            and self.lista_bloqueados.is_empty()
        )

    def imprimir_estado(self):
        print(f"Filas no início do ciclo {self.ciclo_atual}:")
        print(f"  Alta: {self.lista_alta}")
        print(f"  Média: {self.lista_media}")
        print(f"  Baixa: {self.lista_baixa}")
        print(f"  Bloqueados: {self.lista_bloqueados}")
        print(f"  contador_ciclos_alta = {self.contador_ciclos_alta}")

    def executarCicloDeCPU(self):
        self.ciclo_atual += 1
        # 1) desbloqueia o processo mais antigo dos bloqueados
        desbloqueado = self.lista_bloqueados.pop_front()
        if desbloqueado is not None:
            if desbloqueado.prioridade == 1:
                self.lista_alta.append(desbloqueado)
            elif desbloqueado.prioridade == 2:
                self.lista_media.append(desbloqueado)
            else:
                self.lista_baixa.append(desbloqueado)
            print(f"[ciclo {self.ciclo_atual}] Desbloqueio: {desbloqueado.nome}(id={desbloqueado.id}) re-enfileirou na prioridade {desbloqueado.prioridade}")

        # 2) decidir qual processo executar
        escolhido = None
        fonte = None  # "Alta","Média","Baixa"

        # prevenção de inanição (depois de 5 execuções de alta, força média/baixa)
        if self.contador_ciclos_alta >= 5:
            escolhido = self.lista_media.pop_front()
            fonte = "Média"
            if escolhido is None:
                escolhido = self.lista_baixa.pop_front()
                fonte = "Baixa" if escolhido else None
            if escolhido is not None:
                print(f"[ciclo {self.ciclo_atual}] Regra anti-inanição aplicada. Selecionado da fila {fonte}: {escolhido.nome}(id={escolhido.id})")
                self.contador_ciclos_alta = 0

        # execução padrão, se não tiver aplicado anti-starvation
        if escolhido is None:
            escolhido = self.lista_alta.pop_front()
            fonte = "Alta"
            if escolhido is None:
                escolhido = self.lista_media.pop_front()
                fonte = "Média"
            if escolhido is None:
                escolhido = self.lista_baixa.pop_front()
                fonte = "Baixa" if escolhido else None
            if escolhido is not None:
                print(f"[ciclo {self.ciclo_atual}] Selecionado da fila {fonte}: {escolhido.nome}(id={escolhido.id})")

        # Se não há nenhum processo, fim da simulação
        if escolhido is None:
            print(f"[ciclo {self.ciclo_atual}] Nenhum processo disponível para executar.")
            return False  # nada a ser executado

        # 3) gerenciamento de recurso DISCO
        if escolhido.recurso_necessarios == "DISCO" and not escolhido.ja_solicitou_disco:
            escolhido.ja_solicitou_disco = True
            self.lista_bloqueados.append(escolhido)
            print(f"[ciclo {self.ciclo_atual}] Processo {escolhido.nome}(id={escolhido.id}) solicitou DISCO pela primeira vez -> movido para bloqueados")
            return True

        # 4) executar
        escolhido.ciclos_necessarios -= 1
        print(f"[ciclo {self.ciclo_atual}] Executando {escolhido.nome}(id={escolhido.id}) -> ciclos restantes: {escolhido.ciclos_necessarios}")

        # contador de execução
        if fonte == "Alta":
            self.contador_ciclos_alta += 1
        else:
            self.contador_ciclos_alta = 0

        # 5) verificar término
        if escolhido.ciclos_necessarios <= 0:
            print(f"[ciclo {self.ciclo_atual}] Processo {escolhido.nome}(id={escolhido.id}) terminou execução e sai do sistema")
        else:
            if escolhido.prioridade == 1:
                self.lista_alta.append(escolhido)
            elif escolhido.prioridade == 2:
                self.lista_media.append(escolhido)
            else:
                self.lista_baixa.append(escolhido)

        return True


# ----------------------
# Função principal CLI
# ----------------------
def main():
    if len(sys.argv) < 2:
        print("Uso: python scheduler.py input.csv [max_cycles]")
        sys.exit(1)
    path = sys.argv[1]
    max_cycles = int(sys.argv[2]) if len(sys.argv) >= 3 else 10000

    s = Scheduler()
    s.carregar_processos_de_arquivo(path)

    ciclos = 0
    print("=== Iniciando simulação do escalonador ===")
    while ciclos < max_cycles and not s.filas_vazias():
        s.imprimir_estado()
        ok = s.executarCicloDeCPU()
        ciclos += 1
        print("---")
        if not ok and s.filas_vazias():
            break

    print(f"=== Simulação finalizada após {ciclos} ciclos ===")


if __name__ == "__main__":
    main()
