# Importa a biblioteca requests, que é usada para fazer requisições HTTP para APIs

import requests

# Define o caminho do arquivo que  contém o texto a ser resumido, aqui usei as pastas do meu computador (não sei o por que de não ter conseguido usar .txt, unica forma que deu certo foi colocando o caminho direto das pastas)

TOKEN = "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"
ARQUIVO = "/Users/vitoriaayres/PycharmProjects/PythonProject3/bbcnoticia.txt"
MODELOS = {
    "Inglês": "facebook/bart-large-cnn",
    "Português": "pierreguillou/t5-base-pt-sum-text-summary"
}


def ler_arquivo():
    # Bloco try/except para ler o arquivo de texto,  uso o except para a saída de erro em leitura
    try:
        # Abre o arquivo especificado em ARQUIVO no modo leitura ('r')
        # Usa o gerenciador de contexto 'with' para garantir que o arquivo será fechado corretamente
        with open(ARQUIVO, 'r') as arquivo:
            # Lê todo o conteúdo do arquivo e armazena na variável texto
            texto = arquivo.read()
            # Imprime o número de caracteres lidos do arquivoo
            print(f"Texto lido: {len(texto)} caracteres")
            # Retorna o conteúdo do arquivo
            return texto
            
    # Captura qualquer exceção  que possa ocorrrer durante a leitura do arquivo
    # (por exemplo: arquivo não existe, sem permissão,, etc)
    except Exception as erro:
        # Imprime mensagem de erro específica
        print(f"Erro ao ler arquivo: {erro}")
        # Retorna None para   indicar que a leitura falhou
        return None


def gerar_resumo(texto, modelo, idioma):
    resposta = requests.post(
        f"https://api-inference.huggingface.co/models/{modelo}",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"inputs": texto}
    )

    try:
        # Aqui defini os parâmetros necessários para gerar um bom resumo
        if resposta.status_code == 200:
            dados = resposta.json()
            resumo = dados[0]['summary_text']
            print(f"\nResumo em {idioma}:")
            print(f"{resumo}\n{'-' * 50}\n")
        else:
            print(f"Erro no {idioma}: {resposta.text}")  
    # Captura e trata qualquer exceção que ocorra durante o processamento da resposta
    except Exception as erro:
        # Imprime mensagem de erro detalhada, incluindo o tipo específico do erro
        print(f"Erro ao processar resposta: {erro}")


def main():
    # Função principal que coordena todo o fluxo do programa
    
    # Tenta ler o conteúdo do arquivo
    texto = ler_arquivo()
    
    # Se conseguiu ler o arquivo com sucesso
    if texto:
        # Itera sobre cada par de idioma   e modelo definido no dicionário MODELOS
        for idioma, modelo in MODELOS.items():
            # Gera o resumo para cada idioma usando seu respectivo modelo
            gerar_resumo(texto, modelo, idioma)


# Verifica se o script está sendo executado diretamente (não importado como módulo)
if __name__ == "__main__":
    # Chama a função principal para iniciar o programa
    main()
