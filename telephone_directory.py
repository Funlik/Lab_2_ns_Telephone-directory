from tkinter import *
import shelve


class PhoneBook:
    def __init__(self, nameBook, dicRec={}):
        self.nameBook = nameBook
        self.dicRec = dicRec

    def loadBook(self):
        db = shelve.open(self.nameBook)
        self.dicRec = dict(db.items())
        db.close()

    def saveBook(self):
        db = shelve.open(self.nameBook)
        for (key, record) in self.dicRec.items():
            db[key] = record
        db.close()


class PhoneRec:
    def __init__(self, keyRec, char, familyName, phone, data, comment, delR=''):
        self.keyRec = keyRec
        self.char = char
        self.data = data
        self.phone = phone
        self.familyName = familyName
        self.comment = comment
        self.delR = delR


fieldnamesRec = ('keyRec', 'char', 'familyName', 'phone', 'data', 'comment', 'delR')
activCh = 'А'
typeRec = ''
dicRem = {}


# Кнопочки и все остальное
#def makeWidgets():
  #  global entriesRec, entRec, lab1
   # entRec = {}
   # window = Tk()
   # window.title('Phone directory')
   # window.geometry('1260x600+0+0')
   # form1 = Frame(window)
   # form1.pack()
   # lab1 = Label(form1, text=activCh, fg="#eee", bg="#333", width=5)
   # lab1.pack(side=LEFT)
   # Label(form1, text='  ', width=30).pack(side=LEFT)
   # alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
   #          "S", "T", "U", "V", "W", "X", "Y", "Z"]
   # for i in range(len(alpha)):
   #     Button(form1, text=alpha[i], command=(lambda x=alpha[i]: fetchChr(x))).pack(side=LEFT)
   # ent = Entry(form1, width=27)
   # ent.pack(side=LEFT)
   # entRec['entFind'] = ent
   # Button(form1, text="Find", command=fetchFind).pack(side=LEFT)

   # form2 = Frame(window)
   # form2.pack()
   # entriesRec = {}
   # for (ix, label) in enumerate(fieldnamesRec):
    #    lab = Label(form2, text=label)
    #    lab.grid(row=2, column=ix)
   # for i in range(1, 26):
   #     for (ix, label) in enumerate(fieldnamesRec):
   #         if label == 'keyRec' or label == 'char' or label == 'delR':
   #             ent = Entry(form2, state='normal', width=6)
   #         else:
   #             ent = Entry(form2, width=40)
   #         ent.grid(row=i + 2, column=ix)
   #         entriesRec[label + str(i)] = ent
   # form3 = Frame(window)
   # form3.pack()
   # Button(window, text="Next page", command=fetchNext).pack()
   # Label(window, text='      ', width=10).pack(side=LEFT)
   # ent = Entry(window, width=10)
   # ent.pack(side=LEFT)
   # entRec['entKeyRec'] = ent
   # Button(window, text="Open", command=openRec).pack(side=LEFT)
   # Button(window, text="Remove", command=delKeyRec).pack(side=LEFT)
   # Label(window, text='      ', width=30).pack(side=LEFT)
   # Label(window, text='      ', width=20).pack(side=LEFT)
   # Button(window, text="Quit", command=fin).pack(side=LEFT)
   # return window#\


# Чистый лист
def clear_sheet():
    for i in range(1, 26):
        for field in fieldnamesRec:
            if field == 'keyRec' or field == 'delR':
                entriesRec[field + str(i)].config(state='normal')
                entriesRec[field + str(i)].delete(0, END)
                entriesRec[field + str(i)].config(state='readonly')
            else:
                entriesRec[field + str(i)].delete(0, END)


def fetchChr(ch):
    global activCh, typeRec, lab1
    saveRec()
    typeRec = ''
    activCh = ch
    lab1.config(text=activCh)
    dicRecChr = {}
    for key in t1.dicRec.keys():
        if t1.dicRec[key].char == ch:
            dicRecChr[key] = t1.dicRec[key]
    fetch(dicRecChr)


