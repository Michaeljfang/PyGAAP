#My attempt at creating a PyGaap GUI. Unfinished, do not redistribute. (no-one wants to see this)
#PyGaap is the Python port of JGAAP, Java Graphical Authorship Attribution Program by Patrick Juola
#See https://evllabs.github.io/JGAAP/
#
versiondate="2021.03.30"
#Michael Fang, Boston University.

#REQUIRED MODULES BELOW. USE pip OR pip3 IN YOUR TERMINAL TO INSTALL.

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

topwindow=Tk() #this is the top-level window when you first open PyGAAP
topwindow.title("PyGAAP (GUI, underconstruction)")
topwindow.geometry("1000x620")
#topwindow.iconbitmap()
#topwindow.option_add("*Font", "20")

#BELOW ARE ALL THE FUNCTIONS
def todofunc(): #place holder "to-do function"
    return None

def select_features(ListBoxAv, ListBoxOp, feature, function, label=None):
    """Used by Event Drivers, Event culling etc to add/remove/clear selected features.
    Needs to check if feature is already added."""
    #ListBoxAv: "listbox Available", listbox to choose from
    #ListBoxOp: "listbox operate-on", a list of listboxes to modify. Includes the one in the corresponding tab and the
    #   listbox in the Review & Process tab.
    #feature: is the return of listbox.curselection()
    #function: can be "clear", "remove", or "add"
    #label is the label to update in case the listbox it refers to cannot be empty:
    #   e.g. when the canonicizer listbox is empty, update the "Canonicizers" label to show the listbox cannot be empty
    if function=="clear":
        for listboxmember in ListBoxOp:
            listboxmember.delete(0, END)
        #if label != None:
        #    label.configure(text=label["text"]+" ×")
    elif function=="remove":
        try:
            for listboxmember in ListBoxOp:
                listboxmember.delete(feature)
                listboxmember.select_set(END)
            
        #    if ListBoxOp[0].size()==0 and label != None:
        #        label.configure(text=label["text"]+" ×")
        except:
            print("remove from list: nothing selected")
            return None
    elif function=="add":
        try:
            for listboxmember in ListBoxOp:
                listboxmember.insert(END, ListBoxAv.get(feature))
            #if label != None:
            #    label.configure(text=label["text"][:-2])
        except:
            print("add to list: nothing selected")

    return None

def find_parameters(feature):
    """find parameters in some features to display and set"""
    pass

def find_feature(section, directory):
    """Universal find feature function for:
    canonicizers, event drivers, event culling, analysis methods, and distance functions.
    As the app is starting up,
    this function looks for py or text files (or both?) in PyGaap Directory for those features and extracts information like:
    description to display in the discription textbox;
    location of those py files so PyGAAP GUI can use it;
    parameters of a feature to be stored for execution;

    -others to be determined
    """
    #section: categories in which to find the features like Canonicizers, Event Drivers, Event Cullers etc.
    #directory: where to parse the file tree to find the features.
    pass

def displayAbout():
    global versiondate
    """Displays the About Page"""
    AboutPage=Toplevel()
    AboutPage.title("About PyGaap")
    AboutPage.geometry("600x300")
    AboutPage.resizable(False, False)
    AboutPage_logosource=PhotoImage(file="logo.png")
    AboutPage_logosource=AboutPage_logosource.subsample(2, 2)
    AboutPage_logo=Label(AboutPage, image=AboutPage_logosource)
    AboutPage_logo.pack(side="top", fill="both", expand="yes")

    textinfo="THIS IS AN UNFINISHED VERSION OF PyGAAP GUI.\n\
    Version date: "+versiondate+"\n\
    PyGAAP is a Python port of JGAAP,\n\
    Java Graphical Authorship Attribution Program.\n\
    This is an open-source tool developed by the EVL Lab\n\
    (Evaluating Variation in Language Laboratory)."
    AboutPage_text=Label(AboutPage, text=textinfo)
    AboutPage_text.pack(side='bottom', fill='both', expand='yes')
    AboutPage.mainloop()


Notes_content=""

def notepad():
    """Notes button window"""
    global Notes_content
    NotepadWindow=Toplevel()
    NotepadWindow.title("Notes")
    #NotepadWindow.geometry("600x500")
    NotepadWindow_Textfield=Text(NotepadWindow)
    NotepadWindow_Textfield.insert("1.0", str(Notes_content))
    NotepadWindow_SaveButton=Button(NotepadWindow, text="Save & Close",\
        command=lambda:Notepad_Save(NotepadWindow_Textfield.get("1.0", "end-1c"), NotepadWindow))
    NotepadWindow_Textfield.pack(padx=7, pady=7, expand=True)
    NotepadWindow_SaveButton.pack(pady=(0, 12), expand=True)
    NotepadWindow.mainloop()
    ####Liftwindow when in focus
    return None

def Notepad_Save(text, window):
    """saves the contents displayed in the notepad textfield when the button is pressed"""
    global Notes_content
    Notes_content=text
    window.destroy()
    return None

