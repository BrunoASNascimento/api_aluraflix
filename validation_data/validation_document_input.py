import requests

__all__ = ['VideoValidation']


class VideoValidation:
    def __init__(self,  titulo, descricao, url):

        # self.id = id
        self.titulo = self._is_valid_titulo(titulo)
        self.descricao = self._is_valid_descricao(descricao)
        self.url = self._is_valid_url(url)

    def _is_valid_titulo(self, titulo):
        if (len(titulo) > 0) and (len(titulo) <= 1024):
            return titulo
        raise ValueError(
            "Titulo cannot exceed 1024 characters and cannot be null.")

    def _is_valid_descricao(self, descricao):
        if (len(descricao) > 0) and (len(descricao) <= 2048):
            return descricao
        raise ValueError(
            "Descricao cannot exceed 2048 characters and cannot be null.")

    def _is_valid_url(self, url):
        try:
            response = requests.request("GET", url)
            if response.status_code != 200:
                raise ValueError(
                    f"Url not work, status {response.status_code}.")
        except Exception as error:
            raise ValueError(f"Url not work, error: {error}.")
        return url
