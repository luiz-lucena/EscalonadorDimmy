Relatório de Análise

1. Justificativa de Design

As listas encadeadas foram escolhidas por permitirem inserções e remoções eficientes no início e no fim (O(1)), que são operações críticas para o escalonador. Isso garante que a manipulação de processos nas filas seja rápida e previsível.

2. Complexidade (Big-O)

Inserir no final da lista: O(1)

Remover do início da lista: O(1)

Verificar se está vazia: O(1)

Percorrer a lista para exibir estado: O(n)
Essas operações tornam a solução eficiente para o uso contínuo do escalonador.

3. Anti-Inanição

A lógica de anti-inanição garante que, após 5 execuções consecutivas de processos de alta prioridade, um processo de prioridade inferior (média ou baixa) obrigatoriamente seja executado. Isso evita que processos de menor prioridade fiquem indefinidamente sem CPU. Sem essa regra, haveria risco de starvation, especialmente em cenários com muitas tarefas críticas.

4. Bloqueio

Um processo que precisa do recurso “DISCO” é transferido para a lista de bloqueados na primeira vez em que solicita o recurso. A cada ciclo, o processo mais antigo da lista de bloqueados é desbloqueado e retorna ao final da fila de sua prioridade original. Assim, simulamos o comportamento de espera por I/O típico de sistemas reais.

5. Ponto Fraco e Possível Melhoria

O principal gargalo do escalonador está na necessidade de percorrer listas para exibição do estado em cada ciclo (O(n)). Em cenários com muitos processos, isso pode ser custoso. Uma melhoria teórica seria manter estruturas adicionais de índice ou buffers de log, permitindo exibir o estado mais rapidamente sem percorrer todas as listas a cada ciclo.
