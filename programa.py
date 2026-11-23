import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math, random, os, shutil, time

                                                                  
                                     
                                                                  
                                                                  

                                                                              
BG = "#F3F6FC"
SURFACE = "#FFFFFF"
CARD = "#FFFFFF"
CARD2 = "#EAF0F8"
BLUE = "#4263EB"
CYAN = "#087F8C"
GREEN = "#16845B"
ORANGE = "#B96B08"
PURPLE = "#7652A8"
RED = "#C43D55"
WHITE = "#17243A"
MUTED = "#64748B"
INK = "#17243A"
BORDER = "#DCE4F0"

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=BG, **kwargs)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0)
        self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vbar.pack(side="right", fill="y")
        self.inner.bind("<Configure>", self._configure_inner)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.canvas.bind_all("<MouseWheel>", self._wheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-3, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(3, "units"))
    def _configure_inner(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def _configure_canvas(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)
    def _wheel(self, event):
        if self.winfo_ismapped():
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

class ComplexosApp:
    def __init__(self, root):
        self.root = root
        root.title("Números Complexos")
        root.geometry("1240x860")
        root.minsize(820, 620)
        root.configure(bg=BG)
        self.steps = [
            ("Abertura: um problema impossível", self.page_opening, 2),
            ("Cardano e as equações cúbicas", self.page_cardano, 3),
            ("Bombelli: operar com o estranho", self.page_bombelli, 3),
            ("Da estranheza à linguagem dos complexos", self.page_history, 3),
            ("Por que os reais não bastam?", self.page_problem, 5),
            ("Definindo a unidade imaginária", self.page_i, 4),
            ("Potências de i e periodicidade", self.page_powers, 4),
            ("Forma algébrica: duas componentes", self.page_algebraic, 5),
            ("Igualdade e classificação", self.page_components, 4),
            ("O plano de Argand-Gauss", self.page_plane, 5),
            ("Módulo: distância e Pitágoras", self.page_modulus, 5),
            ("Conjugado: simetria no plano", self.page_conjugate, 4),
            ("Adição e subtração", self.page_addsub, 5),
            ("Multiplicação algébrica", self.page_multiply, 5),
            ("Multiplicação como rotação e escala", self.page_rotation, 5),
            ("Divisão e racionalização", self.page_division, 5),
            ("Forma polar: módulo e argumento", self.page_polar, 5),
            ("Conversão entre as formas", self.page_conversion, 4),
            ("Aplicações: ondas e eletricidade", self.page_applications, 4),
            ("Síntese guiada", self.page_synthesis, 4),
            ("Prática orientada", self.page_challenge, 5),
            ("Laboratório de exploração", self.page_lab, 5),
            ("Jogo em grupo: batalha dos complexos", self.page_game, 6),
        ]
        self.index = 0
        self.score = 0
        self.question_no = 0
        self.bank_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banco_imagens_complexos")
        os.makedirs(self.bank_dir, exist_ok=True)
        self.images, self.slides, self.slide_index = [], [], 0
        self.photo = None
        self.mode = "lesson"
        self.build_shell()
        self.show_step()

    def build_shell(self):
                                                                       
        self.header = tk.Frame(self.root, bg=BG)
        self.header.pack(fill="x", padx=26, pady=(17, 8))
        brand = tk.Frame(self.header, bg=BG)
        brand.pack(side="left", fill="x", expand=True)
        tk.Label(brand, text="MATEMÁTICA", bg=BG, fg=CYAN,
                 font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(brand, text="Números complexos", bg=BG, fg=INK,
                 font=("Arial", 24, "bold")).pack(anchor="w", pady=(2, 0))
        tk.Label(brand, text="Uma jornada visual pela álgebra e pela geometria de ℂ",
                 bg=BG, fg=MUTED, font=("Arial", 10)).pack(anchor="w", pady=(1, 0))
        actions = tk.Frame(self.header, bg=BG)
        actions.pack(side="right", anchor="center")
                                                                               
        self.timer_started = None
        self.timer_elapsed = 0
        timer_box = tk.Frame(actions, bg=BG)
        timer_box.pack(side="right", padx=(0, 12))
        self.timer_label = tk.Label(timer_box, text="00:00:00", bg=BG, fg=CYAN,
                                    font=("Arial", 16, "bold"))
        self.timer_label.pack(side="left", padx=(0, 7))
        self.timer_button = self.button(timer_box, "▶  INICIAR", self.start_timer, GREEN)
        self.timer_button.pack(side="left")
        self.button(actions, "▣  BANCO DE IMAGENS", self.open_bank, CARD2).pack(side="right", padx=(8, 0))
        self.button(actions, "⌂  AULA", self.return_lesson, BLUE).pack(side="right")

        separator = tk.Frame(self.root, bg=BORDER, height=1)
        separator.pack(fill="x", padx=26, pady=(2, 10))
        status = tk.Frame(self.root, bg=BG)
        status.pack(fill="x", padx=28, pady=(0, 5))
        self.stage_label = tk.Label(status, text="", bg=BG, fg=MUTED,
                                    font=("Arial", 9, "bold"), anchor="w")
        self.stage_label.pack(side="left")
        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("TProgressbar", troughcolor="#E2E8F0", background=BLUE,
                        bordercolor=BG, lightcolor=BLUE, darkcolor=BLUE, thickness=7)
        self.progress = ttk.Progressbar(self.root, maximum=len(self.steps), mode="determinate")
        self.progress.pack(fill="x", padx=28, pady=(2, 9))

                                                                             
        self.nav = tk.Frame(self.root, bg=BG, highlightthickness=1, highlightbackground=BORDER)
        self.nav.pack(side="bottom", fill="x", padx=26, pady=(7, 14))
        self.prev_btn = self.button(self.nav, "←  VOLTAR", self.previous, CARD2)
        self.prev_btn.pack(side="left", padx=8, pady=7)
        self.next_btn = self.button(self.nav, "PRÓXIMA ETAPA  →", self.next, BLUE)
        self.next_btn.pack(side="right", padx=8, pady=7)
        self.scroll = ScrollableFrame(self.root)
        self.scroll.pack(fill="both", expand=True, padx=22, pady=(0, 4))
        self.area = self.scroll.inner

    def start_timer(self):
        if self.timer_started is None:
            self.timer_started = time.monotonic()
            self.timer_button.config(text="●  EM ANDAMENTO", state="disabled")
            self.update_timer()

    def update_timer(self):
        elapsed = self.timer_elapsed
        if self.timer_started is not None:
            elapsed += time.monotonic() - self.timer_started
        total = int(elapsed)
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(250, self.update_timer)

    def clear(self):
        for w in self.area.winfo_children(): w.destroy()
        self.scroll.canvas.yview_moveto(0)

    def show_step(self):
        self.mode = "lesson"
        self.clear()
        name, fn, minutes = self.steps[self.index]
        self.stage_label.config(text=f"ETAPA {self.index+1:02d}/{len(self.steps):02d}  •  {name.upper()}")
        self.progress.pack(fill="x", padx=22, pady=(3,7))
        self.progress.configure(maximum=len(self.steps), value=self.index+1)
        self.nav.pack(side="bottom", fill="x", padx=22, pady=(7,13))
        self.prev_btn.config(command=self.previous, state="normal" if self.index else "disabled")
        self.next_btn.config(command=self.next, text="CONCLUIR AULA  ✓" if self.index == len(self.steps)-1 else "PRÓXIMO BLOCO  →")
        self.scroll.canvas.yview_moveto(0)
        fn()

    def previous(self):
        if self.mode == "lesson" and self.index > 0:
            self.index -= 1; self.show_step()
    def next(self):
        if self.mode == "lesson":
            if self.index < len(self.steps)-1:
                self.index += 1; self.show_step()
            else:
                messagebox.showinfo("Etapas concluídas", f"Você concluiu todas as etapas.\nTempo decorrido: {self.timer_label.cget('text')}\nPontuação no desafio: {self.score}.")

                                               
    def heading(self, title, subtitle):
        hero = tk.Frame(self.area, bg=BG)
        hero.pack(fill="x", padx=9, pady=(12, 9))
        tk.Label(hero, text=title, bg=BG, fg=INK, font=("Arial", 20, "bold"),
                 anchor="w", justify="left", wraplength=1050).pack(fill="x", pady=(0, 5))
        tk.Label(hero, text=subtitle, bg=BG, fg=MUTED, font=("Arial", 11),
                 anchor="w", justify="left", wraplength=1050).pack(fill="x")

    def card(self, title=None, accent=BLUE):
        shell = tk.Frame(self.area, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        shell.pack(fill="x", padx=9, pady=8)
        stripe = tk.Frame(shell, bg=accent, width=5)
        stripe.pack(side="left", fill="y")
        f = tk.Frame(shell, bg=CARD, padx=19, pady=15)
        f.pack(side="left", fill="both", expand=True)
        if title:
            title_row = tk.Frame(f, bg=CARD)
            title_row.pack(fill="x", pady=(0, 8))
            tk.Label(title_row, text=title, bg=CARD, fg=accent,
                     font=("Arial", 13, "bold")).pack(anchor="w")
        return f

    def para(self, parent, text, size=11, color=WHITE, bold=False):
        tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color,
                 font=("Arial", size, "bold" if bold else "normal"),
                 justify="left", anchor="w", wraplength=1000).pack(fill="x", pady=4)

    def formula(self, parent, text, color=ORANGE, size=21):
        box = tk.Frame(parent, bg="#F4F7FC", padx=13, pady=8,
                       highlightthickness=1, highlightbackground="#E5EBF4")
        box.pack(fill="x", pady=7)
        tk.Label(box, text=text, bg="#F4F7FC", fg=color,
                 font=("Cambria Math", size, "bold"), justify="left",
                 anchor="w", wraplength=1000).pack(fill="x")

    def button(self, parent, text, cmd, color=BLUE):
        dark_text = color in (BLUE, CYAN, GREEN, ORANGE)
        btn = tk.Button(parent, text=text, command=cmd, bg=color,
                        fg="#FFFFFF" if dark_text else INK,
                        activebackground=color, activeforeground="#FFFFFF" if dark_text else INK,
                        relief="flat", bd=0, font=("Arial", 9, "bold"),
                        padx=15, pady=9, cursor="hand2")
                                                    
        btn.bind("<Enter>", lambda _e: btn.config(relief="raised", bd=1))
        btn.bind("<Leave>", lambda _e: btn.config(relief="flat", bd=0))
        return btn
    def entry(self,parent,default="0",width=8):
        e=tk.Entry(parent,width=width,font=("Arial",12),justify="center",bg="#F7F9FC",fg=INK,
                   insertbackground=INK,relief="flat",highlightthickness=1,
                   highlightbackground=BORDER,highlightcolor=BLUE)
        e.insert(0,str(default)); e.pack(side="left",padx=5,ipady=5); return e
    @staticmethod
    def fmt(x):
        if abs(x)<1e-9: x=0
        if abs(x-round(x))<1e-9: return str(int(round(x)))
        return f"{x:.3f}".rstrip("0").rstrip(".")
    def cfmt(self,z):
        a,b=z.real,z.imag
        if abs(b)<1e-9:return self.fmt(a)
        if abs(a)<1e-9:return ("" if abs(b-1)<1e-9 else "-" if abs(b+1)<1e-9 else self.fmt(b))+"i"
        return self.fmt(a)+(" + " if b>0 else " − ")+(("" if abs(abs(b)-1)<1e-9 else self.fmt(abs(b)))+"i")
    def pair_inputs(self,parent,labels=("a","b","c","d"),defaults=(2,3,1,-1)):
        row=tk.Frame(parent,bg=CARD); row.pack(anchor="w",pady=5)
        es=[]
        for lab,val in zip(labels,defaults):
            tk.Label(row,text=lab+" =",bg=CARD,fg=MUTED,font=("Arial",10,"bold")).pack(side="left",padx=(5,0))
            es.append(self.entry(row,val,6))
        return es

                                              
    def page_history(self):
        self.heading("Uma história improvável: de onde vieram os complexos?",
                     "Os números complexos não nasceram de uma definição abstrata pronta. Eles surgiram de tentativas de resolver problemas algébricos concretos.")
        c=self.card("Antes dos complexos: os números negativos já causavam estranhamento",PURPLE)
        self.para(c,"Durante séculos, matemáticos trabalharam com números naturais, frações e grandezas geométricas. Números negativos foram sendo aceitos gradualmente, mas raízes quadradas de números negativos pareciam ainda mais misteriosas: como interpretar √(−1) se nenhum número real ao quadrado produz −1?")
        c=self.card("A pista aparece nas equações cúbicas",ORANGE)
        self.para(c,"No século XVI, a resolução de equações do terceiro grau colocou os matemáticos diante de expressões com raízes de números negativos — inclusive em problemas cujas soluções finais eram números reais. O desconforto não era apenas filosófico: essas expressões apareciam no meio de cálculos que davam respostas corretas.")
        timeline=[("1545 — Girolamo Cardano","Em Ars Magna, publicou métodos para resolver equações cúbicas. Em certos casos, sua fórmula produzia raízes quadradas de números negativos."),("1572 — Rafael Bombelli","Em L'Algebra, desenvolveu regras operatórias para lidar com essas expressões, mostrando como elas podiam funcionar coerentemente nos cálculos."),("Séculos XVIII–XIX — consolidação","Euler popularizou a letra i para √(−1); Gauss ajudou a consolidar a representação geométrica no plano, associada hoje ao plano de Argand-Gauss.")]
        for title,desc in timeline:
            box=tk.Frame(c,bg=CARD2,padx=12,pady=10);box.pack(fill="x",pady=4)
            tk.Label(box,text=title,bg=CARD2,fg=CYAN,font=("Arial",11,"bold")).pack(anchor="w")
            self.para(box,desc,10,MUTED)
        c=self.card("Uma pergunta histórica para pensar",GREEN)
        self.para(c,"Se uma expressão parece impossível, isso significa que ela é inútil? A história dos complexos mostra que uma ampliação bem construída do sistema numérico pode revelar relações e resolver problemas que antes pareciam bloqueados.")
        self.para(c,"Curiosidade: o nome 'imaginário' permaneceu por tradição, mas os números complexos são objetos matemáticos tão consistentes quanto os reais.",10,ORANGE,True)

    def page_problem(self):
        self.heading("O problema das equações: por que ampliar os reais?","Vamos começar com a equação mais simples que não possui solução real: x² + 1 = 0.")
        c=self.card("O impasse",ORANGE); self.formula(c,"x² + 1 = 0  ⟹  x² = −1",ORANGE,25)
        self.para(c,"Para qualquer x real, temos x² ≥ 0. Portanto, não existe número real cujo quadrado seja −1. Isso não é uma falha de cálculo: é uma impossibilidade dentro do conjunto ℝ.")
        c=self.card("Experimente o discriminante",CYAN)
        self.para(c,"Mude os coeficientes da equação ax² + bx + c = 0 e observe quando o discriminante é negativo.")
        row=tk.Frame(c,bg=CARD);row.pack(anchor="w",pady=5)
        es=[]
        for lab,val in [("a",1),("b",0),("c",1)]:
            tk.Label(row,text=lab+" =",bg=CARD,fg=MUTED).pack(side="left");es.append(self.entry(row,val,6))
        out=tk.Label(c,text="Δ = b² − 4ac",bg=CARD,fg=GREEN,font=("Arial",13,"bold"));out.pack(anchor="w",pady=8)
        def calc():
            try:
                a,b,cc=[float(e.get().replace(',','.')) for e in es]
                if abs(a)<1e-12: out.config(text="a não pode ser zero nesta equação quadrática.",fg=RED);return
                d=b*b-4*a*cc
                msg=f"Δ = {self.fmt(d)}. " + ("Duas raízes reais distintas." if d>0 else "Uma raiz real dupla." if d==0 else f"Não há raízes reais. No conjunto complexo: x = {self.fmt(-b/(2*a))} ± {self.fmt(math.sqrt(-d)/(2*abs(a)))}i (ajuste o sinal conforme a).")
                out.config(text=msg,fg=GREEN if d>=0 else ORANGE)
            except ValueError:out.config(text="Digite números válidos.",fg=RED)
        self.button(c,"Calcular Δ",calc).pack(anchor="w")
        c=self.card("A ideia central",PURPLE);self.para(c,"Em vez de abandonar a equação, ampliamos o sistema numérico. Procuramos um conjunto que contenha ℝ e no qual exista um elemento i com i² = −1. Esse conjunto será ℂ, o conjunto dos números complexos.")

    def page_i(self):
        self.heading("A unidade imaginária i","Definimos um novo elemento que permite escrever uma raiz quadrada de −1.")
        c=self.card("Definição",GREEN);self.formula(c,"i² = −1     (equivalentemente, i = √−1 como notação formal)",ORANGE,23)
        self.para(c,"É importante compreender a lógica: não estamos afirmando que exista um real com essa propriedade. Estamos definindo uma nova unidade e construindo um sistema no qual as operações respeitam regras algébricas coerentes.")
        self.formula(c,"x² = −1  ⟹  x = ±i",CYAN,25)
        c=self.card("Atenção à linguagem",RED);self.para(c,"A parte imaginária de um complexo será um número real multiplicado por i. Não confunda 'i' com um número real, nem confunda o coeficiente da parte imaginária com o termo completo bi.")
        c=self.card("Cheque sua compreensão",PURPLE)
        q=tk.Label(c,text="Qual afirmação expressa a definição fundamental?",bg=CARD,fg=WHITE,font=("Arial",11,"bold"));q.pack(anchor="w")
        v=tk.StringVar(value="")
        for txt,val in [("i = 1", "a"),("i² = −1","b"),("i² = 1","c")]:tk.Radiobutton(c,text=txt,variable=v,value=val,bg=CARD,fg=WHITE,selectcolor=CARD2,activebackground=CARD).pack(anchor="w")
        feedback=tk.Label(c,text="",bg=CARD,fg=GREEN);feedback.pack(anchor="w",pady=5)
        self.button(c,"Verificar",lambda:feedback.config(text="Isso mesmo! i² = −1." if v.get()=="b" else "Ainda não. Pense na equação x² = −1."),BLUE).pack(anchor="w")

    def page_powers(self):
        self.heading("Potências de i: um ciclo de quatro","As potências da unidade imaginária seguem um padrão periódico. Descobrir esse ciclo simplifica cálculos com expoentes grandes.")
        c=self.card("Observe a sequência",CYAN);self.formula(c,"i⁰ = 1   •   i¹ = i   •   i² = −1   •   i³ = −i   •   i⁴ = 1",ORANGE,19)
        self.para(c,"Como i⁴ = 1, as potências se repetem a cada quatro expoentes. Para calcular iⁿ, basta dividir n por 4 e observar o resto.")
        c=self.card("Calculadora de potências",GREEN)
        row=tk.Frame(c,bg=CARD);row.pack(anchor="w");tk.Label(row,text="Expoente n =",bg=CARD,fg=MUTED).pack(side="left");e=self.entry(row,37,8)
        out=tk.Label(c,text="",bg=CARD,fg=ORANGE,font=("Arial",16,"bold"));out.pack(anchor="w",pady=8)
        def calc():
            try:
                n=int(e.get());cycle=["1","i","−1","−i"];out.config(text=f"37 = 4·{n//4} + {n%4}" if n>=0 else f"i^{n} = {cycle[n%4]} (expoente negativo também é permitido, pois i ≠ 0)")
                if n>=0:out.config(text=f"{n} = 4·{n//4} + {n%4}   ⇒   i^{n} = {cycle[n%4]}")
            except ValueError:out.config(text="Digite um expoente inteiro.",fg=RED)
        self.button(c,"Calcular iⁿ",calc).pack(anchor="w")
        c=self.card("Por que o ciclo funciona?",PURPLE);self.para(c,"Cada passo multiplica pelo próprio i. Depois de quatro multiplicações, temos i⁴ = (i²)² = (−1)² = 1. Multiplicar por 1 não altera o resultado: o padrão recomeça.")

    def page_algebraic(self):
        self.heading("Forma algébrica e igualdade","A escrita a + bi organiza os complexos em duas componentes reais.")
        c=self.card("Forma algébrica",GREEN);self.formula(c,"z = a + bi,   com a,b ∈ ℝ",ORANGE,27)
        self.para(c,"a = Re(z) é a parte real; b = Im(z) é a parte imaginária. Note: Im(z) = b, não bi.")
        c=self.card("Exemplos",CYAN)
        for z,desc in [("3 + 2i","Re = 3; Im = 2"),("−4 − 5i","Re = −4; Im = −5"),("7","Re = 7; Im = 0 — todo real é complexo"),("−3i","Re = 0; Im = −3 — imaginário puro")]:
            self.formula(c,z,ORANGE,16);self.para(c,desc,10,MUTED)
        c=self.card("Laboratório: identifique as partes",PURPLE)
        row=tk.Frame(c,bg=CARD);row.pack(anchor="w");self.para(c,"Considere z = −6 + 4i. Informe Re(z) e Im(z).")
        er=self.entry(row,"-6",7);ei=self.entry(row,"4",7);out=tk.Label(c,text="",bg=CARD,fg=GREEN);out.pack(anchor="w",pady=6)
        self.button(c,"Conferir",lambda:out.config(text="Correto! Re(z)=−6 e Im(z)=4." if er.get().strip()=="-6" and ei.get().strip()=="4" else "Revise: a parte imaginária é o coeficiente de i."),BLUE).pack(anchor="w")
        c=self.card("Critério de igualdade",ORANGE);self.formula(c,"a + bi = c + di  ⇔  a = c e b = d",WHITE,20)
        self.para(c,"Dois complexos são iguais exatamente quando suas componentes reais correspondentes são iguais.")

    def page_plane(self):
        self.heading("O plano de Argand-Gauss: números como pontos","A cada z = a + bi associamos o ponto (a,b). O eixo horizontal é o real; o vertical, o imaginário.")
        c=self.card("Explore o plano em tempo real",CYAN)
        self.make_complex_plot(c, initial=(3,2), width=660, height=390)
        c=self.card("Leitura geométrica",PURPLE);self.para(c,"O ponto (a,b) pode ser interpretado como um vetor com origem em (0,0). A coordenada horizontal é a parte real; a vertical é a parte imaginária. Assim, o conjunto ℂ pode ser visualizado como um plano, e não apenas como uma reta.")

    def make_complex_plot(self,parent,initial=(2,3),width=600,height=340):
        controls=tk.Frame(parent,bg=CARD);controls.pack(fill="x")
        ar=tk.IntVar(value=initial[0]);bi=tk.IntVar(value=initial[1])
        for label,var,color in [("Parte real a",ar,BLUE),("Parte imaginária b",bi,GREEN)]:
            tk.Label(controls,text=label,bg=CARD,fg=color,font=("Arial",10,"bold")).pack(anchor="w")
            tk.Scale(controls,from_=-8,to=8,orient="horizontal",variable=var,bg=CARD,fg=WHITE,troughcolor=CARD2,
                     highlightthickness=0,length=330,command=lambda _ : draw()).pack(anchor="w")
        info=tk.Label(controls,text="",bg=CARD,fg=ORANGE,font=("Arial",12,"bold"));info.pack(anchor="w",pady=3)
        canvas=tk.Canvas(parent,bg="#F8FAFD",height=height,highlightthickness=0);canvas.pack(fill="x",pady=8)
        def draw(_=None):
            canvas.delete("all");w=max(canvas.winfo_width(),width);h=height;cx=w/2;cy=h/2;s=min((w-70)/18,(h-55)/18)
            for n in range(-8,9):
                canvas.create_line(cx+n*s,15,cx+n*s,h-20,fill="#E1E8F2")
                canvas.create_line(25,cy-n*s,w-20,cy-n*s,fill="#E1E8F2")
                if n:canvas.create_text(cx+n*s,cy+13,text=str(n),fill=MUTED,font=("Arial",8));canvas.create_text(cx-13,cy-n*s,text=str(n),fill=MUTED,font=("Arial",8))
            canvas.create_line(20,cy,w-15,cy,fill=WHITE,width=2,arrow=tk.LAST);canvas.create_line(cx,h-15,cx,12,fill=WHITE,width=2,arrow=tk.LAST)
            canvas.create_text(w-30,cy-16,text="Re",fill=BLUE,font=("Arial",10,"bold"));canvas.create_text(cx+20,18,text="Im",fill=GREEN,font=("Arial",10,"bold"))
            a,b=ar.get(),bi.get();x=cx+a*s;y=cy-b*s
            canvas.create_line(x,y,x,cy,fill=GREEN,dash=(4,3),width=2);canvas.create_line(x,y,cx,y,fill=BLUE,dash=(4,3),width=2)
            canvas.create_line(cx,cy,x,y,fill=ORANGE,width=3,arrow=tk.LAST);canvas.create_oval(x-7,y-7,x+7,y+7,fill=ORANGE,outline=WHITE,width=2)
            info.config(text=f"z = {self.cfmt(complex(a,b))}     Coordenadas: ({a}, {b})")
        canvas.bind("<Configure>",draw);draw()

    def page_modulus(self):
        self.heading("Módulo: a distância até a origem","O módulo de um complexo é o comprimento do vetor que o representa no plano.")
        c=self.card("Definição geométrica e algébrica",GREEN);self.formula(c,"|z| = √(a² + b²),   para z = a + bi",ORANGE,24)
        self.para(c,"A fórmula é consequência direta do teorema de Pitágoras: a e b são os catetos de um triângulo retângulo, e |z| é a hipotenusa.")
        c=self.card("Calcule e visualize",CYAN);self.make_complex_plot(c,(3,4),600,330)
        self.para(c,"Observe que o módulo não é uma coordenada: é uma distância, sempre não negativa.",10,ORANGE,True)
        c=self.card("Mini-investigação",PURPLE);self.para(c,"Quais pontos têm módulo 5? Todos os pontos que satisfazem a² + b² = 25 formam uma circunferência de centro na origem e raio 5.")

    def page_addsub(self):
        self.heading("Adição e subtração: operações por componentes","Somamos ou subtraímos as partes reais entre si e as partes imaginárias entre si.")
        c=self.card("Regras",GREEN);self.formula(c,"(a+bi) ± (c+di) = (a±c) + (b±d)i",ORANGE,22)
        self.para(c,"No plano, a soma corresponde à soma dos vetores por componentes. A subtração pode ser vista como adicionar o vetor oposto.")
        c=self.card("Calculadora de adição/subtração",CYAN);es=self.pair_inputs(c,("a","b","c","d"),(3,2,1,4))
        op=tk.StringVar(value="+");row=tk.Frame(c,bg=CARD);row.pack(anchor="w",pady=5)
        tk.Radiobutton(row,text="Somar",variable=op,value="+",bg=CARD,fg=WHITE,selectcolor=CARD2).pack(side="left")
        tk.Radiobutton(row,text="Subtrair",variable=op,value="-",bg=CARD,fg=WHITE,selectcolor=CARD2).pack(side="left",padx=10)
        out=tk.Label(c,text="",bg=CARD,fg=ORANGE,font=("Arial",16,"bold"));out.pack(anchor="w",pady=7)
        def calc():
            try:
                a,b,cc,d=[float(e.get().replace(',','.')) for e in es];z=complex(a,b)+(complex(cc,d) if op.get()=="+" else -complex(cc,d));out.config(text=f"Resultado: {self.cfmt(z)}")
            except ValueError:out.config(text="Preencha todos os coeficientes com números.",fg=RED)
        self.button(c,"Calcular operação",calc).pack(anchor="w")
        c=self.card("Exemplo desenvolvido",PURPLE);self.formula(c,"(3 + 2i) + (1 + 4i) = 4 + 6i",WHITE,19);self.formula(c,"(3 + 2i) − (1 + 4i) = 2 − 2i",WHITE,19)

    def page_multiply(self):
        self.heading("Multiplicação: distributividade e i² = −1","Multiplicar complexos exige desenvolver os produtos e substituir i² por −1.")
        c=self.card("Demonstração",GREEN)
        for s,col in [("(a + bi)(c + di)",ORANGE),("= ac + adi + bci + bd i²",WHITE),("= ac − bd + (ad + bc)i",CYAN)]:self.formula(c,s,col,21)
        self.para(c,"A parte real do produto é ac − bd; a parte imaginária é ad + bc. O sinal negativo aparece porque i² = −1.")
        c=self.card("Multiplicador interativo",CYAN);es=self.pair_inputs(c,("a","b","c","d"),(2,3,1,2))
        out=tk.Label(c,text="",bg=CARD,fg=ORANGE,font=("Arial",16,"bold"));out.pack(anchor="w",pady=7)
        def calc():
            try:
                a,b,cc,d=[float(e.get().replace(',','.')) for e in es];z=complex(a,b)*complex(cc,d);out.config(text=f"{self.cfmt(complex(a,b))} × {self.cfmt(complex(cc,d))} = {self.cfmt(z)}\nParte real = ac − bd = {self.fmt(a*cc-b*d)}; parte imaginária = ad + bc = {self.fmt(a*d+b*cc)}")
            except ValueError:out.config(text="Digite quatro números.",fg=RED)
        self.button(c,"Multiplicar",calc).pack(anchor="w")
        c=self.card("Interpretação geométrica",PURPLE);self.para(c,"Na forma polar, multiplicar por um complexo pode alterar o comprimento (módulo) e girar o vetor (argumento). Veremos isso na etapa 11.")

    def page_division(self):
        self.heading("Conjugado e divisão","O conjugado permite transformar o denominador em um número real.")
        c=self.card("Conjugado",GREEN);self.formula(c,"Se z = a + bi, então z̄ = a − bi",ORANGE,23);self.formula(c,"z·z̄ = (a+bi)(a−bi) = a²+b² = |z|²",CYAN,20)
        self.para(c,"Geometricamente, o conjugado reflete o ponto em relação ao eixo real: mantém a parte real e inverte o sinal da parte imaginária.")
        c=self.card("Divisão passo a passo",CYAN);self.formula(c,"(a+bi)/(c+di) · (c−di)/(c−di)",ORANGE,19)
        self.formula(c,"= [(ac+bd) + (bc−ad)i] / (c²+d²)",WHITE,19)
        self.para(c,"O denominador c²+d² é |c+di|². Ele só é zero quando c=d=0, isto é, quando o divisor é o complexo nulo.")
        c=self.card("Calculadora de divisão",PURPLE);es=self.pair_inputs(c,("a","b","c","d"),(3,1,1,1))
        out=tk.Label(c,text="",bg=CARD,fg=ORANGE,font=("Arial",15,"bold"),justify="left");out.pack(anchor="w",pady=7)
        def calc():
            try:
                a,b,cc,d=[float(e.get().replace(',','.')) for e in es]
                if abs(cc)+abs(d)<1e-12:out.config(text="Divisão por zero não é definida.",fg=RED);return
                z=complex(a,b)/complex(cc,d);out.config(text=f"Resultado: {self.cfmt(z)}\nConjugado do divisor: {self.cfmt(complex(cc,-d))}")
            except ValueError:out.config(text="Digite números válidos.",fg=RED)
        self.button(c,"Dividir",calc).pack(anchor="w")

    def page_polar(self):
        self.heading("Forma polar: módulo e argumento","Além de a + bi, podemos descrever um complexo pelo comprimento do vetor e pelo ângulo que ele forma com o eixo real positivo.")
        c=self.card("Forma trigonométrica",GREEN);self.formula(c,"z = r(cos θ + i sen θ)",ORANGE,25)
        self.para(c,"Aqui r = |z| ≥ 0 é o módulo e θ é um argumento de z. Para z ≠ 0, o argumento é determinado a menos de múltiplos de 2π (ou 360°).")
        self.para(c,"Como a = r cos θ e b = r sen θ, recuperamos a forma algébrica. A forma polar torna especialmente clara a multiplicação: módulos multiplicam e argumentos somam.")
        c=self.card("Gire um vetor",CYAN)
        row=tk.Frame(c,bg=CARD);row.pack(anchor="w");tk.Label(row,text="Ângulo θ (graus):",bg=CARD,fg=MUTED).pack(side="left");e=self.entry(row,45,7)
        out=tk.Label(c,text="",bg=CARD,fg=ORANGE,font=("Arial",13,"bold"));out.pack(anchor="w",pady=7)
        canv=tk.Canvas(c,bg="#F8FAFD",height=260,highlightthickness=0);canv.pack(fill="x",pady=5)
        def draw():
            try:deg=float(e.get().replace(',','.'))
            except ValueError:out.config(text="Digite um ângulo.",fg=RED);return
            theta=math.radians(deg);r=4; a=r*math.cos(theta);b=r*math.sin(theta);w=max(canv.winfo_width(),500);h=260;cx=w/2;cy=h/2;s=27
            canv.delete("all");canv.create_line(20,cy,w-20,cy,fill=WHITE,arrow=tk.LAST);canv.create_line(cx,h-15,cx,15,fill=WHITE,arrow=tk.LAST)
            x=cx+a*s;y=cy-b*s;canv.create_line(cx,cy,x,y,fill=ORANGE,width=4,arrow=tk.LAST);canv.create_oval(x-6,y-6,x+6,y+6,fill=CYAN,outline=WHITE)
            out.config(text=f"z ≈ {self.fmt(a)} {('+' if b>=0 else '−')} {self.fmt(abs(b))}i     |z| = 4     θ = {self.fmt(deg)}°")
        self.button(c,"Atualizar rotação",draw).pack(anchor="w");canv.bind("<Configure>",lambda _:draw());draw()
        c=self.card("Regra de ouro",PURPLE);self.formula(c,"r₁ cis θ₁ · r₂ cis θ₂ = (r₁r₂) cis(θ₁+θ₂)",WHITE,18)

    def page_applications(self):
        self.heading("Aplicações e síntese","Os complexos ultrapassam o exercício de sala: são uma linguagem útil para descrever fenômenos com amplitude e fase.")
        c=self.card("Onde aparecem?",CYAN)
        items=[("Eletricidade em corrente alternada","Representações complexas simplificam cálculos de amplitude e defasagem em circuitos."),("Sinais e processamento","Exponenciais complexas descrevem oscilações e são centrais na análise de Fourier."),("Física e engenharia","A linguagem complexa aparece em ondas, vibrações, sistemas lineares e soluções de equações diferenciais."),("Matemática","Polinômios, funções, análise complexa e álgebra ganham estrutura quando trabalhamos em ℂ.")]
        for t,d in items:
            box=tk.Frame(c,bg=CARD2,padx=12,pady=9);box.pack(fill="x",pady=4);tk.Label(box,text=t,bg=CARD2,fg=ORANGE,font=("Arial",11,"bold")).pack(anchor="w");self.para(box,d,10,MUTED)
        c=self.card("Mapa conceitual",GREEN);self.formula(c,"ℂ: z = a + bi  ↔  (a,b)",ORANGE,23)
        self.para(c,"Forma algébrica → operações por componentes e distributividade.\nConjugado → reflexão no eixo real e racionalização.\nMódulo → distância à origem.\nForma polar → módulo + argumento; multiplicação = escala + rotação.")
        c=self.card("Uma última ideia",PURPLE);self.para(c,"A ampliação de ℝ para ℂ não elimina os números reais: ela os incorpora como casos particulares, com parte imaginária igual a zero. O sistema maior preserva as operações conhecidas e permite resolver equações antes impossíveis em ℝ.")

    def page_challenge(self):
        self.heading("Desafio final","Resolva uma sequência de questões curtas. Você pode tentar novamente antes de avançar.")
        c=self.card("Desafio de compreensão",ORANGE)
        self.question_area=tk.Frame(c,bg=CARD);self.question_area.pack(fill="x")
        self.q_index=0;self.q_score=0;self.challenge_questions=[
            ("Quanto vale i¹⁰?",["1","−1","i","−i"],1,"10 deixa resto 2 na divisão por 4; portanto i¹⁰ = i² = −1."),
            ("Se z = −2 + 5i, qual é Im(z)?",["5i","−2","5","−5"],2,"A parte imaginária é o coeficiente real 5."),
            ("Qual é o módulo de 3 + 4i?",["7","5","25","√7"],1,"|z| = √(3²+4²) = 5."),
            ("(1 + 2i)(2 − i) é igual a:",["4 + 3i","0 + 3i","4 − 3i","2 + 3i"],0,"2 − i + 4i − 2i² = 4 + 3i."),
            ("O conjugado de −3 + 7i é:",["3 + 7i","−3 − 7i","−3 + 7i","3 − 7i"],1,"Mantemos a parte real e trocamos o sinal da imaginária.")]
        self.render_question()
    def render_question(self):
        for w in self.question_area.winfo_children():w.destroy()
        q=self.challenge_questions[self.q_index];tk.Label(self.question_area,text=f"QUESTÃO {self.q_index+1}/{len(self.challenge_questions)}   •   ACERTOS: {self.q_score}",bg=CARD,fg=CYAN,font=("Arial",10,"bold")).pack(anchor="w",pady=5)
        tk.Label(self.question_area,text=q[0],bg=CARD,fg=WHITE,font=("Arial",14,"bold"),wraplength=900).pack(anchor="w",pady=8)
        v=tk.IntVar(value=-1)
        for i,opt in enumerate(q[1]):tk.Radiobutton(self.question_area,text=opt,variable=v,value=i,bg=CARD,fg=WHITE,selectcolor=CARD2,activebackground=CARD,font=("Arial",11)).pack(anchor="w",pady=2)
        feedback=tk.Label(self.question_area,text="",bg=CARD,fg=GREEN,justify="left",wraplength=950);feedback.pack(anchor="w",pady=8)
        def check():
            if v.get()<0:feedback.config(text="Escolha uma alternativa.",fg=RED);return
            if v.get()==q[2]:self.q_score+=1;self.score=self.q_score;feedback.config(text="Correto! "+q[3],fg=GREEN)
            else:feedback.config(text="Ainda não. "+q[3],fg=ORANGE)
            verify.config(state="disabled")
        verify=self.button(self.question_area,"Verificar resposta",check,BLUE);verify.pack(anchor="w",pady=4)
        if self.q_index<len(self.challenge_questions)-1:self.button(self.question_area,"Próxima questão →",lambda:self.advance_question(),PURPLE).pack(anchor="w",pady=4)
        else:self.button(self.question_area,"Ver resultado",lambda:messagebox.showinfo("Resultado",f"Você acertou {self.q_score} de {len(self.challenge_questions)} questões."),GREEN).pack(anchor="w",pady=4)
    def advance_question(self):self.q_index+=1;self.render_question()

                                                                            
    def page_opening(self):
        self.heading("Uma pergunta que parece impossível", "A aula começa com um problema, não com uma definição pronta.")
        c=self.card("Problema de abertura", BLUE)
        self.formula(c, "x² + 1 = 0   ⟺   x² = −1", ORANGE, 27)
        self.para(c, "Pense individualmente por alguns segundos: existe um número real que, multiplicado por si mesmo, resulte em −1? Justifique sem usar apenas a frase ‘não existe’.")
        c=self.card("Objetivos da jornada", GREEN)
        self.para(c, "Ao final, a turma deverá interpretar a forma a + bi, localizar complexos no plano, calcular operações fundamentais, compreender módulo, conjugado e forma polar e reconhecer por que essa ampliação é útil.")

    def page_cardano(self):
        self.heading("Cardano e o caminho até as raízes negativas", "A história começa no século XVI, com equações cúbicas e fórmulas de resolução.")
        c=self.card("O contexto matemático", PURPLE)
        self.para(c, "No Renascimento, resolver equações polinomiais era um problema central da álgebra. Em 1545, Girolamo Cardano publicou Ars Magna, obra que sistematizou métodos para equações cúbicas. Em alguns casos, a fórmula levava a raízes quadradas de números negativos, mesmo quando a solução final procurada era real.")
        c=self.card("O caso que provoca estranhamento", ORANGE)
        self.formula(c, "x³ = 15x + 4", ORANGE, 24)
        self.para(c, "Uma raiz real é x = 4. Entretanto, a fórmula de resolução pode produzir uma expressão intermediária que contém √(−121). O ponto histórico importante é esse: a expressão aparentemente impossível surgia dentro de um cálculo que conduzia a uma resposta real.")
        self.para(c, "Pergunta para a turma: se um método correto produz uma expressão estranha no meio do caminho, devemos descartá-la imediatamente?", 11, CYAN, True)

    def page_bombelli(self):
        self.heading("Bombelli: aprender a calcular antes de compreender", "A contribuição decisiva foi estabelecer regras operatórias coerentes para expressões com raízes negativas.")
        c=self.card("A ousadia algébrica", GREEN)
        self.para(c, "Em 1572, Rafael Bombelli publicou L'Algebra. Ele tratou expressões envolvendo raízes de negativos de maneira sistemática. Em vez de simplesmente rejeitá-las, estabeleceu regras para somar e multiplicar esses termos e verificou que os cálculos podiam levar a resultados consistentes.")
        self.formula(c, "(√−1)² = −1", ORANGE, 25)
        c=self.card("Experimento mental", CYAN)
        self.para(c, "Imagine que uma nova notação seja introduzida para representar √−1. Que regra ela precisa obedecer para que a álgebra continue funcionando? A regra central será i² = −1.")
        self.para(c, "A história não é uma sequência linear em que todos concordaram imediatamente. A aceitação dos complexos foi gradual, acompanhada por novas interpretações algébricas e geométricas.", 10, MUTED)

    def page_components(self):
        self.heading("Igualdade e classificação dos complexos", "A forma algébrica permite comparar números e reconhecer casos particulares.")
        c=self.card("Igualdade componente a componente", BLUE)
        self.formula(c, "a + bi = c + di  ⇔  a = c  e  b = d", ORANGE, 22)
        self.para(c, "Exemplo: 3 + 2i = x + yi implica x = 3 e y = 2. Não basta que os números ‘pareçam próximos’: as duas componentes devem coincidir.")
        c=self.card("Três casos importantes", PURPLE)
        for title,desc in [("Real", "b = 0. Exemplo: 5 = 5 + 0i."),("Imaginário puro", "a = 0 e b ≠ 0. Exemplo: −3i."),("Complexo não real", "a ≠ 0 e b ≠ 0. Exemplo: 2 − 7i.")]:
            self.para(c, title + " — " + desc, 11, INK)
        c=self.card("Teste rápido", GREEN)
        self.para(c, "Se z = −4 + 0i, ele é real, imaginário puro ou complexo não real? Resposta esperada: é real; todo número real pertence a ℂ.")

    def page_conjugate(self):
        self.heading("Conjugado: uma reflexão no eixo real", "O conjugado é uma operação algébrica com uma interpretação geométrica simples.")
        c=self.card("Definição e propriedades", GREEN)
        self.formula(c, "z = a + bi   ⇒   z̄ = a − bi", ORANGE, 24)
        self.formula(c, "z + z̄ = 2a     e     z·z̄ = a² + b² = |z|²", CYAN, 20)
        self.para(c, "No plano, z e z̄ são simétricos em relação ao eixo real: a coordenada horizontal permanece e a vertical troca de sinal.")
        c=self.card("Veja a simetria", CYAN)
        cv=tk.Canvas(c,bg="#F8FAFD",height=245,highlightthickness=0);cv.pack(fill="x")
        def draw(_=None):
            cv.delete("all");w=max(cv.winfo_width(),520);h=245;cx=w/2;cy=h/2;s=28
            cv.create_line(20,cy,w-20,cy,fill=INK,width=2,arrow=tk.LAST);cv.create_line(cx,h-12,cx,12,fill=INK,width=2,arrow=tk.LAST)
            for a,b,col,label in [(3,2,BLUE,"z = 3 + 2i"),(3,-2,ORANGE,"z̄ = 3 − 2i")]:
                x=cx+a*s;y=cy-b*s;cv.create_line(cx,cy,x,y,fill=col,width=3,arrow=tk.LAST);cv.create_oval(x-5,y-5,x+5,y+5,fill=col,outline=col);cv.create_text(x+55,y,text=label,fill=col,font=("Arial",10,"bold"))
        cv.bind("<Configure>",draw);draw()

    def page_rotation(self):
        self.heading("Multiplicar também pode girar e ampliar", "A forma polar revela uma interpretação geométrica da multiplicação.")
        c=self.card("Duas ações em uma", PURPLE)
        self.para(c, "Multiplicar por um complexo não nulo pode alterar o comprimento do vetor e sua direção. O módulo do produto é o produto dos módulos; os argumentos são somados.")
        self.formula(c, "|z₁z₂| = |z₁|·|z₂|", ORANGE, 22)
        self.formula(c, "arg(z₁z₂) = arg(z₁) + arg(z₂)  (mod 2π)", CYAN, 20)
        c=self.card("Explore a rotação", CYAN)
        row=tk.Frame(c,bg=CARD);row.pack(anchor="w",pady=4)
        tk.Label(row,text="Ângulo do fator (graus):",bg=CARD,fg=MUTED).pack(side="left")
        angle=self.entry(row,90,6)
        out=tk.Label(c,text="",bg=CARD,fg=ORANGE,font=("Arial",12,"bold"));out.pack(anchor="w",pady=6)
        cv=tk.Canvas(c,bg="#F8FAFD",height=260,highlightthickness=0);cv.pack(fill="x")
        def draw():
            try:deg=float(angle.get().replace(',','.'))
            except ValueError:out.config(text="Digite um ângulo válido.",fg=RED);return
            t=math.radians(deg);w=max(cv.winfo_width(),520);h=260;cx=w/2;cy=h/2;s=28
            cv.delete("all");cv.create_line(15,cy,w-15,cy,fill=INK,arrow=tk.LAST);cv.create_line(cx,h-12,cx,12,fill=INK,arrow=tk.LAST)
            for theta,col in [(0,BLUE),(t,ORANGE)]:
                x=cx+4*math.cos(theta)*s;y=cy-4*math.sin(theta)*s;cv.create_line(cx,cy,x,y,fill=col,width=4,arrow=tk.LAST)
            out.config(text=f"Multiplicar por cis({self.fmt(deg)}°) mantém o módulo 4 e gira o vetor em {self.fmt(deg)}°.")
        self.button(c,"Atualizar",draw,BLUE).pack(anchor="w",pady=5);cv.bind("<Configure>",lambda e:draw());draw()

    def page_conversion(self):
        self.heading("Da forma algébrica à forma polar", "Converta as coordenadas cartesianas em módulo e argumento.")
        c=self.card("Relações fundamentais", GREEN)
        self.formula(c, "r = √(a² + b²)     cos θ = a/r     sen θ = b/r", ORANGE, 21)
        self.para(c, "O módulo vem do teorema de Pitágoras. O argumento depende do quadrante do ponto; por isso, não basta calcular arctan(b/a) sem observar os sinais de a e b.")
        c=self.card("Conversor interativo", CYAN)
        row=tk.Frame(c,bg=CARD);row.pack(anchor="w")
        tk.Label(row,text="a =",bg=CARD,fg=MUTED).pack(side="left");ea=self.entry(row,3,6)
        tk.Label(row,text="b =",bg=CARD,fg=MUTED).pack(side="left",padx=(10,0));eb=self.entry(row,4,6)
        out=tk.Label(c,text="",bg=CARD,fg=ORANGE,font=("Arial",13,"bold"),justify="left");out.pack(anchor="w",pady=8)
        def convert():
            try:
                a=float(ea.get().replace(',','.'));b=float(eb.get().replace(',','.'));r=math.hypot(a,b)
                if r==0:out.config(text="Para z = 0, o argumento não é definido.",fg=RED);return
                deg=math.degrees(math.atan2(b,a));out.config(text=f"z = {self.cfmt(complex(a,b))}\nMódulo r = {self.fmt(r)}\nArgumento principal θ = {self.fmt(deg)}°\nForma polar: {self.fmt(r)}(cos {self.fmt(deg)}° + i sen {self.fmt(deg)}°)")
            except ValueError:out.config(text="Informe valores numéricos.",fg=RED)
        self.button(c,"Converter",convert).pack(anchor="w")

    def page_synthesis(self):
        self.heading("Síntese: como as ideias se conectam", "Retome o mapa conceitual antes do jogo coletivo.")
        items=[("Forma algébrica", "z = a + bi: duas componentes reais."),("Plano", "z ↔ (a,b): ponto ou vetor no plano."),("Módulo", "|z| = √(a²+b²): distância à origem."),("Conjugado", "a − bi: reflexão no eixo real; z·z̄ = |z|²."),("Operações", "Adição por componentes; multiplicação pela distributividade."),("Forma polar", "Módulo e argumento; produto combina escala e rotação.")]
        for title,desc in items:
            c=self.card(title,BLUE);self.para(c,desc,11,INK)
        c=self.card("Questão de amarração", ORANGE)
        self.para(c, "Por que a forma algébrica costuma ser conveniente para somar, enquanto a forma polar costuma ser conveniente para multiplicar? Discuta: na primeira, agrupamos componentes; na segunda, multiplicamos módulos e somamos ângulos.", 11, INK)

    def page_game(self):
        self.heading("Batalha dos complexos", "Mini game para projetar: a turma responde em voz alta, por equipes ou levantando cartões. O computador fica com o apresentador.")
        c=self.card("Como conduzir", PURPLE)
        self.para(c, "Divida a sala em duas equipes. Leia a pergunta projetada e dê o tempo indicado. A turma discute sem usar o teclado. Clique em ‘Revelar resposta’ para mostrar a solução e a justificativa; depois atribua o ponto à equipe correspondente.")
        self.game_questions=[
            ("Aquecimento", "Quanto vale i² + i⁴?", "0", "i² = −1 e i⁴ = 1; portanto, −1 + 1 = 0.", "30 s"),
            ("Leitura", "Se z = −3 + 8i, quanto vale Im(z)?", "8", "A parte imaginária é o coeficiente real de i: 8.", "25 s"),
            ("Plano", "Qual ponto representa z = 2 − 3i?", "(2, −3)", "A coordenada real é 2 e a imaginária é −3.", "30 s"),
            ("Módulo", "Qual é |5 + 12i|?", "13", "√(25 + 144) = √169 = 13.", "30 s"),
            ("Operação", "Calcule (2 + i) + (−5 + 3i).", "−3 + 4i", "Somamos as partes: 2 − 5 = −3 e 1 + 3 = 4.", "35 s"),
            ("Produto", "Calcule (1 + i)(1 − i).", "2", "Produto de conjugados: 1² + 1² = 2.", "35 s"),
            ("Conjugado", "Qual é o conjugado de −4 − 7i?", "−4 + 7i", "Mantemos a parte real e trocamos o sinal da parte imaginária.", "25 s"),
            ("Desafio", "Multiplicar por i corresponde a que rotação no plano?", "90° no sentido anti-horário", "i tem módulo 1 e argumento 90°; portanto, gira sem alterar o comprimento.", "40 s"),
        ]
        self.game_index=0;self.game_score=[0,0];self.game_revealed=False;self.game_timer_id=None;self.game_seconds=0
        panel=tk.Frame(self.area,bg="#101C32",padx=22,pady=20);panel.pack(fill="x",padx=9,pady=10)
        top=tk.Frame(panel,bg="#101C32");top.pack(fill="x")
        self.game_round_label=tk.Label(top,text="",bg="#101C32",fg="#9FB8FF",font=("Arial",10,"bold"));self.game_round_label.pack(side="left")
        self.game_timer_label=tk.Label(top,text="",bg="#101C32",fg="#FFFFFF",font=("Arial",12,"bold"));self.game_timer_label.pack(side="right")
        self.game_question_label=tk.Label(panel,text="",bg="#101C32",fg="#FFFFFF",font=("Arial",22,"bold"),wraplength=900,justify="center",height=4)
        self.game_question_label.pack(fill="x",pady=16)
        self.game_answer_label=tk.Label(panel,text="",bg="#101C32",fg="#8BE0B4",font=("Arial",16,"bold"),wraplength=900,justify="center")
        self.game_answer_label.pack(fill="x",pady=8)
        scorebar=tk.Frame(self.area,bg=BG);scorebar.pack(fill="x",padx=10,pady=6)
        self.game_score_label=tk.Label(scorebar,text="",bg=BG,fg=INK,font=("Arial",13,"bold"));self.game_score_label.pack(side="left")
        controls=tk.Frame(self.area,bg=BG);controls.pack(fill="x",padx=10,pady=8)
        self.button(controls,"▶ Iniciar tempo",self.game_start_timer,BLUE).pack(side="left",padx=3)
        self.button(controls,"Revelar resposta",self.game_reveal,GREEN).pack(side="left",padx=3)
        self.button(controls,"+1 Equipe A",lambda:self.game_add_point(0),CYAN).pack(side="left",padx=3)
        self.button(controls,"+1 Equipe B",lambda:self.game_add_point(1),PURPLE).pack(side="left",padx=3)
        self.button(controls,"Próxima rodada →",self.game_next,ORANGE).pack(side="right",padx=3)
        self.game_render()

    def game_render(self):
        q=self.game_questions[self.game_index]
        self.game_round_label.config(text=f"RODADA {self.game_index+1}/{len(self.game_questions)}  •  {q[0].upper()}")
        self.game_question_label.config(text=q[1]);self.game_answer_label.config(text="Resposta oculta — discuta com a turma.")
        self.game_timer_label.config(text=f"TEMPO: {q[4]}");self.game_revealed=False
        self.game_score_label.config(text=f"EQUIPE A  {self.game_score[0]} pontos     |     EQUIPE B  {self.game_score[1]} pontos")

    def game_reveal(self):
        if self.game_revealed:return
        q=self.game_questions[self.game_index]
        self.game_answer_label.config(text=f"RESPOSTA: {q[2]}\n{q[3]}")
        self.game_revealed=True
        if self.game_timer_id:
            self.root.after_cancel(self.game_timer_id);self.game_timer_id=None

    def game_add_point(self,team):
        self.game_score[team]+=1
        self.game_score_label.config(text=f"EQUIPE A  {self.game_score[0]} pontos     |     EQUIPE B  {self.game_score[1]} pontos")

    def game_start_timer(self):
        if self.game_timer_id:self.root.after_cancel(self.game_timer_id)
        try:
            self.game_seconds=int(self.game_questions[self.game_index][4].split()[0])
        except Exception:
            self.game_seconds=30
        self.game_tick()

    def game_tick(self):
        self.game_timer_label.config(text=f"TEMPO: {self.game_seconds}s")
        if self.game_seconds<=0:
            self.game_timer_id=None;self.game_timer_label.config(text="TEMPO ESGOTADO — revele a resposta")
            return
        self.game_seconds-=1;self.game_timer_id=self.root.after(1000,self.game_tick)

    def game_next(self):
        if self.game_timer_id:
            self.root.after_cancel(self.game_timer_id);self.game_timer_id=None
        if self.game_index<len(self.game_questions)-1:
            self.game_index+=1;self.game_render()
        else:
            winner="Empate!" if self.game_score[0]==self.game_score[1] else ("Equipe A venceu!" if self.game_score[0]>self.game_score[1] else "Equipe B venceu!")
            messagebox.showinfo("Fim da batalha",f"{winner}\nEquipe A: {self.game_score[0]} pontos\nEquipe B: {self.game_score[1]} pontos")
            self.game_index=0;self.game_score=[0,0];self.game_render()

    def page_lab(self):
        self.heading("Laboratório: explore livremente","Use as ferramentas para experimentar, testar conjecturas e praticar operações.")
        c=self.card("Explorador geométrico",CYAN);self.make_complex_plot(c,(3,2),650,390)
        c=self.card("Gerador de exercícios",PURPLE)
        self.para(c,"Gere operações aleatórias e resolva informando as partes real e imaginária.")
        self.quiz_box=tk.Frame(c,bg=CARD);self.quiz_box.pack(fill="x");self.new_practice_question()

    def new_practice_question(self):
        for w in self.quiz_box.winfo_children():w.destroy()
        a,b,cc,d=[random.randint(-5,5) for _ in range(4)];op=random.choice(["+","−","×"]);z1=complex(a,b);z2=complex(cc,d)
        ans=z1+z2 if op=="+" else z1-z2 if op=="−" else z1*z2
        tk.Label(self.quiz_box,text=f"({self.cfmt(z1)})  {op}  ({self.cfmt(z2)})",bg=CARD,fg=ORANGE,font=("Arial",19,"bold")).pack(anchor="w",pady=8)
        row=tk.Frame(self.quiz_box,bg=CARD);row.pack(anchor="w");tk.Label(row,text="Parte real",bg=CARD,fg=MUTED).pack(side="left");er=self.entry(row,"",7);tk.Label(row,text="Parte imaginária",bg=CARD,fg=MUTED).pack(side="left",padx=(12,0));ei=self.entry(row,"",7)
        fb=tk.Label(self.quiz_box,text="",bg=CARD,fg=GREEN);fb.pack(anchor="w",pady=6)
        def check():
            try:r=float(er.get().replace(',','.'));i=float(ei.get().replace(',','.'))
            except ValueError:fb.config(text="Preencha os dois campos com números.",fg=RED);return
            fb.config(text="Correto! Muito bem." if abs(r-ans.real)<1e-8 and abs(i-ans.imag)<1e-8 else f"Não foi dessa vez. Resultado: {self.cfmt(ans)}",fg=GREEN if abs(r-ans.real)<1e-8 and abs(i-ans.imag)<1e-8 else ORANGE)
        self.button(self.quiz_box,"Conferir",check,BLUE).pack(anchor="w",pady=3);self.button(self.quiz_box,"Nova questão",self.new_practice_question,PURPLE).pack(anchor="w",pady=3)

                                            
    def open_bank(self):
        self.mode="bank";self.clear();self.stage_label.config(text="RECURSOS DIDÁTICOS  •  BANCO DE IMAGENS")
        self.progress.pack_forget();self.nav.pack_forget()
        self.heading("Banco de imagens e apresentações","Guarde fotos ou digitalizações de exercícios e transforme-as em slides para projetar durante a aula.")
        left=tk.Frame(self.area,bg=CARD,padx=15,pady=15);left.pack(fill="both",expand=True,padx=8,pady=6)
        tk.Label(left,text="IMAGENS DISPONÍVEIS",bg=CARD,fg=CYAN,font=("Arial",13,"bold")).pack(anchor="w")
        self.image_list=tk.Listbox(left,selectmode=tk.EXTENDED,bg="#F7F9FC",fg=INK,selectbackground=BLUE,relief="flat",font=("Arial",10),height=12)
        self.image_list.pack(fill="both",expand=True,pady=9)
        row=tk.Frame(left,bg=CARD);row.pack(fill="x")
        self.button(row,"＋ Adicionar imagens",self.add_images,BLUE).pack(side="left",padx=(0,6));self.button(row,"Remover selecionadas",self.remove_images,RED).pack(side="left")
        self.button(left,"▶ Criar apresentação",self.create_slides,GREEN).pack(anchor="w",pady=10)
        self.para(left,"As imagens ficam na pasta banco_imagens_complexos, ao lado do programa. JPG/JPEG/WEBP requer Pillow; PNG e GIF costumam funcionar sem ele.",10,MUTED)
        self.refresh_images()
    def refresh_images(self):
        self.images=[];self.image_list.delete(0,tk.END)
        for name in sorted(os.listdir(self.bank_dir)):
            if name.lower().endswith((".png",".gif",".bmp",".ppm",".pgm",".jpg",".jpeg",".webp")):
                self.images.append(os.path.join(self.bank_dir,name));self.image_list.insert(tk.END,name)
        if not self.images:self.image_list.insert(tk.END,"Banco vazio — adicione imagens acima.")
    def add_images(self):
        files=filedialog.askopenfilenames(title="Selecione imagens",filetypes=[("Imagens","*.png *.gif *.bmp *.jpg *.jpeg *.webp *.ppm *.pgm"),("Todos","*.*")])
        n=0
        for src in files:
            name=os.path.basename(src);base,ext=os.path.splitext(name);dst=os.path.join(self.bank_dir,name);k=1
            while os.path.exists(dst):dst=os.path.join(self.bank_dir,f"{base}_{k}{ext}");k+=1
            try:shutil.copy2(src,dst);n+=1
            except OSError as ex:messagebox.showerror("Erro",str(ex))
        self.refresh_images();messagebox.showinfo("Banco atualizado",f"{n} imagem(ns) adicionada(s).")
    def remove_images(self):
        sel=self.image_list.curselection()
        if not sel:return
        if not messagebox.askyesno("Confirmar","Apagar as imagens selecionadas do banco?"):return
        for i in sel:
            if i<len(self.images):
                try:os.remove(self.images[i])
                except OSError:pass
        self.refresh_images()
    def create_slides(self):
        sel=self.image_list.curselection();self.slides=[self.images[i] for i in sel if i<len(self.images)] if sel else list(self.images)
        if not self.slides:messagebox.showwarning("Banco vazio","Adicione imagens primeiro.");return
        self.slide_index=0;self.show_slide()
    def show_slide(self):
        self.mode="slides";self.clear();self.nav.pack_forget();self.progress.pack_forget()
        self.stage_label.config(text=f"APRESENTAÇÃO  •  SLIDE {self.slide_index+1}/{len(self.slides)}")
        self.heading("Apresentação de exercícios", "Use os controles fixos abaixo da imagem para navegar.")
        self.slide_name=tk.Label(self.area,text=os.path.basename(self.slides[self.slide_index]),bg=BG,fg=ORANGE,font=("Arial",11,"bold"));self.slide_name.pack(anchor="w",padx=10)
        self.image_label=tk.Label(self.area,bg="#FFFFFF",fg=INK,text="Carregando imagem…",font=("Arial",12));self.image_label.pack(fill="both",expand=True,padx=10,pady=8,ipady=120)
        self.image_label.bind("<Configure>",lambda _:self.root.after(100,self.render_slide_image));self.render_slide_image()
        controls=tk.Frame(self.area,bg=BG);controls.pack(fill="x",padx=10,pady=10)
        self.button(controls,"← Anterior",self.slide_prev,CARD2).pack(side="left")
        self.button(controls,"Voltar ao banco",self.open_bank,PURPLE).pack(side="right",padx=5)
        self.button(controls,"Próximo →",self.slide_next,BLUE).pack(side="right")
    def render_slide_image(self):
        if self.mode!="slides" or not hasattr(self,"image_label") or not self.image_label.winfo_exists():return
        path=self.slides[self.slide_index];w=max(self.image_label.winfo_width()-25,400);h=max(self.image_label.winfo_height()-25,300)
        try:
            from PIL import Image,ImageTk
            im=Image.open(path).convert("RGB");res=getattr(Image,"Resampling",Image);im.thumbnail((w,h),res.LANCZOS);self.photo=ImageTk.PhotoImage(im)
        except ImportError:
            try:
                im=tk.PhotoImage(file=path);factor=max(1,math.ceil(max(im.width()/w,im.height()/h)));self.photo=im.subsample(factor,factor)
            except Exception as ex:self.image_label.config(text=f"Não foi possível abrir. Para JPG/WEBP, instale Pillow.\n{ex}",image="");return
        except Exception as ex:self.image_label.config(text=f"Erro ao abrir imagem: {ex}",image="");return
        self.image_label.config(image=self.photo,text="")
    def slide_prev(self):
        if self.slide_index>0:self.slide_index-=1;self.show_slide()
    def slide_next(self):
        if self.slide_index<len(self.slides)-1:self.slide_index+=1;self.show_slide()
    def return_lesson(self):
        self.mode="lesson";self.progress.pack(fill="x",padx=22,pady=(3,7));self.nav.pack(side="bottom",fill="x",padx=22,pady=(7,13));self.show_step()

if __name__ == "__main__":
    root=tk.Tk();app=ComplexosApp(root);root.mainloop()
