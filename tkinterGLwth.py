class gl2d:
    def __init__(self):
        import tkinter as tRef
        self.tRef = tRef
        self.togDyn = True
        self.objsList = []
        pass
    def setWidthHeight(self, w = 200, h = 200):
        self.width = w
        self.height = h
        self.gui.geometry(w,h)
        pass
    def setup(self):
        self.gui = self.tRef.Tk()
        self.cnvi = self.tRef.Canvas(self.gui)
        self.cnvi.place(x=0,y=0)
        self.cnva = self.tRef.Canvas(self.gui)
        self.cnva.place(x=0,y=0)
        self.cnv = self.cnvi
        return self.cnv
    def mloop(self):
        self.gui.mainloop()
        return
    def updateDisplay(self,lineCoordsList): #UPDATE DISPLAY
        for linexyxy in lineCoordsList:
            self.cnv.create_line(linexyxy[0],linexyxy[1],linexyxy[2],linexyxy[3])
        self.flipBuffer()
        return True
    def flipBuffer(self):
        if self.togDyn:
            self.tRef.Misc.lift(self.cnvi)
            self.cnv = self.cnva
            self.cnv.delete('all')
            self.togDyn = False
        else:
            self.tRef.Misc.lift(self.cnva)
            self.cnv = self.cnvi
            self.cnv.delete('all')
            self.togDyn = True
        self.gui.update()
    def loadObj(self,objFile,objName,closeLoop=True):
        with open(objFile) as file:
            vrtxList = file.readlines()
        num = len(vrtxList)
        if not closeLoop:
            num -= 1
        vrtxList.append(vrtxList[0])
        clList = []
        for cl in vrtxList:
            clList.append([float(cl.replace('\n','').split(',')[0]),float(cl.replace('\n','').split(',')[1])])
        coords = []
        for i in range(num):
            coords.append([clList[i][0],clList[i][1],clList[i+1][0],clList[i+1][1]])
        
        self.objsList.append([objName, coords])
    def getObj(self, objName):
        tC = 0
        tV = len(self.objsList)
        objFound = False
        objVcs= []
        while(1):
            if tC < tV:
                if self.objsList[tC][0] == objName:
                    objVcs = self.objsList[tC][1]
                    objFound = True
                    break
                tC += 1
            else:
                break

        if objFound:
            return objVcs
        return []
    def applyOffset(obj,xInc,yInc):
        newcd = []
        for cd in obj:
            cda = cd[0]+xInc
            cdb = cd[2]+xInc
            if cda < cdb:
                newcd.append([cd[0]+xInc,cd[1]+yInc,cd[2]+xInc,cd[3]+yInc])
            else:
                newcd.append([cd[2]+xInc,cd[3]+yInc,cd[0]+xInc,cd[1]+yInc])
        return newcd

class newObj:
    def __init__(self,objFile,objName,closeLoop=True):
        self.objLnList = []
        with open(objFile) as file:
            vrtxList = file.readlines()
        num = len(vrtxList)
        if not closeLoop:
            num -= 1
        vrtxList.append(vrtxList[0])
        clList = []
        for cl in vrtxList:
            clList.append([float(cl.replace('\n','').split(',')[0]),float(cl.replace('\n','').split(',')[1])])
        coords = []
        for i in range(num):
            self.objLnList.append([clList[i][0],clList[i][1],clList[i+1][0],clList[i+1][1]])
    def applyOffset(self,xInc,yInc):
        newcd = []
        for cd in self.objLnList:
            newcd.append([cd[0]+xInc,cd[1]+yInc,cd[2]+xInc,cd[3]+yInc])
        self.objLnList = newcd
        return
    def getLnList(self):
        return self.objLnList
