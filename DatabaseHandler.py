class DatabaseHandler:
    def __init__(self, databasefilename):
        if databasefilename[-4:] != ".txt":
            self.databasefile = databasefilename + ".txt"
        else:
            self.databasefile = databasefilename
        try:
            open(self.databasefile, "r").close()
        except:
            open(self.databasefile, "a").close()
            newdbwrite = open(self.databasefile, "w")
            newdbwrite.write("UserID,Money,Rank\n")
            newdbwrite.close()

    def changedb(self, newdbcontent):
        content = str(newdbcontent)
        open(self.databasefile, "w").close()
        dbfile = open(self.databasefile, "w")
        dbfile.write(content)
        dbfile.close()

    def datagrab(self, Key):
        self.updaterows()
        key = str(Key)
        with open(self.databasefile, "r") as dbfile:
            dblines = dbfile.readlines()[1:]
            for x in range(len(dblines)):
                dbline = dblines[x].replace("\n", "")
                linedata = dbline.split(",")
                if linedata[0] == key:
                    return [linedata, x]
        return None

    def valueget(self, valueID, Key):
        valID = str(valueID)
        key = str(Key)
        with open(self.databasefile, "r") as dbfile:
            valueids = dbfile.readlines()[0].replace("\n", "")
            valueids = valueids.split(",")
            for x in range(len(valueids)):
                if valueids[x] == valID:
                    return [self.datagrab(key)[0][x], x]
        print("No value id : " + valID)

    def valueupdate(self, valueID, Key, newvalue):
        valID = str(valueID)
        key = str(Key)
        update = str(newvalue)
        self.updaterows()
        try:
            with open(self.databasefile, "r") as dbfile:
                dblines = dbfile.readlines()
            data = self.datagrab(key)
            data[0][self.valueget(valID, key)[1]] = update
            dblines[data[1]+1] = ",".join(data[0]) + "\n"
            self.changedb("".join(dblines))
        except:
            print("Could not update " + valID + " for " + key + " to new value " + update)

    def newkey(self, newkey):
        nkey = str(newkey)
        tempflag = False
        if self.datagrab(nkey) == None:
            with open(self.databasefile, "r") as dbfile:
                try:
                    dbcoms = dbfile.readlines()[0].count(",")
                except:
                    tempflag = True
            if tempflag == True:
                newdb = open(self.databasefile, "w")
                newdb.write("UserID,Money,Rank\n")
                newdb.close()
                dbcoms = dbfile.readlines()[0].count(",")
            for x in range(dbcoms):
                nkey += ",0"
            with open(self.databasefile, "r") as dbfile:
                dbcontent = dbfile.read() + nkey + "\n"
            self.changedb(dbcontent)
            nkey = str(newkey)
            #New user defaults:

            #self.valueupdate("Money", nkey, 25)
            #self.valueupdate("Commands_Used", nkey, 0)
            
            return True
        else:
            return False

    def delcol(self, valueID):
        valID = str(valueID)
        self.z = 0
        self.tempstr = ""
        self.templine = []
        with open(self.databasefile, "r") as dbfile:
            dbline = str(dbfile.readlines()[0].replace("\n", "")).split(",")
            for x in range(len(dbline)):
                if dbline[x] == valID:
                    self.z = x
        with open(self.databasefile, "r") as dbfile:
            dblines = dbfile.readlines()
        for x in range(len(dblines)):
            self.templine = (dblines[x].replace("\n", "")).split(",")
            self.templine.pop(self.z)
            self.tempstr += ",".join(self.templine) + "\n"
        self.changedb(self.tempstr)

    def updaterows(self):
        self.tempstr = ""
        with open(self.databasefile, "r") as dbfile:
            filelines = dbfile.readlines()
            comcount = filelines[0].count(",")
            filelines[0] = filelines[0].replace("\n", "")
        with open(self.databasefile, "r") as dbfile:
            readfile = dbfile.read()
        for x in range(len(filelines)-1):
            filelines[x+1] = filelines[x+1].replace("\n", "")
            if filelines[x+1] != "":
                linecom = filelines[x+1].count(",")
                while linecom < comcount:
                    filelines[x+1] += ",0"
                    linecom = filelines[x+1].count(",")
        newfile = "\n".join(filelines) + "\n"
        self.changedb(newfile)

    #Calls--

    #Used to interact with database in a user-friendly method

    def get(self, DataField, Key): #Get a cell value
        return self.valueget(DataField, Key)[0]
    def update(self, DataField, Key, NewValue): #Update a cell value
        self.valueupdate(DataField, Key, NewValue)
    def delid(self, DataField): #Delete a data id column
        self.delcol(DataField)
    def create_user(self, Key): #Creates a new row with given key
        return self.newkey(Key)