def switch_tabs(notebook, mode, tabID=0):
    if mode=="next":
        try:
            notebook.select(notebook.index(notebook.select())+1)
            return None
        except:
            return None
    elif mode=="choose":
        try:
            notebook.select(tabID)
            return None
        except:
            return None

def addFile(WindowTitle, ListboxOp, AllowDuplicates, liftwindow=None):
    """Universal add file function to bring up the explorer window"""
    #WindowTitle is the title of the window, may change depending on what kind of files are added
    #ListboxOp is the listbox object to operate on
    #AllowDuplicates is whether the listbox allows duplicates.
    #if listbox does not allow duplicates, item won't be added to the listbox and this prints a message to the terminal.
    #liftwindow is the window to go back to focus when the file browser closes
    filename=askopenfilename(filetypes=(("Text File", "*.txt"), ("All Files", "*.*")), title=WindowTitle)
    if liftwindow != None:
        liftwindow.lift(topwindow)
    if AllowDuplicates and filename !="":
        ListboxOp.insert(END, filename)
    else:
        for fileinlist in ListboxOp.get(0, END):
            if fileinlist==filename:
                print("Add document: file already in list")
                liftwindow.lift()
                return None
        if filename != None:
            ListboxOp.insert(END, filename)

    if liftwindow != None:
        liftwindow.lift()
    return None



KnownAuthors=[]
#KnownAuthors list format: [[author, [file-directory, file-directory]], [author, [file-directory, file directory]]]
KnownAuthorsList=[]
#this decides which in the 1-dimensionl listbox is the author and therefore can be deleted when using delete author

def authorsListUpdater(listbox):
    """This updates the ListBox from the KnownAuthors python-list"""
    global KnownAuthors
    global KnownAuthorsList
    listbox.delete(0, END)
    KnownAuthorsList=[]
    for authorlistindex in range(len(KnownAuthors)):#Authors
        listbox.insert(END, KnownAuthors[authorlistindex][0])
        listbox.itemconfig(END, background="light cyan", selectbackground="sky blue")
        KnownAuthorsList+=[authorlistindex]
        for document in KnownAuthors[authorlistindex][1]:
            listbox.insert(END, document)#Author's documents
            listbox.itemconfig(END, background="gray90", selectbackground="gray77")
            KnownAuthorsList+=[-1]
    return None


def authorSave(window, listbox, author, documentsList, mode):
    """This saves author when adding/editing to the KnownAuthors list. Then uses authorsListUpdater to update the listbox
    """
    #Listbox: the authors listbox.
    #author: 
    #       "ADD MODE": the author's name entered in authorsList window
    #       "EDIT MODE": [original author name, changed author name]
    #documentsList: list of documents entered in the listbox in the authorsList window
    #mode: add or edit
    global KnownAuthors
    if mode=="add":
        if (author != None and author.strip() !="") and (documentsList !=None and len(documentsList)!=0):  
            AuthorIndex=0
            while AuthorIndex<len(KnownAuthors):#check if author already exists
                if KnownAuthors[AuthorIndex][0]==author:#when author is already in the list, merge.
                    KnownAuthors[AuthorIndex][1]=KnownAuthors[AuthorIndex][1]+list([doc for doc in documentsList if doc not in KnownAuthors[AuthorIndex][1]])
                    authorsListUpdater(listbox)
                    window.destroy()
                    return None
                AuthorIndex+=1
            KnownAuthors+=[[author, list([file for file in documentsList if type(file)==str])]]#no existing author found, add.
            authorsListUpdater(listbox)
        window.destroy()
        return None
    elif mode=='edit':
        if (author[1] != None and author[1].strip() !="") and (documentsList !=None and len(documentsList)!=0):
            AuthorIndex=0
            while AuthorIndex<len(KnownAuthors):
                if KnownAuthors[AuthorIndex][0]==author[0]:
                    KnownAuthors[AuthorIndex]=[author[1], documentsList]
                    authorsListUpdater(listbox)
                    window.destroy()
                    return None
                AuthorIndex+=1
            print("coding error: editing author: list of authors and documents changed unexpectedly when saving")
            return None
    else:
        print("coding error: unknown parameter passed to 'authorSave' function: ", str(mode))
    window.destroy()
    return None

