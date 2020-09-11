from tkinter import *               # ventana
from tkinter import Menu            # barra de tareas
from tkinter import filedialog      # filechooser
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box

#from analyzer import lexer           # llamando a una funcion externa
from analyzerjs import AnalyzerJS
from analyzercss import AnalyzerCSS
from analyzerhtml import AnalyzerHTML

class GUI:
    # Metodo que contiene la definicion de la interfaz grafica 
    def __init__(self):
        
        self.window = Tk()
        self.txtEntrada = Entry(self.window,width=10)
        self.txtConsola = Entry(self.window,width=10)
        # Propiedades de la ventana
        self.window.title("Proyecto 1 - ML WEB EDITOR")
        self.window.geometry('1000x750')
        self.window.configure(bg = '#9ACFEF')
        #self.lbl = Label(self.window, text="ML WEB EDITOR", font=("Arial Bold", 15))
        #self.lbl.place(x=440, y = 10)

        # propiedades del menu 
        self.menu = Menu(self.window)
        self.file_item = Menu(self.menu)  #Menu File
        self.file_item.add_command(label='Open File', command=self.abrirFile)
        self.file_item.add_separator()
        self.file_item.add_command(label='Analyze')
        self.file_item.add_separator()
        self.file_item.add_command(label='Exit')

        self.report_item = Menu(self.menu)    # menu Reports
        self.report_item.add_separator()
        self.report_item.add_command(label='Errors')
        self.report_item.add_separator()
        self.report_item.add_command(label='Tree')

        self.menu.add_cascade(label='File', menu=self.file_item)
        self.menu.add_cascade(label='Reports', menu=self.report_item)
        self.window.config(menu=self.menu)
        
        # propiedades del textarea

        
        self.txtEntrada = scrolledtext.ScrolledText(self.window,width=90,height=20)  
        
        # textArea Entrada
        self.txtEntrada.place(x=50, y = 60)
        self.txtEntrada.insert("1.0", """/*\n\nEste\nes un \ncomentario \n@ multilínea\n\n*/\n\nvar int = 1\nvar string ="4"\nvar char = '4'\nvar boolean = true\n\nvar edad = 18;\nif(edad >= 18) {\nconsole.log("Eres mayor de edad");\n} else {\nconsole.log("Todavía eres menor de\nedad")""")
        #Background = color de fondo
        #Foreground = color de las letras
        #self.txtEntrada.insert("0.0", "")
        #self.txtEntrada.tag_add("formato", 1.0,15.0, foreground="blue")
        self.txtEntrada.tag_configure("formato", foreground="blue")

        self.lblConsole = Label(self.window, text="Console:")  #label 
        self.lblConsole.place(x=50, y = 465)
        # textArea consola
        self.txtConsola = scrolledtext.ScrolledText(self.window,width=90,height=10)   
        self.txtConsola.place(x=50, y = 490)
        self.btn = Button(self.window, text="Analizar JS", bg="black", fg="white", command=self.AnalizarJS)    #btn Analyze
        self.btn.place(x=0, y = 0)
        self.btncss = Button(self.window, text="Analizar CSS", bg="black", fg="white", command=self.AnalizarCSS)    #btn Analyze
        self.btncss.place(x=100, y = 0)
        self.btnhtml = Button(self.window, text="Analizar HTML", bg="black", fg="white", command=self.AnalizarHTML)    #btn Analyze
        self.btnhtml.place(x=215, y = 0)
        # Dispara la interfaz
        self.txtEntrada.mainloop()
        self.window.mainloop()

    def AnalizarJS(self):
        entrada = self.txtEntrada.get("1.0", END) #fila 1 col 0 hasta fila 2 col 10
        #entrada = "hola("
        analisis = AnalyzerJS()
        retorno = analisis.lexer(entrada)
        self.txtConsola.delete("1.0", END)
        self.txtConsola.insert("1.0", retorno)
        messagebox.showinfo('Project 1', 'Analysis Finished')

    def AnalizarCSS(self):
        entrada = self.txtEntrada.get("1.0", END) #fila 1 col 0 hasta fila 2 col 10
        #entrada = "hola("
        analisis = AnalyzerCSS()
        retorno = analisis.lexer(entrada)
        self.txtConsola.delete("1.0", END)
        self.txtConsola.insert("1.0", retorno)
        messagebox.showinfo('Project 1', 'Analysis Finished')
    
    def AnalizarHTML(self):
        entrada = self.txtEntrada.get("1.0", END) #fila 1 col 0 hasta fila 2 col 10
        #entrada = "hola("
        analisis = AnalyzerHTML()
        retorno = analisis.lexer(entrada)
        self.txtConsola.delete("1.0", END)
        self.txtConsola.insert("1.0", retorno)
        messagebox.showinfo('Project 1', 'Analysis Finished')

    # Dispara el Filechooser
    def abrirFile(self):
        nameFile=filedialog.askopenfilename(title = "Seleccione archivo",filetypes = (("js files","*.js"), ("html files","*.html"),("css files","*.css"),("All Files","*.*")))
        if nameFile!='':
            archi1=open(nameFile, "r", encoding="utf-8")
            contenido=archi1.read()
            archi1.close()
            self.txtEntrada.delete("1.0", END) 
            self.txtEntrada.insert("1.0", contenido)


