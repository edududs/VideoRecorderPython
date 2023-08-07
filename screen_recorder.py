import cv2
import numpy as np
import pyautogui


class ScreenRecorder:
    def __init__(
        self, filename: str, resolution=(1920, 1080), codec="mp4v", fps: float = 30.0
    ) -> None:
        """
        Inicializa um objeto ScreenRecorder.

        Parâmetros:
            filename (str): Nome do arquivo de saída para salvar o vídeo gravado.
            resolution (tuple, opcional): Resolução do vídeo (largura, altura). Padrão é (1920, 1080).
            codec (str, opcional): Código do codec para o formato de vídeo. Padrão é "mp4v".
            fps (float, opcional): Taxa de quadros por segundo do vídeo. Padrão é 30.0.
        """
        self.filename = filename
        self.resolution = resolution
        # Verifica se o codec é suportado pelo OpenCV
        supported_codecs = ["mp4v", "xvid", "h264", "avc1", "vp9"]
        if codec not in supported_codecs:
            raise ValueError(
                f"Codec '{codec}' não é suportado pelo OpenCV. Escolha um dos seguintes codecs: {supported_codecs}"
            )
        self.codec = cv2.VideoWriter_fourcc(*codec)
        self.fps = fps
        self.out = None

    def set_fps(self, fps: float):
        """
        Atualiza o valor do FPS do vídeo.

        Parâmetros:
            fps (float): Novo valor do FPS.
        """
        self.fps = fps

    def start_recording(self):
        """
        Inicia a gravação do vídeo, criando o objeto VideoWriter.
        """
        self.out = cv2.VideoWriter(self.filename, self.codec, self.fps, self.resolution)

    def stop_recording(self):
        """
        Para a gravação do vídeo e libera os recursos.
        """
        if self.out is not None:
            self.out.release()

    def capture_frame(self):
        """
        Captura o quadro da tela e o converte para o formato RGB.

        Retorna:
            frame (numpy.array): Quadro capturado em formato RGB.
        """
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
