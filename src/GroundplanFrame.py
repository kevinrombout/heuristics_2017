from Tkinter import *

class GroundplanFrame(object):
    MARGINLEFT = 25
    MARGINTOP = 25
    
    COLOR_WATER = "blue"
    COLOR_PLAYGROUND = "green" 
    
    def __init__(self, plan):
        self.SCALE = 3
        self.root = Tk()
        self.plan = plan
        
        self.frame = Frame(self.root, width=1024, height=768, colormap="new")
        self.frame.pack(fill=BOTH,expand=1)
        
        self.label = Label(self.frame, text="Heuristieken 2016 - Amstelhaege!")
        self.label.pack(fill=X, expand=1)
        
        self.canvas = Canvas(self.frame, 
                             bg="white", 
                             width=self.plan.getWidth()*self.SCALE, 
                             height=self.plan.getHeight()*self.SCALE,
                             cursor="plus")
        
        self.canvas.bind("<Button-1>", self.processMouseEvent)
        self.canvas.focus_set()
        
        self.text = Text(self.root, bd=4, width=80, height=2)
        
    def setPlan(self):
        count = 1
        for residence in self.plan.getResidences():
            if count <= 100:
                self.canvas.create_rectangle(residence.getX()*self.SCALE, 
                                             residence.getY()*self.SCALE,
                                             (residence.getX()+residence.getWidth())*self.SCALE,
                                             (residence.getY()+residence.getHeight())*self.SCALE,
                                             fill=residence.getColor())
                self.canvas.create_text(residence.getX()*self.SCALE, 
                                             residence.getY()*self.SCALE,
                                             text=count)            
                # self.canvas.create_text(residence.getX(),residence.getY(), text=count)
                count = count+1
                
        for waterbody in self.plan.getWaterbodies():
            self.canvas.create_rectangle(waterbody.getX()*self.SCALE, 
                                         waterbody.getY()*self.SCALE,
                                         (waterbody.getX()+waterbody.getWidth())*self.SCALE,
                                         (waterbody.getY()+waterbody.getHeight())*self.SCALE,
                                         fill=self.COLOR_WATER)
            
        for playground in self.plan.getPlaygrounds():
            self.canvas.create_rectangle(playground.getX()*self.SCALE, 
                                         playground.getY()*self.SCALE,
                                         (playground.getX()+playground.getWidth())*self.SCALE,
                                         (playground.getY()+playground.getHeight())*self.SCALE,
                                         fill=self.COLOR_PLAYGROUND)
        
        self.text.insert(INSERT, "Value of plan is: ")
        self.text.insert(INSERT, self.plan.getPlanValue())
        
        self.canvas.pack()
        self.text.pack(fill=BOTH, expand=1)
        
        self.root.update()

    def repaint(self, newPlan):
        self.text.delete(1.0, END)
        self.canvas.delete("all")
        self.plan = newPlan
        self.setPlan()
            
    def processMouseEvent(self, event):
        coordinates = ((event.x/self.SCALE), ",", (event.y/self.SCALE))
        self.canvas.create_text(event.x, event.y, text = coordinates)