def fetch(dicR):
    global dicRem
    clear_sheet()
    count = 1
    dicRe = dicR.copy()
    while count <= 25 and len(dicRe):
        for key in dicR.keys():
            if dicR[key].delR == typeRec:
                record = dicR[key]
                for field in fieldnamesRec:
                    if field == 'keyRec' or field == 'delR':
                        entriesRec[field + str(count)].config(state='normal')
                        entriesRec[field + str(count)].insert(0, getattr(record, field))
                        entriesRec[field + str(count)].config(state='readonly')
                    else:
                        entriesRec[field + str(count)].insert(0, getattr(record, field))
                count += 1
                dicRe.pop(key)
                if count > 25:
                    break
            else:
                dicRe.pop(key)
    dicRem = dicRe.copy()


def fetchNext():
    saveRec()
    fetch(dicRem)


# Физическое удаление из базы данных
def delKeyRec():
    key = entRec['entKeyRec'].get()
    del t1.dicRec[key]
    db = shelve.open(t1.nameBook)
    del db[key]
    db.close()
    for i in range(1, 26):
        if entriesRec['keyRec' + str(i)].get() == key:
            entriesRec['delR' + str(i)].config(state='normal')
            entriesRec['delR' + str(i)].insert(0, 'd')
            entriesRec['delR' + str(i)].config(state='readonly')
    entRec['entKeyRec'].delete(0, END)


def openRec():
    key = entRec['entKeyRec'].get()
    for i in range(1, 26):
        if entriesRec['keyRec' + str(i)].get() == key:
            entriesRec['delR' + str(i)].config(state='normal')
            entriesRec['delR' + str(i)].delete(0, END)
            entriesRec['delR' + str(i)].insert(0, '')
            entriesRec['delR' + str(i)].config(state='readonly')
    entRec['entKeyRec'].delete(0, END)


# Поиск
def fetchFind():
    saveRec()
    clear_sheet()
    strF = entRec['entFind'].get()
    dicFind = {}
    for key in t1.dicRec.keys():
        record = t1.dicRec[key]
        for field in fieldnamesRec:
            if (field != 'keyRec' and field != 'char' and field != 'delR' and
                    getattr(record, field).find(strF) != -1):
                dicFind[key] = record
                break
    fetch(dicFind)


def saveRec():
    global typeRec
    for i in range(1, 26):
        key = entriesRec['keyRec' + str(i)].get()
        if entriesRec['delR' + str(i)].get() == 'd':
            continue
        elif key:
            record = t1.dicRec[key]
            for field in fieldnamesRec:
                setattr(record, field, entriesRec[field + str(i)].get())
            t1.dicRec[key] = record
        else:
            existRec = False
            for field in fieldnamesRec:
                if entriesRec[field + str(i)].get():
                    existRec = True  # Если существует запись в поле на этой строке
            if existRec:
                if entriesRec['char' + str(i)].get():
                    char = entriesRec['char' + str(i)].get().title()
                else:
                    char = activCh
                familyName = entriesRec['familyName' + str(i)].get().title()
                data = entriesRec['data' + str(i)].get()
                phone = entriesRec['phone' + str(i)].get()
                comment = entriesRec['comment' + str(i)].get().title()
                if len(t1.dicRec) > 0:
                    L = sorted(t1.dicRec.items(), key=lambda item: int(item[0]))
                    keyRec = str(int(L[-1][0]) + 1)
                else:
                    keyRec = "1"
                record = PhoneRec(keyRec, char, familyName, phone, data, comment)
                t1.dicRec[keyRec] = record
    t1.saveBook()


def fin():
    saveRec()
    window.destroy()


if __name__ == '__main__':
    t1 = PhoneBook("Телефоны")
    t1.loadBook()

    window = makeWidgets()
    fetchChr('А')
    window.mainloop()
