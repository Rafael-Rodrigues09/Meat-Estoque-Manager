import requests

def request(url, method, token, data=None):
    try:
        if not url:
            return False, "Erro: url invalida"
        if not token:
            return False, "Erro: token invalido"
        if method == 'GET':
            response = requests.get(url, timeout=(3.05, 10), headers=token)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=(3.05, 15), headers=token)
        else:
            return False, "Erro: Metodo invalido"
        response.raise_for_status()
        return True, response.json()        
    except requests.exceptions.Timeout:
        return False, "Erro: O servidor demorou muito para responder."
    except requests.exceptions.ConnectionError:
        return False, "Erro: Falha de conexão com a internet."
    except requests.exceptions.HTTPError as e:
        return False, f"Erro da API: {e.response.status_code}. Detalhe: {e.response.json().get('detail')}"
    except requests.exceptions.RequestException as e:
        return False, f"Erro inesperado de rede: {e}"
    except ValueError:
        return False, "Erro: O servidor não devolveu um JSON válido."