def authorsList(authorList, mode):
    """Add, edit or remove authors
    This updates the global KnownAuthors list.
    This opens a window to add/edit authors; does not open a window to remove authors
    """
    #authorList: the listbox that displays known authors in the topwindow.
    #authorList calls authorSave (which calls authorListUpdater) when adding/editing author
    #
    global KnownAuthors
    global KnownAuthorsList
    if mode=="add":
        title="Add Author"
        mode='add'
    elif mode=='edit':
        try:
            authorList.get(authorList.curselection())
            title="Edit Author"
            mode='edit'
            selected=int(authorList.curselection()[0])
            if KnownAuthorsList[selected]==-1:
                print("edit author: select the author instead of the document")
                return None
            else:
                AuthorIndex=KnownAuthorsList[selected]#gets the index in the 2D list
                insertAuthor=KnownAuthors[selected][0]#original author name
                insertDocs=KnownAuthors[selected][1]#original list of documents
        except:
            print("edit author: nothing selected")
            return None

    elif mode=="remove":#remove author does not open a window
        try:
            selected=int(authorList.curselection()[0])#this gets the listbox selection index
            if KnownAuthorsList[selected]==-1:
                print("remove author: select the author instead of the document")
                return None
            else:
                AuthorIndex=KnownAuthorsList[selected]#This gets the index in KnownAuthors nested list
                if AuthorIndex>=len(KnownAuthors)-1:
                    KnownAuthors=KnownAuthors[:AuthorIndex]
                else:
                    KnownAuthors=KnownAuthors[:AuthorIndex]+KnownAuthors[AuthorIndex+1:]
                authorsListUpdater(authorList)

        except:
            print("remove author: nothing selected")
            return None
        return None
    else:
        print("coding error: Author Add/Edit/Remove function 'authorsList' has an unknown mode parameter "+str(mode))
        assert mode=="add" or mode=="remove" or mode=="edit"
        return None

    AuthorWindow=Toplevel()
    AuthorWindow.grab_set()#Disables main window when the add/edit author window appears
    AuthorWindow.title(title)
    AuthorWindow.geometry("550x330")

    AuthorNameLabel=Label(AuthorWindow, text="Author", font="bold")
    AuthorNameLabel.grid(row=1, column=1, pady=7, sticky="NW")

    AuthorNameEntry=Entry(AuthorWindow, width=40)
    if mode=="edit":
        AuthorNameEntry.insert(END, insertAuthor)
    AuthorNameEntry.grid(row=1, column=2, pady=7, sticky="NW")

    AuthorListbox=Listbox(AuthorWindow, height=12, width=60)
    if mode=="edit":
        for j in insertDocs:
            AuthorListbox.insert(END, j)
    AuthorListbox.grid(row=2, column=2, sticky="NW")

    AuthorButtonsFrame=Frame(AuthorWindow)
    
    AuthorAddDocButton=Button(AuthorButtonsFrame, text="Add Document",\
        command=lambda:addFile("Add Document For Author", AuthorListbox, False, AuthorWindow))
    AuthorAddDocButton.grid(row=1, column=1)
    AuthorRmvDocButton=Button(AuthorButtonsFrame, text="Remove Document",\
        command=lambda:select_features(None, AuthorListbox, AuthorListbox.curselection(), 'remove'))
    AuthorRmvDocButton.grid(row=1, column=2)
    AuthorButtonsFrame.grid(row=3, column=2, sticky='NW')

    AuthorBottomButtonsFrame=Frame(AuthorWindow)
    #OK button functions differently depending on "add" or "edit".
    AuthorOKButton=Button(AuthorBottomButtonsFrame, text="OK")
    if mode=="add":
        AuthorOKButton.configure(command=lambda:authorSave(AuthorWindow, authorList, AuthorNameEntry.get(), AuthorListbox.get(0, END), mode))
    elif mode=="edit":
        AuthorOKButton.configure(command=lambda:authorSave(AuthorWindow, authorList, [insertAuthor, AuthorNameEntry.get()], AuthorListbox.get(0, END), mode))

    AuthorOKButton.grid(row=1, column=1, sticky="W")
    AuthorCancelButton=Button(AuthorBottomButtonsFrame, text="Cancel", command=lambda:AuthorWindow.destroy())
    AuthorCancelButton.grid(row=1, column=2, sticky="W")
    AuthorBottomButtonsFrame.grid(row=4, column=2, pady=7, sticky="NW")
    
    AuthorWindow.mainloop()
    return None


#ABOVE ARE ALL THE FUNCTIONS

