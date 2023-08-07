import threading
import tkinter as tk
from tkinter import ttk

import cv2

from screen_recorder import ScreenRecorder


class GravadorApp:
    def __init__(self, root) -> None:
        """
        Inicializa a interface gráfica para o Gravador de Tela.

        Parâmetros:
            root (tk.Tk): Instância da janela principal tkinter.
        """
        self.root = root
        self.root.title("Gravador de Tela")

        # Define o tamanho menor da janela
        window_width = 400
        window_height = 90
        # Centraliza a janela na tela
        self.root.pack_propagate(False)
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Criar uma instância do ScreenRecorder
        self.extensao = ".mp4"
        self.screen_recorder = ScreenRecorder(f"gravacção{self.extensao}")

        # Criação do botão "Iniciar Gravação"
        self.btn_iniciar = tk.Button(
            self.root, text="Iniciar Gravação", command=self.iniciar_gravacao
        )
        self.btn_iniciar.grid(
            row=0, column=0, padx=10, pady=(10, 0)
        )  # Posiciona na coluna 0 da primeira linha

        # Criação do botão "Parar Gravação"
        self.btn_parar = tk.Button(
            self.root, text="Parar Gravação", command=self.parar_gravacao
        )
        self.btn_parar.grid(
            row=0, column=1, padx=10, pady=(10, 0)
        )  # Posiciona na coluna 1 da primeira linha

        # Criação da variável de controle para armazenar o valor do FPS selecionado
        self.fps_var = tk.StringVar()
        self.fps_var.set("30")  # Valor padrão é 30 FPS

        # Criação do menu de seleção de opções de FPS
        self.combobox_fps = ttk.Combobox(
            self.root, textvariable=self.fps_var, values=["15", "30", "60"]
        )
        self.combobox_fps.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(0, 10)
        )  # Posiciona na segunda linha, coluna 0, ocupando duas colunas

        # Vincula o evento <<ComboboxSelected>> para chamar o método trocar_fps quando o valor da caixa de seleção for alterado
        self.combobox_fps.bind("<<ComboboxSelected>>", lambda event: self.trocar_fps())
        
        # Criação da variável de controle para armazenar a extensão selecionada
        self.extensao_var = tk.StringVar()
        self.extensao_var.set(".mp4")  # Valor padrão é .mp4

        # Criação do menu de seleção de opções de extensão
        self.combobox_extensao = ttk.Combobox(
            self.root, textvariable=self.extensao_var, values=[".avi", ".mp4"]
        )
        self.combobox_extensao.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10))  # Posiciona na terceira linha, coluna 0, ocupando duas colunas

        # Vincula o evento <<ComboboxSelected>> para chamar o método trocar_extensao quando o valor da caixa de seleção for alterado
        self.combobox_extensao.bind("<<ComboboxSelected>>", lambda event: self.trocar_extensao())

        # Alinha os botões verticalmente no canto direito
        self.root.pack_propagate(False)
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        self.btn_iniciar.pack_configure(anchor="e")
        self.btn_parar.pack_configure(anchor="e")

        self.recording = False
        self.thread = None

    def trocar_fps(self, event=None):
        """
        Atualiza o valor do FPS na instância de ScreenRecorder quando o usuário selecionar um novo valor na caixa de seleção.
        """
        fps = int(self.fps_var.get())
        self.screen_recorder.set_fps(fps)

    def trocar_extensao(self, event=None):
        """
        Atualiza a extensão do arquivo de saída na instância de ScreenRecorder quando o usuário selecionar uma nova extensão na caixa de seleção.
        """
        extensao = self.extensao_var.get()
        self.extensao = extensao

    def iniciar_gravacao(self):
        """
        Inicia a gravação do vídeo e cria a thread para atualizar o quadro.
        """
        # Abre o menu de opções de FPS antes de iniciar a gravação

        if not self.recording:
            self.recording = True
            self.thread = threading.Thread(target=self.atualizar_quadro)
            self.thread.start()

    def parar_gravacao(self):
        """
        Interrompe a gravação do vídeo e aguarda a finalização da thread antes de fechar a janela.
        """
        if self.recording:
            self.recording = False

    def atualizar_quadro(self):
        """
        Atualiza continuamente o quadro capturado e exibe-o na janela "Live" até a gravação ser interrompida.
        """
        self.screen_recorder.start_recording()

        while self.recording:
            frame = self.screen_recorder.capture_frame()

            # Exibe o quadro capturado na janela "Live" (opcional, apenas para visualização em tempo real)
            cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Live", 480, 270)
            cv2.imshow("Live", frame)

            self.screen_recorder.out.write(frame)

            # Verifica se a tecla 'q' foi pressionada
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.parar_gravacao()

        cv2.destroyAllWindows()
        self.screen_recorder.stop_recording()


if __name__ == "__main__":
    root = tk.Tk()
    app = GravadorApp(root)
    root.mainloop()
