"""
Script de Demonstração: Scanner de Imagens com YOLO e Tkinter.
Desenvolvido para prototipagem rápida, fins educacionais e deploy leve.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
import spacy

class YoloScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scanner com Yolo")
        self.root.geometry("800x600")
        
        # Centralizar a janela na tela
        self.center_window()
        
        # Carregar modelo YOLO (usando um modelo leve padrão do Ultralytics)
        try:
            self.model = YOLO("yolov8n.pt")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o modelo YOLO: {e}")
            
        # Carregar modelo do Spacy para processamento de texto complementar
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except Exception:
            self.nlp = None

        self.setup_ui()

    def center_window(self):
        """Centraliza a janela principal na tela do usuário."""
        self.root.update_idletasks()
        width = 800
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        """Configura os elementos da interface gráfica (Tkinter)."""
        # Título da Aplicação
        self.title_label = tk.Label(self.root, text="Scanner de Imagens com YOLO", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Botão para selecionar imagem
        self.btn_load = tk.Button(
            self.root, 
            text="Carregar Imagem", 
            command=self.load_image, 
            font=("Arial", 12), 
            bg="#4CAF50", 
            fg="white",
            relief="raised",
            padx=10,
            pady=5
        )
        self.btn_load.pack(pady=10)

        # Área de exibição da imagem
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="#2e2e2e", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Caixa de texto para mostrar o que existe na imagem
        self.text_output = tk.Text(self.root, height=8, width=80, font=("Courier", 10))
        self.text_output.pack(pady=10)
        self.text_output.insert(tk.END, "Aguardando o carregamento de uma imagem para detecção...\n")

    def load_image(self):
        """Abre o diálogo de arquivos para selecionar a imagem a ser escaneada."""
        file_path = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.process_image(file_path)

    def process_image(self, file_path):
        """Realiza a inferência com YOLO na imagem selecionada e atualiza a interface."""
        try:
            # Exibir a imagem redimensionada no canvas do Tkinter
            pil_img = Image.open(file_path)
            pil_img_resized = pil_img.resize((400, 300))
            self.photo = ImageTk.PhotoImage(pil_img_resized)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # Executar inferência do modelo YOLO
            results = self.model(file_path)
            
            # Extrair objetos detectados
            detected_objects = []
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = self.model.names[cls_id]
                    detected_objects.append(f"- {class_name} (Confiança: {conf:.2f})")

            # Atualizar caixa de texto com os resultados
            self.text_output.delete("1.0", tk.END)
            if detected_objects:
                self.text_output.insert(tk.END, "Objetos detectados na imagem:\n" + "\n".join(detected_objects))
                
                # Demonstração de uso do Spacy com o resumo textual gerado
                if self.nlp:
                    summary_text = f"Total de {len(detected_objects)} elementos encontrados."
                    doc = self.nlp(summary_text)
                    tokens = [token.text for token in doc if token.is_alpha]
                    self.text_output.insert(tk.END, f"\n\nAnálise Textual (Spacy): {tokens}")
            else:
                self.text_output.insert(tk.END, "Nenhum objeto conhecido foi detectado nesta imagem.")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar a imagem: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YoloScannerApp(root)
    root.mainloop()