start = GUI()

"""from tkinter import *

root = Tk()
root.title("Mi editor")

def nuevo():
    mensaje.set('Nuevo fichero')

def abrir(): 
    mensaje.set('Nuevo fichero')

def guardar():
    mensaje.set('Guardar fichero')

def guardar_como():
    print("Guardar fichero como")

# Menú superior
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=nuevo)
filemenu.add_command(label="Abrir", command=abrir)
filemenu.add_command(label="Guardar", command=guardar)
filemenu.add_command(label="Guardar como", command=guardar_como)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)

# Caja de texto central
texto = Text(root)
texto.pack(fill='both', expand=1)
texto.config(padx=6, pady=4, bd=0, font=("Consolas", 12))

# Monitor inferior
mensaje = StringVar()
mensaje.set('Bienvenido a tu editor')
monitor = Label(root, textvar=mensaje, justify='right')
monitor.pack(side='left')

# Menu y bucle de la aplicación
root.config(menu=menubar)
root.mainloop()"""

"""from tkinter import *
root = Tk()

class EditorClass(object):
    UPDATE_PERIOD = 100 #ms
    editors = []
    updateId = None
    
    def __init__(self, master):
        self.__class__.editors.append(self)
        self.lineNumbers = ''
        # Este es un marco para contener los tres componentes del widget
        self.frame = Frame(master, bd=2, relief=SUNKEN)
        # Esta es la barra de desplazamiento vertical de los widgets
        self.vScrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.vScrollbar.pack(fill='y', side=RIGHT)
        # El widget de texto que contiene los números de línea.
        self.lnText = Text(self.frame,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = 'lightgrey',
                foreground = 'black',
                state='disabled'
        )
        self.lnText.pack(side=LEFT, fill='y')
        # El widget Text es el principal
        self.text = Text(self.frame,
                width=16,
                bd=0,
                padx = 4,
                undo=True,
                background = 'white'
        )
        self.text.pack(side=LEFT, fill=BOTH, expand=1)
        self.text.config(yscrollcommand=self.vScrollbar.set)
        self.vScrollbar.config(command=self.text.yview)
        if self.__class__.updateId is None:
            self.updateAllLineNumbers()
    def getLineNumbers(self):
        x = 0
        line = '0'
        col= ''
        ln = ''
        # assume each line is at least 6 pixels high
        step = 6
        nl = '\n'
        lineMask = '    %s\n'
        indexMask = '@0,%d'
        for i in range(0, self.text.winfo_height(), step):
            ll, cc = self.text.index( indexMask % i).split('.')
            if line == ll:
                if col != cc:
                    col = cc
                    ln += nl
            else:
                line, col = ll, cc
                ln += (lineMask % line)[-5:]
        return ln
    
    def updateLineNumbers(self):
        tt = self.lnText
        ln = self.getLineNumbers()
        if self.lineNumbers != ln:
            self.lineNumbers = ln
            tt.config(state='normal')
            tt.delete('1.0', END)
            tt.insert('1.0', self.lineNumbers)
            tt.config(state='disabled')
    
    @classmethod
    def updateAllLineNumbers(cls):
        if len(cls.editors) < 1:
            cls.updateId = None
            return
        for ed in cls.editors:
            ed.updateLineNumbers()
        cls.updateId = ed.text.after(
            cls.UPDATE_PERIOD,
            cls.updateAllLineNumbers)

def demo(noOfEditors, noOfLines):
    pane = PanedWindow(root, orient=HORIZONTAL, opaqueresize=True)
    for e in range(noOfEditors):
        ed = EditorClass(root)
        pane.add(ed.frame)
    s = 'line ................................... %s'
    s = '\n'.join( s%i for i in range(1, noOfLines+1) )
    for ed in EditorClass.editors:
        ed.text.insert(END, s)
    pane.pack(fill='both', expand=1)
    root.title("Example - Line Numbers For Text Widgets")
if __name__ == '__main__':
    demo(3, 9999)
    mainloop()"""