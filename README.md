Trabalho da P1 de Algoritmos e Estruturas de Dados I
Professor: Dimmy Magalhães
Aluno: Luiz Felipe Lucena Guimarães (0030938)

Link Repositório: https://github.com/luiz-lucena/PythonProject

Descrição do Projeto
Este projeto implementa um escalonador de processos com múltiplas filas de prioridade (alta, média, baixa), prevenção de inanição e suporte a bloqueio por recurso (DISCO). Nenhuma estrutura de dados pronta foi utilizada, todas as listas são implementadas manualmente via nós encadeados.

Instruções de Execução
Certifique-se de ter o Python 3 instalado!
Abra o terminal dentro da pasta do projeto e execute o comando: python escalonador.py input.csv
O programa lerá os processos de input.csv e simulará a execução ciclo a ciclo, imprimindo o estado no console.

Dependências
Não há bibliotecas externas. O projeto utiliza apenas a biblioteca padrão do Python.

Formato do Arquivo de Entrada (CSV)
Cada linha corresponde a um processo, no formato: id,nome,prioridade,ciclos_necessarios,recurso_necessario
Exemplo: 1,P1,1,3,
         2,P2,1,2,DISCO
         3,P3,2,4,

Agora é só salvar o arquivo!