#Test List for features
testfeatures=["first", "second", "third", "fourth", 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth']

menubar=Menu(topwindow)#adds top menu bar
filemenu=Menu(menubar, tearoff=0)

#tkinter menu building goes from bottom to top / leaves to root
BatchDocumentsMenu=Menu(filemenu, tearoff=0)#batch documents menu
BatchDocumentsMenu.add_command(label="Save Documents", command=todofunc)
BatchDocumentsMenu.add_command(label="Load Documents", command=todofunc)
filemenu.add_cascade(label="Batch Documents", menu=BatchDocumentsMenu, underline=0)

AAACProblemsMenu=Menu(filemenu, tearoff=0)#problems menu
AAACProblemsMenu.add_command(label="Problem 1", command=todofunc)
filemenu.add_cascade(label="AAAC Problems", menu=AAACProblemsMenu, underline=0)

filemenu.add_separator()#file menu
filemenu.add_command(label="Exit", command=topwindow.destroy)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu=Menu(menubar, tearoff=0)#help menu
helpmenu.add_command(label="About...", command=displayAbout)
menubar.add_cascade(label="Help", menu=helpmenu)

topwindow.config(menu=menubar)
#bottom of the main window is at the bottom of this file


#the middle workspace where the tabs are

workspace=Frame(topwindow, height=800, width=570)
workspace.pack(padx=20)

tabs=ttk.Notebook(workspace)
tabs.pack(pady=1, expand=True)

#size for all the main tabs.
tabheight=550
tabwidth=1000


#below is the tabs framework
Tab_Documents=Frame(tabs, height=tabheight, width=tabwidth)
#Tab_Documents.rowconfigure((1, 1), weight=1)
#Tab_Documents.columnconfigure((1, 1), weight=1)
Tab_Documents.pack(fill='both', expand=True)

Tab_Canonicizers=Frame(tabs, height=tabheight, width=tabwidth)
Tab_Canonicizers.pack(fill='both', expand=True)

Tab_EventDrivers=Frame(tabs, height=tabheight, width=tabwidth)
Tab_EventDrivers.pack(fill='both', expand=True)

Tab_EventCulling=Frame(tabs, height=tabheight, width=tabwidth)
Tab_EventCulling.pack(fill='both', expand=True)

Tab_AnalysisMethods=Frame(tabs, height=tabheight, width=tabwidth)
Tab_AnalysisMethods.pack(fill='both', expand=True)

Tab_ReviewProcess=Frame(tabs, height=tabheight, width=tabwidth)
Tab_ReviewProcess.pack(fill='both', expand=True)

tabs.add(Tab_Documents, text="Documents")
tabs.add(Tab_Canonicizers, text="Canonicizers")
tabs.add(Tab_EventDrivers, text="Event Drivers")
tabs.add(Tab_EventCulling, text="Event Culling")
tabs.add(Tab_AnalysisMethods, text="Analysis Methods")
tabs.add(Tab_ReviewProcess, text="Review & Process")
#above is the tabs framework


#BELOW ARE CONFIGS FOR EACH TAB

#Note: the review & process tab is set-up first instead of last.

#####REVIEW & PROCESS TAB
#basic frames structure

Tab_ReviewProcess_Canonicizers=Frame(Tab_ReviewProcess)
Tab_ReviewProcess_Canonicizers.grid(row=1, column=1, columnspan=3, sticky="NW")

Tab_ReviewProcess_EventDrivers=Frame(Tab_ReviewProcess)
Tab_ReviewProcess_EventDrivers.grid(row=2, column=1, sticky="NW")

Tab_ReviewProcess_EventCulling=Frame(Tab_ReviewProcess)
Tab_ReviewProcess_EventCulling.grid(row=2, column=2, sticky="NW")

Tab_ReviewProcess_AnalysisMethods=Frame(Tab_ReviewProcess)
Tab_ReviewProcess_AnalysisMethods.grid(row=2, column=3, sticky="NW")

#RP = ReviewProcess
listbox_width=37
listbox_height=12

#note: the buttons below (that redirect to corresponding tabs) have hard-coded tab numbers
Tab_RP_Canonicizers_Button=Button(Tab_ReviewProcess_Canonicizers, text="Canonicizers", font=("helvetica", 16), relief=FLAT,\
    command=lambda:switch_tabs(tabs, "choose", 1))
Tab_RP_Canonicizers_Button.grid(row=1, column=1, pady=(15, 4))

Tab_RP_Canonicizers_Listbox=Listbox(Tab_ReviewProcess_Canonicizers, width=listbox_width*3, height=listbox_height)
Tab_RP_Canonicizers_Listbox.grid(row=2, column=1, padx=27)



Tab_RP_EventDrivers_Button=Button(Tab_ReviewProcess_EventDrivers, text="Event Drivers", font=("helvetica", 16), relief=FLAT,\
    command=lambda:switch_tabs(tabs, "choose", 2))
Tab_RP_EventDrivers_Button.grid(row=1, column=1, pady=(15, 4))

Tab_RP_EventDrivers_Listbox=Listbox(Tab_ReviewProcess_EventDrivers, width=listbox_width, height=listbox_height)
Tab_RP_EventDrivers_Listbox.grid(row=2, column=1, padx=(15, 5))



Tab_RP_EventCulling_Button=Button(Tab_ReviewProcess_EventCulling, text="Event Culling", font=("helvetica", 16), relief=FLAT,\
    command=lambda:switch_tabs(tabs, "choose", 3))
Tab_RP_EventCulling_Button.grid(row=1, column=1, pady=(15, 4))

Tab_RP_EventCulling_Listbox=Listbox(Tab_ReviewProcess_EventCulling, width=listbox_width, height=listbox_height)
Tab_RP_EventCulling_Listbox.grid(row=2, column=1, padx=(5, 5))



Tab_RP_AnalysisMethods_Button=Button(Tab_ReviewProcess_AnalysisMethods, text="Analysis Methods", font=("helvetica", 16), relief=FLAT,\
    command=lambda:switch_tabs(tabs, "choose", 4))
Tab_RP_AnalysisMethods_Button.grid(row=1, column=1, pady=(15, 4))

Tab_RP_AnalysisMethods_Listbox=Listbox(Tab_ReviewProcess_AnalysisMethods, width=listbox_width, height=listbox_height)
Tab_RP_AnalysisMethods_Listbox.grid(row=2, column=1, padx=(5, 15))






###############DOCUMENTS TAB
Tab_Documents_Language_label=Label(Tab_Documents, text="Language", font=("helvetica", 15), anchor='nw')
Tab_Documents_Language_label.grid(row=1, column=1, sticky='NW')

#documents-language selection
analysisLanguage=StringVar()
analysisLanguage.set("English")
#may need a lookup function for the options below
analysisLanguageOptions=["Arabic (ISO-8859-6)", "Chinese (GB2123)", "English"]
Tab_Documents_language_dropdown=OptionMenu(Tab_Documents, analysisLanguage, *analysisLanguageOptions, )
Tab_Documents_language_dropdown['anchor']='nw'
Tab_Documents_language_dropdown.grid(row=2, column=1, sticky='NW')



#documents-unknown authors
Tab_Documents_UnknownAuthors_label=Label(Tab_Documents, text="Unknown Authors", font=("helvetica", 15), anchor='nw')
Tab_Documents_UnknownAuthors_label.grid(row=4, column=1, sticky="W")


Tab_Documents_UnknownAuthors_Frame=Frame(Tab_Documents)
Tab_Documents_UnknownAuthors_Frame.grid(row=5, column=1, sticky="W")


Tab_Documents_UnknownAuthors_listbox=Listbox(Tab_Documents_UnknownAuthors_Frame, width="100")
Tab_Documents_UnknownAuthors_listscrollbar=Scrollbar(Tab_Documents_UnknownAuthors_Frame)
#loop below: to be removed
for values in testfeatures[:5]:
    Tab_Documents_UnknownAuthors_listbox.insert(END, values)


Tab_Documents_UnknownAuthors_listbox.config(yscrollcommand=Tab_Documents_UnknownAuthors_listscrollbar.set)
Tab_Documents_UnknownAuthors_listscrollbar.config(command=Tab_Documents_UnknownAuthors_listbox.yview)


Tab_Documents_UnknownAuthors_listbox.pack(side=LEFT, fill=BOTH)
Tab_Documents_UnknownAuthors_listscrollbar.pack(side=RIGHT, fill=BOTH)

Tab_Documents_doc_buttons=Frame(Tab_Documents)
Tab_Documents_doc_buttons.grid(row=6, column=1, sticky="W")
Tab_Documents_UnknownAuthors_AddDoc_Button=Button(Tab_Documents_doc_buttons, text="Add Document", width="16", command=\
    lambda:addFile("Add a document to Unknown Authors", Tab_Documents_UnknownAuthors_listbox, False))
Tab_Documents_UnknownAuthors_RmvDoc_Button=Button(Tab_Documents_doc_buttons, text="Remove Document", width="16", command=\
    lambda:select_features(None, Tab_Documents_UnknownAuthors_listbox, Tab_Documents_UnknownAuthors_listbox.curselection(), "remove"))

Tab_Documents_UnknownAuthors_AddDoc_Button.grid(row=1, column=1, sticky="W")
Tab_Documents_UnknownAuthors_RmvDoc_Button.grid(row=1, column=2, sticky="W")

#documents-known authors
Tab_Documents_KnownAuthors_label=Label(Tab_Documents, text="Known Authors", font=("helvetica", 15), anchor='nw')
Tab_Documents_KnownAuthors_label.grid(row=7, column=1, sticky="W")


Tab_Documents_KnownAuthors_Frame=Frame(Tab_Documents)
Tab_Documents_KnownAuthors_Frame.grid(row=8, column=1, sticky="W")


Tab_Documents_KnownAuthors_listbox=Listbox(Tab_Documents_KnownAuthors_Frame, width="100")
Tab_Documents_KnownAuthors_listscroller=Scrollbar(Tab_Documents_KnownAuthors_Frame)

Tab_Documents_KnownAuthors_listbox.config(yscrollcommand=Tab_Documents_KnownAuthors_listscroller.set)
Tab_Documents_KnownAuthors_listscroller.config(command=Tab_Documents_KnownAuthors_listbox.yview)


Tab_Documents_KnownAuthors_listbox.pack(side=LEFT, fill=BOTH)
Tab_Documents_KnownAuthors_listscroller.pack(side=RIGHT, fill=BOTH)

#These are known authors
Tab_Documents_knownauth_buttons=Frame(Tab_Documents)
Tab_Documents_knownauth_buttons.grid(row=9, column=1, sticky="W")
Tab_Documents_KnownAuthors_AddAuth_Button=Button(Tab_Documents_knownauth_buttons, text="Add Author", width="15",\
    command=lambda:authorsList(Tab_Documents_KnownAuthors_listbox, 'add'))
Tab_Documents_KnownAuthors_EditAuth_Button=Button(Tab_Documents_knownauth_buttons, text="Edit Author", width="15",\
    command=lambda:authorsList(Tab_Documents_KnownAuthors_listbox, 'edit'))
Tab_Documents_KnownAuthors_RmvAuth_Button=Button(Tab_Documents_knownauth_buttons, text="Remove Author", width="15", command=\
    lambda:authorsList(Tab_Documents_KnownAuthors_listbox, "remove"))

Tab_Documents_KnownAuthors_AddAuth_Button.grid(row=1, column=1, sticky="W")
Tab_Documents_KnownAuthors_EditAuth_Button.grid(row=1, column=2, sticky="W")
Tab_Documents_KnownAuthors_RmvAuth_Button.grid(row=1, column=3, sticky="W")



#CANONICIZERS TAB
Tab_Canon_Frame=Frame(Tab_Canonicizers)
Tab_Canon_Frame.grid(row=1, column=1)

#the height of the top section (everything except the "description at bottom")
Tab_Canon_topsection_height="20"

#####available canonicizers
Tab_Canon_Available=Frame(Tab_Canon_Frame)
Tab_Canon_Available.grid(row=1, column=1)

Tab_Canon_Available_label=Label(Tab_Canon_Available, text="Canonicizers", font=("helvetica", 15), anchor='nw')
Tab_Canon_Available_label.grid(row=1, column=1, sticky="NW")
Tab_Canon_Available_listbox=Listbox(Tab_Canon_Available, width="30", height=Tab_Canon_topsection_height)
for values in testfeatures[:10]:
    Tab_Canon_Available_listbox.insert(END, values)
Tab_Canon_Available_listbox.grid(row=2, column=1)
#####


#####buttons to choose or remove canonicizers
Tab_Canon_Buttons=Frame(Tab_Canon_Frame)
Tab_Canon_Buttons.grid(row=1, column=2)

Tab_Canon_ButtonWidth="11"
CanonicizerFormat=StringVar()
CanonicizerFormat.set("All")
CanonicizerFormatOptions=["All", "Generic", "Doc", "PDF", "HTML"]
Tab_Canon_Buttons_formatMenu=OptionMenu(Tab_Canon_Buttons, CanonicizerFormat, *CanonicizerFormatOptions)
Tab_Canon_Buttons_formatMenu.grid(row=1, column=1, sticky="NW")

Tab_Canon_Buttons_add=Button(Tab_Canon_Buttons, width=Tab_Canon_ButtonWidth, text="Add", command=todofunc)
#first initialize the buttons. Since the "selected listbox is not initialized yet, can't use the select_features function."
#need to reconfigure later.
Tab_Canon_Buttons_add.grid(row=2, column=1, sticky="NW")

Tab_Canon_Buttons_remove=Button(Tab_Canon_Buttons, width=Tab_Canon_ButtonWidth, text="Remove", command=todofunc)
Tab_Canon_Buttons_remove.grid(row=3, column=1, sticky="NW")

Tab_Canon_Buttons_clear=Button(Tab_Canon_Buttons, width=Tab_Canon_ButtonWidth, text="Clear", command=todofunc)
Tab_Canon_Buttons_clear.grid(row=4, column=1, sticky="NW")
#####

#####selected canonicizers
Tab_Canon_Selected=Frame(Tab_Canon_Frame)
Tab_Canon_Selected.grid(row=1, column=3)

Tab_Canon_Selected_label=Label(Tab_Canon_Selected, text="Selected", font=("helvetica", 15), anchor='nw')
Tab_Canon_Selected_label.grid(row=1, column=1, sticky="W")
Tab_Canon_Selected_listbox=Listbox(Tab_Canon_Selected, width="45", height=Tab_Canon_topsection_height)
Tab_Canon_Selected_listbox.grid(row=2, column=1)

#reconfiguring the buttons after the seleted listboxes are initialized:
Tab_Canon_Buttons_add.configure(command=lambda:select_features(Tab_Canon_Available_listbox, [Tab_Canon_Selected_listbox, Tab_RP_Canonicizers_Listbox],\
    Tab_Canon_Available_listbox.curselection(), "add"))
Tab_Canon_Buttons_remove.configure(command=lambda:select_features(None, [Tab_Canon_Selected_listbox, Tab_RP_Canonicizers_Listbox],\
    Tab_Canon_Selected_listbox.curselection(), "remove"))
Tab_Canon_Buttons_clear.configure(command=lambda:select_features(None, [Tab_Canon_Selected_listbox, Tab_RP_Canonicizers_Listbox], None, "clear"))
#####

Tab_Canon_Description=Frame(Tab_Canonicizers)
Tab_Canon_Description.grid(row=2, column=1, sticky="NW")

Tab_Canon_DescriptionLabel=Label(Tab_Canon_Description, text="Description", font=("helvetica", 15), anchor='nw')
Tab_Canon_DescriptionLabel.grid(row=1, column=1, sticky="NW")
Tab_Canon_DescriptionText=Text(Tab_Canon_Description, height='6')
Tab_Canon_DescriptionText.grid(row=2, column=1, sticky="NW")


#EVENT DRIVERS

Tab_EventDrivers_topframe=Frame(Tab_EventDrivers)
Tab_EventDrivers_topframe.grid(row=1, column=1, sticky='nw')
#Available Event Drivers
Tab_EventDrivers_available=Frame(Tab_EventDrivers_topframe)
Tab_EventDrivers_available.grid(row=1, column=1)

Tab_EventDrivers_topframe_height="20"

Tab_EventDrivers_available_label=Label(Tab_EventDrivers_available, text="Event Drivers", font=("helvetica", 15), anchor='nw')
Tab_EventDrivers_available_label.grid(row=1, column=1, sticky="NW")
Tab_EventDrivers_available_listbox=Listbox(Tab_EventDrivers_available, width="30", height=Tab_EventDrivers_topframe_height)
for values in testfeatures[:10]:
    Tab_EventDrivers_available_listbox.insert(END, values)
Tab_EventDrivers_available_listbox.grid(row=2, column=1)
#####

#####buttons to choose or remove Event drivers
Tab_EventDrivers_Buttons=Frame(Tab_EventDrivers_topframe)
Tab_EventDrivers_Buttons.grid(row=1, column=2)

Tab_EventDrivers_buttonwidth="11"

Tab_EventDrivers_Buttons_add=Button(Tab_EventDrivers_Buttons, width=Tab_EventDrivers_buttonwidth, text="Add", command=todofunc)
Tab_EventDrivers_Buttons_add.grid(row=1, column=1, sticky="NW")

Tab_EventDrivers_Buttons_remove=Button(Tab_EventDrivers_Buttons, width=Tab_EventDrivers_buttonwidth, text="Remove", command=todofunc)
Tab_EventDrivers_Buttons_remove.grid(row=2, column=1, sticky="NW")

Tab_EventDrivers_Buttons_clear=Button(Tab_EventDrivers_Buttons, width=Tab_EventDrivers_buttonwidth, text="Clear", command=todofunc)
Tab_EventDrivers_Buttons_clear.grid(row=3, column=1, sticky="NW")
#####

#####selected event drivers
Tab_EventDrivers_Selected=Frame(Tab_EventDrivers_topframe)
Tab_EventDrivers_Selected.grid(row=1, column=3)

Tab_EventDrivers_Selected_label=Label(Tab_EventDrivers_Selected, text="Selected", font=("helvetica", 15), anchor='nw')
Tab_EventDrivers_Selected_label.grid(row=1, column=1, sticky="W")
Tab_EventDrivers_Selected_listbox=Listbox(Tab_EventDrivers_Selected, width="45", height=Tab_EventDrivers_topframe_height)
Tab_EventDrivers_Selected_listbox.grid(row=2, column=1)
#####

#reconfiguring buttons for event drivers
Tab_EventDrivers_Buttons_add.configure(command=\
    lambda:select_features(Tab_EventDrivers_available_listbox, [Tab_EventDrivers_Selected_listbox, Tab_RP_EventDrivers_Listbox], Tab_EventDrivers_available_listbox.curselection(), "add", Tab_RP_EventDrivers_Button))
Tab_EventDrivers_Buttons_clear.configure(command=\
    lambda:select_features(None, [Tab_EventDrivers_Selected_listbox, Tab_RP_EventDrivers_Listbox], None, "clear", Tab_RP_EventDrivers_Button))
Tab_EventDrivers_Buttons_remove.configure(command=\
    lambda:select_features(None, [Tab_EventDrivers_Selected_listbox, Tab_RP_EventDrivers_Listbox], Tab_EventDrivers_Selected_listbox.curselection(), "remove", Tab_RP_EventDrivers_Button))


#####parameters frame
Tab_EventDrivers_Parameters=Frame(Tab_EventDrivers_topframe)
Tab_EventDrivers_Parameters.grid(row=1, column=4)
Tab_EventDrivers_ParametersLabel=Label(Tab_EventDrivers_Parameters, text="Parameters", font=("helvetica", 15))
Tab_EventDrivers_ParametersLabel.grid(row=1, column=1, sticky="NW")
Tab_EventDrivers_Parameters_Dynamic=Frame(Tab_EventDrivers_Parameters)
##Tab_EventDrivers_Parameters_Dynamic.bind(<event>, <event handler>)
##bind events to frame to show parameters


#####descriptions frame
Tab_EventDrivers_Description=Frame(Tab_EventDrivers)
Tab_EventDrivers_Description.grid(row=2, column=1, columnspan=5, sticky="NW")

Tab_EventDrivers_DescriptionLabel=Label(Tab_EventDrivers_Description, text="Description", font=("helvetica", 15), anchor='nw')
Tab_EventDrivers_DescriptionLabel.grid(row=1, column=1, sticky="NW")
Tab_EventDrivers_DescriptionText=Text(Tab_EventDrivers_Description, height='6')
Tab_EventDrivers_DescriptionText.grid(row=2, column=1, sticky="NW")







#####EVENT CULLING FRAME
#EVENT CULLING

Tab_EventCulling_topframe=Frame(Tab_EventCulling)
Tab_EventCulling_topframe.grid(row=1, column=1, sticky='nw')
#Available Event Culling
Tab_EventCulling_available=Frame(Tab_EventCulling_topframe)
Tab_EventCulling_available.grid(row=1, column=1)

Tab_EventCulling_topframe_height="20"

Tab_EventCulling_available_label=Label(Tab_EventCulling_available, text="Event Culling", font=("helvetica", 15), anchor='nw')
Tab_EventCulling_available_label.grid(row=1, column=1, sticky="NW")
Tab_EventCulling_available_listbox=Listbox(Tab_EventCulling_available, width="30", height=Tab_EventCulling_topframe_height)
for values in testfeatures[:10]:
    Tab_EventCulling_available_listbox.insert(END, values)
Tab_EventCulling_available_listbox.grid(row=2, column=1)
#####

#####buttons to choose or remove Event culling
Tab_EventCulling_Buttons=Frame(Tab_EventCulling_topframe)
Tab_EventCulling_Buttons.grid(row=1, column=2)

Tab_EventCulling_buttonwidth="11"

Tab_EventCulling_Buttons_add=Button(Tab_EventCulling_Buttons, width=Tab_EventCulling_buttonwidth, text="Add", command=todofunc)
Tab_EventCulling_Buttons_add.grid(row=1, column=1, sticky="NW")

Tab_EventCulling_Buttons_remove=Button(Tab_EventCulling_Buttons, width=Tab_EventCulling_buttonwidth, text="Remove", command=todofunc)
Tab_EventCulling_Buttons_remove.grid(row=2, column=1, sticky="NW")

Tab_EventCulling_Buttons_clear=Button(Tab_EventCulling_Buttons, width=Tab_EventCulling_buttonwidth, text="Clear", command=todofunc)
Tab_EventCulling_Buttons_clear.grid(row=3, column=1, sticky="NW")
#####

#####selected event culling
Tab_EventCulling_Selected=Frame(Tab_EventCulling_topframe)
Tab_EventCulling_Selected.grid(row=1, column=3)

Tab_EventCulling_Selected_label=Label(Tab_EventCulling_Selected, text="Selected", font=("helvetica", 15), anchor='nw')
Tab_EventCulling_Selected_label.grid(row=1, column=1, sticky="W")
Tab_EventCulling_Selected_listbox=Listbox(Tab_EventCulling_Selected, width="45", height=Tab_EventCulling_topframe_height)

Tab_EventCulling_Selected_listbox.grid(row=2, column=1)
#####

#reconfiguring buttons for event culling
Tab_EventCulling_Buttons_add.configure(command=\
    lambda:select_features(Tab_EventCulling_available_listbox, [Tab_EventCulling_Selected_listbox, Tab_RP_EventCulling_Listbox], Tab_EventCulling_available_listbox.curselection(), "add"))
Tab_EventCulling_Buttons_clear.configure(command=\
    lambda:select_features(None, [Tab_EventCulling_Selected_listbox, Tab_RP_EventCulling_Listbox], None, "clear"))
Tab_EventCulling_Buttons_remove.configure(command=\
    lambda:select_features(None, [Tab_EventCulling_Selected_listbox, Tab_RP_EventCulling_Listbox], Tab_EventCulling_Selected_listbox.curselection(), "remove"))


#####parameters frame
Tab_EventCulling_Parameters=Frame(Tab_EventCulling_topframe)
Tab_EventCulling_Parameters.grid(row=1, column=4)
Tab_EventCulling_ParametersLabel=Label(Tab_EventCulling_Parameters, text="Parameters", font=("helvetica", 15))
Tab_EventCulling_ParametersLabel.grid(row=1, column=1, sticky="NW")
Tab_EventCulling_Parameters_Dynamic=Frame(Tab_EventCulling_Parameters)
##Tab_EventCulling_Parameters_Dynamic.bind(<event>, <event handler>)
##bind events to frame to show parameters


#####descriptions frame
Tab_EventCulling_Description=Frame(Tab_EventCulling_topframe)
Tab_EventCulling_Description.grid(row=2, column=1, columnspan=5, sticky="NW")

Tab_EventCulling_DescriptionLabel=Label(Tab_EventCulling_Description, text="Description", font=("helvetica", 15), anchor='nw')
Tab_EventCulling_DescriptionLabel.grid(row=1, column=1, sticky="NW")
Tab_EventCulling_DescriptionText=Text(Tab_EventCulling_Description, height='6')
Tab_EventCulling_DescriptionText.grid(row=2, column=1, sticky="NW")





#ABOVE ARE THE CONFIGS FOR EACH TAB

bottomframe=Frame(topwindow, height=150, width=570)
bottomframe.pack()

FinishButton=Button(bottomframe, text="Finish & Review", command=lambda:switch_tabs(tabs, "choose", 5))#note: this button has a hard-coded tab number
NextButton=Button(bottomframe, text="Next ->", command=lambda:switch_tabs(tabs, "next"))

FinishButton.pack(side=RIGHT)
NextButton.pack(side=RIGHT)

Notes_Button=Button(bottomframe, text="Notes", command=notepad)
Notes_Button.pack(side=RIGHT)


#starts app
topwindow.mainloop()
