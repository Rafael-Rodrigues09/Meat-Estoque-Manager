# Nativas Grill - Gerenciador de Estoque

## Contexto Operacional
O controle de estoque no setor de carnes em ambientes de alta demanda é tradicionalmente feito em papel. Esse método manual gera perda de histórico, inconsistência de dados e falhas de auditoria. Este projeto foi desenvolvido para substituir a prancheta física por um sistema digital, persistente e de fácil acesso para os operadores locais.

## Arquitetura do Sistema
A aplicação foi construída com foco em eficiência, dispensando frameworks complexos de front-end para priorizar a integridade dos dados e a lógica de negócios.

- **Camada de Persistência:** Utiliza estrutura JSON para I/O (leitura e escrita) direto em disco, mantendo o estado da aplicação leve e seguro contra quedas de energia ou reinicializações.
- **Lógica de Estado:** O algoritmo processa as entradas de "Uso" e "Sobra" e as anexa em uma tabela em tempo real. 
- **Rotina EOD (End of Day):** Função automatizada de fechamento de turno. O sistema compila os dados do dia, gera um arquivo de backup em disco com timestamp (data atual) e executa a limpeza do banco de dados principal para o turno seguinte.
- **Interface (Web):** Renderização de interface via Streamlit, permitindo que a aplicação seja acessada por smartphones na rede local sem necessidade de linguagens de marcação ou estilização CSS.
