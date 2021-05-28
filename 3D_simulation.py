import pygame,sys, math
import random

pygame.init()
w,h = 600,600               #Dimensions of window
cx,cy = w//2,h//2           #Center of window
clock=pygame.time.Clock()
screen=pygame.display.set_mode((w,h))

#pygame.event.get()
#pygame.mouse.get_rel()



class Box():
    vertices= (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    def __init__(self,pos=[0,0,0],length=[1,1,1]):
        self.verts =[ [ (a/2+pos[0])*length[0] ,(b/2+pos[1])*length[1]  ,(c/2+pos[2])*length[2]  ] for a,b,c in self.vertices]
        self.edges= [0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]
        self.faces=[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[0,3,7,4],[1,2,6,5]
class View():
    def __init__(self,pos=(0,0,0),rad=0):
        self.pos=list(pos)
        self.rad=rad
    def update(self,key):
        c=0.2
        x,y,z=0,0,0
        if key[pygame.K_a]: x -=c
        if key[pygame.K_s]: z +=c
        if key[pygame.K_d]: x +=c
        if key[pygame.K_w]: z -=c
        if key[pygame.K_q]: y -=c
        if key[pygame.K_e]: y +=c
        if key[pygame.K_y]: self.rad +=0.005

        x,z = rot2d(x,z,self.rad)

        self.pos[0] += x;  self.pos[1] += y; self.pos[2] += z
        
def rot2d(x,y,rad):
    a = x*math.cos(rad) - y*math.sin(rad)
    b = x*math.sin(rad) + y*math.cos(rad)
    return (a,b)
    
def update_obj(box,screen,view,rad,size):
    edges=box.edges
    for edge in edges:
        x0,y0,z0 =box.verts[edge[0]][0]-view[0],box.verts[edge[0]][1]-view[1],box.verts[edge[0]][2]-view[2]
        x1,y1,z1 =box.verts[edge[1]][0]-view[0],box.verts[edge[1]][1]-view[1],box.verts[edge[1]][2]-view[2]
        x0,z0=  rot2d(x0,z0,rad)
        x1,z1=  rot2d(x1,z1,rad) 
        if z0>0 and z1>0:
            f0=size/(z0+0.05)    #factor of proporcionalidade
            f1=size/(z1+0.05)
            vert0= ( (x0)*f0 +cx ,    (y0)*f0 +cy)
            vert1= ( (x1)*f1 +cx ,    (y1)*f1 +cy)
            #rotation
            pygame.draw.line(screen,(255,255,255),vert0,vert1,1)
            
        elif z0<0 and z1>0: #one face behing you
            f0=size/(0.05)    #factor of proporcionalidade
            f1=size/(z1+0.05)
            vert0= ( (x0)*f0 +cx ,    (y0)*f0 +cy)
            vert1= ( (x1)*f1 +cx ,    (y1)*f1 +cy)
            #rotation
            pygame.draw.line(screen,(255,255,255),vert0,vert1,1)
        elif z0>0 and z1<0: #one face behing you
            f0=size/(z0+0.05)    #factor of proporcionalidade
            f1=size/(0.05)
            vert0= ( (x0)*f0 +cx ,    (y0)*f0 +cy)
            vert1= ( (x1)*f1 +cx ,    (y1)*f1 +cy)
            #rotation
            pygame.draw.line(screen,(255,255,255),vert0,vert1,1)


            
    
def main():           
    size=50
    box=[]
    circle_obj=100
    aumento=2*math.pi/circle_obj
    for i in range(circle_obj):
        #box.append(Box((random.randint(0,4),random.randint(0,4),2), (random.randint(1,4),random.randint(1,4),random.randint(1,3))))
        box.append(Box((4*math.cos(aumento*i),0,4*math.sin(aumento*i)), (3,3,3) )  )
        box.append(Box((0,4*math.cos(aumento*i),4*math.sin(aumento*i)), (3,3,3) )  )
        box.append(Box((4*math.cos(aumento*i),4*math.sin(aumento*i),0), (3,3,3) )  )
    a,b,c=255,255,255
    view=View()
    while 1:
        screen.fill([0,0,0])
        dt=clock.tick()/1000
        for event in pygame.event.get():
            if event.type==pygame.QUIT:pygame.quit();sys.exit()
        for j in range(len(box)):
            update_obj(box[j],screen,view.pos,view.rad,size)
        pygame.display.flip()
        key = pygame.key.get_pressed()
        view.update(key)
        #print(key)

main()