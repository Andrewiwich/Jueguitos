import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
from functools import partial
import time
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
"""extra functions"""
def find_all_paths(graph, start, end, path=[]):
      path = path + [start]
      if start == end:
          return [path]
      if not start in graph:
          return []
      paths = []
      for node in graph[start]:
          if node not in path:
              newpaths = find_all_paths(graph, node, end, path)
              for newpath in newpaths:
                  paths.append(newpath)
      return paths

def sorthestPath(graph, start, end):
    caminos = find_all_paths(graph, start, end)
    longs = [len(p) for p in caminos]
    short = min(longs)
    return [a for a in caminos if len(a) == short]
    
"""interfaz"""
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Zombis & Supervivientes")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        niveles = [[1,"nivel1.png","nivel1.txt",[2]],[2,"nivel2.png","nivel2.txt",[11,12]],[3,"nivel3.png","nivel3.txt", [11,12]]]
        self.frames = {}
        self.resizable(False,False)
        for F in (StartPage,LevelSelectPage, RulePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        for nv in niveles:
            page_name = "PlayPage" + str(nv[0])
            frame = PlayPage(parent=container, controller=self, number = nv[0], imagen = nv[1], datos = nv[2], posZombies = nv[3])
            
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        path = "zz.png"
        #C:/Users/aecan/Documents/UPM/4º/OPTIMIZACION_Y_JUEGOS/PROYECTO/
        im = Image.open(path)
        ph = ImageTk.PhotoImage(im)

        label = tk.Label(self, image=ph, font=controller.title_font)
        label.image = ph  # need

        label.pack(side="top", fill="x", pady=10)

        playButton = tk.Button(self, bg="PaleGreen1", text="JUGAR",command=lambda: controller.show_frame("LevelSelectPage"))
        # justify="center"
        ruleButton = tk.Button(self, bg="light blue", text="REGLAS",command=lambda: controller.show_frame("RulePage"))
        # , justify="center"
        # ,command=openRules()
        playButton.pack(side="left", expand="True")
        ruleButton.pack(side="right", expand="True")

        ##
        # button1 = tk.Button(self, text="Go to Page One",
        #                     command=lambda: controller.show_frame("PageOne"))
        #         # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()

class LevelSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        im1 = ImageTk.PhotoImage(Image.open("nivel1.png").resize((400,130))) 
        im2 = ImageTk.PhotoImage(Image.open("nivel2.png").resize((400,130))) 
        im3 = ImageTk.PhotoImage(Image.open("nivel3.png").resize((400,130)))  
        
        niv1 = tk.Button(self, image = im1, command=lambda: controller.show_frame("PlayPage1"))
        niv1.image = im1
        niv2 = tk.Button(self, image = im2, command=lambda: controller.show_frame("PlayPage2"))
        niv2.image = im2
        niv3 = tk.Button(self, image = im3, command=lambda: controller.show_frame("PlayPage3"))
        niv3.image = im3

        niv1.pack(side="top", expand="True")
        niv2.pack(side="top", expand="True")
        niv3.pack(side="top", expand="True")

        
class PlayPage(tk.Frame):
    
    
    def __init__(self, parent, controller, number, imagen, datos, posZombies):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        label = tk.Label(self, text="Este es el nivel " + str(number), font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Volver al menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
        background_image = ImageTk.PhotoImage(Image.open(imagen))
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.pack()
        self.crearNodos(datos)
        
        self.survivor = -1#posicion del superviviente
        self.zombiOr = posZombies# posicion del/de los zombie/s
        self.zombi = []
        self.resetZombie()
    
    def resetZombie(self):
        if self.zombi != []:
            for z in self.zombi:
                self.nodos[z].configure(image = self.imNode)
                
        self.zombi = self.zombiOr.copy()# posicion del/de los zombie/s
        for z in self.zombi:
            self.nodos[z].configure(image = self.imZombie)
        
    def crearNodos(self, datos):
        self.imNode = ImageTk.PhotoImage(Image.open("nodo.png"))
        self.imZombie = ImageTk.PhotoImage(Image.open("zombie.png"))
        self.imSurvivor = ImageTk.PhotoImage(Image.open("superv.png"))
        
        self.adyacencias = {} # el grafo es un diccionario
        
        self.nodos = []
        nodes = [line.rstrip('\n') for line in open(datos)]
        j = 0
        for l in nodes:
            posi, ad = l.split(";")
            pos = {j:[int(i) for i in posi.split(",")]}
            self.adyacencias[j] = [int(i) for i in ad.split(",")]
            self.nodos.append(tk.Button(self, command = partial(self.mover, j) , image = self.imNode))
            self.nodos[-1].image = self.imNode
            self.nodos[-1].place(x = pos[j][0], y = 80 + pos[j][1])
            j += 1
        
    def mover(self, pos):
        if pos not in self.zombi:# no puedes colocarte en un zombie
            if self.survivor == -1 or pos in self.adyacencias[self.survivor]:#colocate o muevete a una adyacente
                if self.survivor != -1:
                    self.nodos[self.survivor].configure(image = self.imNode)
                self.survivor = pos
                self.nodos[self.survivor].configure(image = self.imSurvivor)
                z = 0
                while z < len(self.zombi):
                    sorth = sorthestPath(self.adyacencias, self.zombi[z], self.survivor) 
                    l, j = len(sorth), 0
                    moved = False
                    while j < l and not moved and sorth != []:
                        newpos = sorth[j][1]
                        if newpos not in self.zombi:# la casilla no esta ocupada ya por otro zombie
                            time.sleep(0.3)
                            self.nodos[self.zombi[z]].configure(image = self.imNode)
                            self.nodos[newpos].configure(image = self.imZombie)
                            self.zombi[z] = newpos
                            moved = True
                        
                        j += 1
                        
                    z += 1
                
                #comprobar si el superviviente esta bloqueado
                blocked = 0
                for i in self.adyacencias[self.survivor]:
                    blocked += 1 if i in self.zombi else 0
                    
                if blocked == len(self.adyacencias[self.survivor]):
                    showinfo("Message", "El superviviente esta atrapado por zombis... ")
                    time.sleep(0.5)
                    self.resetZombie()
                    self.nodos[self.survivor].configure(image = self.imNode)
                    self.survivor = -1
                    
            else:
               showinfo("Message", "Muevete solo a un nodo adyacente") 
               return
        else:
           showinfo("Message", "No te puedes mover a un nodo con Zombi") 
           return
       
        if self.survivor in self.zombi:
            self.survivor = -1
            showinfo("Message", "Tu superviviente ha sido alcanzado por un Zombi...") 
            time.sleep(0.5)
            self.resetZombie()
    
        
        
class RulePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        ph = ImageTk.PhotoImage(Image.open("rules.png"))

        label = tk.Label(self, image=ph, font=controller.title_font)
        label.image = ph  # need
        label.place(x=0,y=0)
        label.pack(side="top", fill="both", pady=10)

        homeButton = tk.Button(self, bg="light blue", text="Volver al Menu", command=lambda: controller.show_frame("StartPage"))
        #tutorialButton = tk.Button(self, bg="PaleGreen1", text="TUTORIAL",command=lambda: controller.show_frame("TutorialPage"))
        #playButton.pack(side="left", expand="True")
        #tutorialButton.pack()
        homeButton.pack(side="right", expand="True")

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()