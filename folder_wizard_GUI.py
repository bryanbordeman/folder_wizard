'''==========================================
Title:  folder_wizard_GUI.py
Author:  Bryan Bordeman
Start Date:  062219
Updated:  091519
Version:  v2.0

;=========================================='''

from win32api import GetSystemMetrics
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkcalendar import DateEntry
from quote_codes import category
from project_attribute_list import*
from zip_2_state import find_state
from zip_2_state import country_str
import time
from folder_wizard import*
from tkinter import filedialog

version = 'v2.0'
opportunity = ''
project =''


class CreateToolTip(object):
    ''' create popup for zip options'''

    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background='white', relief='solid', borderwidth=1,
                      font=("times", "8", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


class WizardTitle:
    def __init__(self, master):
        self.master = master
        master.title(f"GPS Folder Wizard  ({version})")
        style = ttk.Style()
        style.theme_use('winnative')

        # Welcome message-------------------------------------------
        self.welcome_frame = Frame()
        self.welcome_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        welcome_message = 'Welcome to GPS Folder Wizard\n\nThis program is designed to automate folder creation as well as update all applicable logs.\nAll data generated in this Wizard will be archived for future queries.\n\n\nSelect folder type and click NEXT to continue, or CANCEL to exit Wizard'
        Label(self.welcome_frame, text=welcome_message).pack(side=LEFT)

        # ---------------------------------------------------------

        self.notes_frame = Frame()
        self.notes_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        Label(self.notes_frame, text=f'Author: Bryan Bordeman\nCreated: 2019\nVersion: {version}').pack(side=LEFT)

        # Select radio buttons-------------------------------------
        self.radio_frame = Frame()
        self.radio_frame.pack(fill=BOTH, anchor=W, padx=10, pady=20)
        Label(self.radio_frame, text="Select Folder type     ").pack(side=LEFT)
        self.v = IntVar()
        self.r_button_opp = Radiobutton(self.radio_frame, text='Opportunity     ', variable=self.v, value=1).pack(side=LEFT)
        self.r_button_prj = Radiobutton(self.radio_frame, text='Project', variable=self.v, value=2).pack(side=LEFT)

        # control buttons  ----------------------------------------
        self.next_frame = Frame()
        self.next_frame.pack(fill=BOTH, side=BOTTOM, anchor=W, padx=10, pady=10)
        self.next = Button(self.next_frame, width=15, text="Next >", command=self.next)
        self.next.pack(side=RIGHT, padx=5, pady=20)
        self.cancel = Button(self.next_frame, width=15, text="Cancel", command=self.cancel)
        self.cancel.pack(side=RIGHT, padx=5, pady=20)

    def next(self):
        '''creates window based on selection of folder type'''
        if self.v.get() == 1:  # create opportunity window
            self.welcome_frame.pack_forget()
            self.radio_frame.pack_forget()
            self.next_frame.pack_forget()
            self.notes_frame.pack_forget()
            opportunity = WizardOpportunity(root)
        elif self.v.get() == 2:  # create project window
            self.welcome_frame.pack_forget()
            self.radio_frame.pack_forget()
            self.next_frame.pack_forget()
            self.notes_frame.pack_forget()
            project = WizardProject(root)
        else:
            pass  # nothing is selected

    def cancel(self):
        root.quit()


class WizardOpportunity:
    def __init__(self, master):
        self.master = master
        master.title(f"GPS Folder Wizard (Opportunity)  ({version})")
        style = ttk.Style()
        style.theme_use('winnative')

        self.idx = float(0)  # keeps tabs on customer list
        self.inquiry_date = time.strftime("%D")

        # project name input ------------------------------------
        self.project_name_frame = Frame()
        self.project_name_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        self.project_name_label = Label(self.project_name_frame, text="Project Name       ").pack(side=LEFT)
        self.project_name_var = StringVar()
        vcmde = self.project_name_frame.register(self.validate_entry)


        self.project_name_entry = Entry(self.project_name_frame, width=70,
                                        textvariable=self.project_name_var, validate="key", validatecommand=(vcmde, '%P'))

        self.project_name_entry.pack(side=LEFT)

        # project category input (dynamic optionmenu)------------
        self.dict = category

        self.project_category_frame = Frame()
        self.project_category_frame.pack(fill=BOTH, anchor=W, padx=10, pady=5)
        self.project_category_label = Label(self.project_category_frame, text="Project Category  ").pack(side=LEFT)

        self.category_var = StringVar()
        self.type_var = StringVar()

        # OptionMenu to select project category
        self.project_category = OptionMenu(self.project_category_frame, self.category_var, 'MRI', *self.dict.keys())

        # OptionMenu to select project type
        self.project_type = OptionMenu(self.project_category_frame, self.type_var, '')

        self.category_var.trace('w', self.update_options)

        self.category_var.set('MRI')

        self.project_category.pack(side=LEFT)

        self.project_type_label = Label(self.project_category_frame, text="   Project Type  ").pack(side=LEFT)
        self.project_type.pack(side=LEFT)

        # project zip input ------------------------------------
        self.project_zip_frame = Frame()
        self.project_zip_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        self.project_zip_label = Label(self.project_zip_frame, text="Project ZIP*           ").pack(side=LEFT)
        self.project_zip_var = StringVar()
        self.project_zip_var.set('0')
        vcmd = self.project_zip_frame.register(self.validate)
        self.project_zip_entry = Entry(self.project_zip_frame, textvariable=self.project_zip_var, width=6, validate="key", validatecommand=(vcmd, '%P'))
        self.project_zip_entry.pack(side=LEFT)

        self.country_hover = CreateToolTip(self.project_zip_entry, country_str)

        # Manager ---------------------------------------------

        Label(self.project_zip_frame, text="  Manager   ").pack(side=LEFT)
        self.manager_var = StringVar()
        self.manager_list = list(manager.keys())
        self.manager = OptionMenu(self.project_zip_frame, self.manager_var, self.manager_list[0], *self.manager_list)
        self.manager.pack(side=LEFT)

        # customer input --------------------------------------
        self.customer_frame = Frame()
        self.customer_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        self.customer_label = Label(self.customer_frame, text="Customer(s)         ").pack(side=LEFT)
        self.customer_var = StringVar()
        self.customer_entry = Entry(self.customer_frame, width=46, textvariable=self.customer_var).pack(side=LEFT)
        self.customer_list = []

        # customer add button ----------------------------------
        self.undo = Button(self.customer_frame, width=9, text="  Undo  ", command=self.undo)
        self.undo.pack(side=LEFT, padx=5)

        self.add = Button(self.customer_frame, width=9, text="   Add   ", command=self.add)
        self.add.pack(side=LEFT, padx=5)

        # customer output display ----------------------------------

        self.label_frame_customer = LabelFrame(master, text="Customer List")
        self.label_frame_customer.pack(anchor=W, padx=10)

        self.customer_output_frame = Frame(self.label_frame_customer)
        self.customer_output_frame.pack(fill=BOTH, anchor=W)

        self.customer_output = Text(self.customer_output_frame, background='white', border=2, height=6)
        self.customer_output.pack(side=LEFT)

        # Bid Due  ------------------------------------------------
        self.bid_frame = Frame()
        self.bid_frame.pack(fill=BOTH, side=BOTTOM, anchor=W, padx=10, pady=30)
        self.bid_label = Label(self.bid_frame, text="Bid Due Date       ").pack(side=LEFT)
        self.bid_var = StringVar()
        self.bid_entry = DateEntry(self.bid_frame, width=12, textvariable=self.bid_var, background='darkblue', foreground='white', borderwidth=2)
        self.bid_entry.pack(side=LEFT)
        # control buttons  ----------------------------------------

        # Submit takes inputs and commits them to the program
        self.create = Button(self.bid_frame, width=9, text="   Create   ", command=self.create)
        self.create.pack(side=RIGHT, padx=5)

        # clears all inputs
        self.clear = Button(self.bid_frame, width=9, text="   Clear   ", command=self.clear)
        self.clear.pack(side=RIGHT, padx=5)

        # back button (takes you back to title frame)
        self.back = Button(self.bid_frame, width=9, text=" < Back   ", command=self.back)
        self.back.pack(side=RIGHT, padx=5)

        #----------------------------------------------------------

    def update_options(self, *args):
        '''Updates project type based on project category selection'''
        self.categories = [i[0] for i in self.dict[self.category_var.get()]]  # makes list based on what category is picked
        self.type_var.set(self.categories[0])  # sets project type to first in list

        menu = self.project_type['menu']
        menu.delete(0, 'end')

        for category in self.categories:
            menu.add_command(label=category, command=lambda category=category: self.type_var.set(category))
        # --------------------------------------------------------------

    def validate(self, new_text):
        '''validate characters are integers used for zip entry'''
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True
        if len(new_text) > 5: #limit char. to 5 max
            return False

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

        # --------------------------------------------------------------
        # limit char. on entry to max 27

    def validate_entry(self, new_text):
        '''validate max number of characters in entry field'''
        if len(new_text) > 27:  # the field is being cleared
            self.entered_text = ''
            return False

        try:
            self.entered_text = str(new_text)
            return True
        except ValueError:
            return False
        # --------------------------------------------------------------

    def add(self):
        self.customer_list.append(self.customer_var.get())
        self.customer_output.insert(END, self.customer_var.get() + '\n')
        self.customer_var.set('')
        self.idx += 1
        # print(self.customer_list) # for testing only
        # --------------------------------------------------------------

    def undo(self):
        if len(self.customer_list) > 0:
            self.customer_list.pop()
            self.customer_output.delete(self.idx, END)
            self.idx -= 1
            # print(self.customer_list) # for testing only
        # --------------------------------------------------------------

    def create(self):
        global opportunity
        # print(self.project_name_var.get())
        # print(self.project_zip_var.get())
        # print(find_state(int(self.project_zip_var.get())))  # get state code
        # print(self.customer_list)
        # print(self.bid_var.get())
        # print(self.inquiry_date)
        self.type_code = category[self.category_var.get()][self.categories.index(self.type_var.get())][1]  # need to create code
        # print(self.category_var.get())
        # print(self.type_var.get())
        # print(self.type_code)

        try:
            opportunity = Opportunity(self.project_name_var.get(), self.category_var.get(), self.type_var.get(), self.type_code, self.project_zip_var.get(), self.customer_list, self.bid_var.get(), manager[self.manager_var.get()])

            # erase frames---------------------
            self.project_name_frame.pack_forget()
            self.project_category_frame.pack_forget()
            self.project_zip_frame.pack_forget()
            self.customer_frame.pack_forget()
            self.label_frame_customer.pack_forget()
            self.customer_output_frame.pack_forget()
            self.bid_frame.pack_forget()
            confirmation = WizardConfirmation(root, 'opportunity')
        except PermissionError:
            error_message = 'Error: Creating quote number. "Master Quote Log.xlsx" is open by another user'
            top_width = app_width
            top_height = 100
            top = Toplevel()
            top.title("Error 001")
            top.geometry(f'{top_width}x{top_height}+{int((screen_width - app_width)/2)}+{int((screen_height - app_height)/2)}')

            msg = Message(top, text=error_message, width=f'{top_width}', pady=20)
            msg.pack()

            button = Button(top, text="Dismiss", command=top.destroy)
            button.pack()
        except FileNotFoundError:
            error_message = 'Error: Creating quote number. Please make sure "Master Quote Log.xlsx" is placed in directory'
            top_width = app_width
            top_height = 100
            top = Toplevel()
            top.title("Error 002")
            top.geometry(f'{top_width}x{top_height}+{int((screen_width - app_width)/2)}+{int((screen_height - app_height)/2)}')

            msg = Message(top, text=error_message, width=f'{top_width}', pady=20)
            msg.pack()

            button = Button(top, text="Dismiss", command=top.destroy)
            button.pack()

        # root.quit()

    def back(self):
        self.project_name_frame.pack_forget()
        self.project_category_frame.pack_forget()
        self.project_zip_frame.pack_forget()
        self.customer_frame.pack_forget()
        self.label_frame_customer.pack_forget()
        self.customer_output_frame.pack_forget()
        self.bid_frame.pack_forget()
        title = WizardTitle(root)

    def clear(self):
        self.project_name_var.set('')
        self.project_zip_var.set('')
        self.customer_list = []
        self.bid_var.set('')
        self.customer_output.delete('1.0', END)


class WizardProject:
    def __init__(self, master):
        self.master = master
        master.title(f"GPS Folder Wizard (Project)  ({version})")
        style = ttk.Style()
        style.theme_use('winnative')

        self.labor_code_list = []
        self.opportunity = ''

        # select opportunity ------------------------------------
        self.opp_sel_frame = Frame()
        self.opp_sel_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        Label(self.opp_sel_frame, text="Opportunity         ").pack(side=LEFT)
        self.opp_dir = Text(self.opp_sel_frame, width=50, background='white', border=2, height=1)
        self.opp_dir.pack(side=LEFT)
        self.dir_button = Button(self.opp_sel_frame, width=3, text='...', command=self.browse)
        self.dir_button.pack(side=LEFT)

        # self.opp_sel_var = StringVar()
        # self.opp_list = ['Q19-001', 'Q19-002', 'Q19-003', 'Q19-004']
        # self.opp_sel = OptionMenu(self.opp_sel_frame, self.opp_sel_var, 'Opportunity', *self.opp_list)
        # self.opp_sel.pack(side=LEFT)

        self.or_frame = Frame()
        self.or_frame.pack(fill=BOTH, anchor=W, padx=10)
        Label(self.or_frame, text="If Opportunity folder selected was created in this Wizard some of the input fields below will\npopulate automatically. ").pack(side=LEFT)

        # Notes: Need to think about what to do when list gets super large

        # project name input ------------------------------------
        self.project_name_frame = Frame()
        self.project_name_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        self.project_name_label = Label(self.project_name_frame, text="Project Name       ").pack(side=LEFT)
        self.project_name_var = StringVar()
        vcmde = self.project_name_frame.register(self.validate_entry)

        self.project_name_entry = Entry(self.project_name_frame, width=70,
                                        textvariable=self.project_name_var, validate="key", validatecommand=(vcmde, '%P'))

        self.project_name_entry.pack(side=LEFT)

        # project category input (dynamic optionmenu)------------
        self.dict = category

        self.project_category_frame = Frame()
        self.project_category_frame.pack(fill=BOTH, anchor=W, padx=10, pady=5)
        self.project_category_label = Label(self.project_category_frame, text="Project Category  ").pack(side=LEFT)

        self.category_var = StringVar()
        self.type_var = StringVar()

        # OptionMenu to select project category
        self.project_category = OptionMenu(self.project_category_frame, self.category_var, 'MRI', *self.dict.keys())

        # OptionMenu to select project type
        self.project_type = OptionMenu(self.project_category_frame, self.type_var, '')

        self.category_var.trace('w', self.update_options)

        self.category_var.set('MRI')

        self.project_category.pack(side=LEFT)

        self.project_type_label = Label(self.project_category_frame, text="   Project Type  ").pack(side=LEFT)
        self.project_type.pack(side=LEFT)

        # project zip input ------------------------------------
        self.project_zip_frame = Frame()
        self.project_zip_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        self.project_zip_label = Label(self.project_zip_frame, text="Project ZIP*           ").pack(side=LEFT)
        self.project_zip_var = StringVar()
        self.project_zip_var.set('0')
        vcmd = self.project_zip_frame.register(self.validate)
        self.project_zip_entry = Entry(self.project_zip_frame, textvariable=self.project_zip_var, width=6, validate="key", validatecommand=(vcmd, '%P'))
        self.project_zip_entry.pack(side=LEFT)

        self.country_hover = CreateToolTip(self.project_zip_entry, country_str)

        # project terms---------------------------------------------
        # self.terms_frame = Frame()
        # self.terms_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        Label(self.project_zip_frame, text="  Project Terms   ").pack(side=LEFT)
        self.terms_var = StringVar()
        self.terms_list = terms_list
        self.terms = OptionMenu(self.project_zip_frame, self.terms_var, self.terms_list[0], *self.terms_list)
        self.terms.pack(side=LEFT)

        # customer input --------------------------------------
        self.customer_frame = Frame()
        self.customer_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        self.customer_label = Label(self.customer_frame, text="Customer             ").pack(side=LEFT)
        self.customer_var = StringVar()

        self.customer_entry = Entry(self.customer_frame, width=66, textvariable=self.customer_var)
        self.customer_entry.pack(side=LEFT)

        # Billing--------------------------------------------
        self.billing_frame = Frame()
        self.billing_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        Label(self.billing_frame, text="Billing Type          ").pack(side=LEFT)
        self.billing_var = StringVar()
        self.billing_list = list(billing_dict.keys())
        self.billing = OptionMenu(self.billing_frame, self.billing_var, self.billing_list[0], *self.billing_list)
        self.billing.pack(side=LEFT)

        # Order type ---------------------------------------------

        Label(self.billing_frame, text="  Order Type   ").pack(side=LEFT)
        self.order_var = StringVar()
        self.order_list = order_type
        self.order = OptionMenu(self.billing_frame, self.order_var, self.order_list[0], *self.order_list)
        self.order.pack(side=LEFT)

        # Select radio buttons-------------------------------------
        Label(self.billing_frame, text="   Tax Exempt   ").pack(side=LEFT)
        self.tax = IntVar()
        self.r_button_tax_yes = Radiobutton(self.billing_frame, text='Yes  ', variable=self.tax, value=True).pack(side=LEFT)
        self.r_button_tax_no = Radiobutton(self.billing_frame, text='No  ', variable=self.tax, value=False).pack(side=LEFT)

        # Labor--------------------------------------------------
        self.labor_frame = Frame()
        self.labor_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        Label(self.labor_frame, text="Labor Type           ").pack(side=LEFT)
        self.labor_var = StringVar()
        self.labor_list = list(labor_dict.keys())
        self.labor = OptionMenu(self.labor_frame, self.labor_var, self.labor_list[0], *self.labor_list)
        self.labor.pack(side=LEFT)

        self.undo = Button(self.labor_frame, width=5, text="Undo", command=self.undo)
        self.undo.pack(side=LEFT, padx=5)

        self.add = Button(self.labor_frame, width=5, text="Add", command=self.add)
        self.add.pack(side=LEFT, padx=5)

        self.labor_text = Text(self.labor_frame, width=20, background='white', border=2, height=1)
        self.labor_text.pack()

        # control buttons  ----------------------------------------

        self.control_frame = Frame()
        self.control_frame.pack(fill=BOTH, side=BOTTOM, anchor=W, padx=10, pady=10)

        # project price
        self.price_label = Label(self.control_frame, text="Sell Price (USD)    ").pack(side=LEFT)
        self.price_var = StringVar()
        self.price_entry = Entry(self.control_frame, width=12, textvariable=self.price_var, validate="key", validatecommand=(vcmd, '%P')).pack(side=LEFT)

        # Submit takes inputs and commits them to the program
        self.create = Button(self.control_frame, width=9, text="   Create   ", command=self.create)
        self.create.pack(side=RIGHT, padx=5)

        # clears all inputs
        self.clear = Button(self.control_frame, width=9, text="   Clear   ", command=self.clear)
        self.clear.pack(side=RIGHT, padx=5)

        # back button (takes you back to title frame)
        self.back = Button(self.control_frame, width=9, text=" < Back   ", command=self.back)
        self.back.pack(side=RIGHT, padx=5)

        #----------------------------------------------------------

    def update_options(self, *args):
        '''Updates project type based on project category selection'''
        self.categories = [i[0] for i in self.dict[self.category_var.get()]]  # makes list based on what category is picked
        self.type_var.set(self.categories[0])  # sets project type to first in list

        menu = self.project_type['menu']
        menu.delete(0, 'end')

        for category in self.categories:
            menu.add_command(label=category, command=lambda category=category: self.type_var.set(category))

        if self.category_var.get() == 'GPS Specialty Doors':
            self.order_var.set(self.order_list[-1])  # set to GPS
        # --------------------------------------------------------------

    def validate(self, new_text):
        '''validate characters are integers used for zip entry'''
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True
        if len(new_text) > 5:  # limit char. to 5 max
            return False

        try:
            self.entered_number = float(new_text)
            return True
        except ValueError:
            return False

       # --------------------------------------------------------------
        # limit char. on entry to max 27

    def validate_entry(self, new_text):
        '''validate max number of characters in entry field'''
        if len(new_text) > 27:  # the field is being cleared
            self.entered_text = ''
            return False

        try:
            self.entered_text = str(new_text)
            return True
        except ValueError:
            return False
         # --------------------------------------------------------------

    def browse(self):
        ''' select opportunity to import into project'''
        dir = StringVar()
        dir.set(filedialog.askdirectory())
        self.opportunity = (str(dir.get()).split('/')[-1])[:7]  # take end of directory

        # Unpack pickle data -----------------------------------------
        quote_data = 'opportunity.pkl'
        if os.path.exists(quote_data):
            with open(quote_data, 'rb') as rfp:
                quote_obj = pickle.load(rfp)

        try:
            # check 1 = see if string starts with "Q"
            # Check 2 = see if "-" is at index [3]
            # **** need to add third check for opportunity[4:7] to confirm it is int.****
            if self.opportunity[0] == 'Q' and self.opportunity[3] == '-':
                self.opp_dir.delete('1.0', END)
                self.opp_dir.insert('1.0', (str(dir.get()).split('/')[-1]))
                # If quote is in pickled data import information

                # Look up will be as follows:
                # quote_obj[quote_number][index]
                # index 0 = project_name
                # index 1 = project_category
                # index 2 = project_type
                # index 3 = type_code
                # index 4 = project_zip
                # index 5 = customer_list
                # index 6 = bid_due]

                if list(quote_obj.keys()).count(self.opportunity) > 0:
                    self.project_name_var.set(quote_obj[self.opportunity][0])
                    self.category_var.set(quote_obj[self.opportunity][1])
                    self.type_var.set(quote_obj[self.opportunity][2])
                    self.project_zip_var.set(quote_obj[self.opportunity][4])
                    #**** Need to figure out how to update OptionMenu with customer list??******
                    #
                    self.customer_var.set(list(quote_obj[self.opportunity][5])[0])

                    # menu = self.customer_button['menu']
                    # menu.delete(0, 'end')

                    # Get Customer list from README.txt ------------------------
                    try:
                        name_of_file = 'README'
                        path = dir.get()
                        completeName = os.path.join(path, name_of_file + ".txt")
                        readme = open(completeName, "r")
                        customer_str = readme.read().split('[')[-1].strip(']')
                        customer_list = [i.strip("'") for i in customer_str.split(', ')]
                    except UnboundLocalError:
                        customer_list = quote_obj[self.opportunity][5]
                    except FileNotFoundError:
                        customer_list = quote_obj[self.opportunity][5]
                    # ----------------------------------------------------------
                    # create dropdown to select customer from opp. customer list

                    self.customer_button = OptionMenu(self.customer_frame, self.customer_var, customer_list[0], *customer_list)
                    self.customer_button.pack(side=LEFT)

                else:
                    # erase enrty if project was selected and then different project is selected after
                    self.project_name_var.set('')
                    self.project_zip_var.set('')
                    self.customer_var.set('')
                    # need to add pack_forget for customer_button

            else:
                self.opp_dir.delete('1.0', END)
                return self.opp_dir.insert('1.0', 'Invalid Opportunity selection')
        except IndexError:
            pass

        # **** Need to put auto fill code for project data maybe at method to call in above try statement??****

    def pick_customer(self):
        '''when opportunity is picked select customer from list'''
        pass

    def undo(self):
        '''takes labor code off list or better string??'''
        self.labor_text.delete('1.0', END)
        if len(self.labor_code_list) > 0:
            self.labor_code_list.pop()
            self.labor_text.insert('1.0', self.labor_code_list)

    def add(self):
        '''adds labor code to list '''
        # check to make sure no duplicates in list
        if self.labor_code_list.count(labor_dict[self.labor_var.get()]) == 0:
            self.labor_text.delete('1.0', END)
            self.labor_code_list.append(labor_dict[self.labor_var.get()])
            self.labor_text.insert('1.0', self.labor_code_list)
        # --------------------------------------------------------------

    def create(self):
        global project
        # print(self.project_name_var.get())
        # print(self.project_zip_var.get())
        # print(find_state(int(self.project_zip_var.get())))  # get state code
        # print(self.customer_var.get())
        # print(self.category_var.get())
        # print(self.type_var.get())
        # print(self.type_code)
        # print(self.labor_code)
        # print(self.opportunity)

        self.labor_code = str(",".join(self.labor_code_list))  # make labor list into string var

        self.type_code = category[self.category_var.get()][self.categories.index(self.type_var.get())][1]  # need to create code

        try:
            project = Project(self.project_name_var.get(), self.category_var.get(), self.type_var.get(), self.type_code, self.project_zip_var.get(), self.customer_var.get(), self.opportunity, self.terms_var.get(), self.tax.get(), billing_dict[self.billing_var.get()], self.labor_code, self.order_var.get(), self.price_var.get())

            # erase frames---------------------
            self.opp_sel_frame.pack_forget()
            self.or_frame.pack_forget()
            self.project_name_frame.pack_forget()
            self.project_category_frame.pack_forget()
            self.project_zip_frame.pack_forget()
            self.customer_frame.pack_forget()
            # self.terms_frame.pack_forget()
            self.billing_frame.pack_forget()
            self.labor_frame.pack_forget()
            self.control_frame.pack_forget()
            confirmation = WizardConfirmation(root, 'project')

        except PermissionError:
            error_message = 'Error: Creating quote number. "Global Job List-start-complete dates 2016.xlsx" is open by another user'
            top_width = app_width
            top_height = 100
            top = Toplevel()
            top.title("Error 003")
            top.geometry(f'{top_width}x{top_height}+{int((screen_width - app_width)/2)}+{int((screen_height - app_height)/2)}')

            msg = Message(top, text=error_message, width=f'{top_width}', pady=20)
            msg.pack()

            button = Button(top, text="Dismiss", command=top.destroy)
            button.pack()

        except FileNotFoundError:
            error_message = 'Error: Creating project number. Please make sure "Global Job List-start-complete dates 2016.xlsx"\nis placed in directory'
            top_width = app_width
            top_height = 100
            top = Toplevel()
            top.title("Error 004")
            top.geometry(f'{top_width}x{top_height}+{int((screen_width - app_width)/2)}+{int((screen_height - app_height)/2)}')

            msg = Message(top, text=error_message, width=f'{top_width}', pady=20)
            msg.pack()

            button = Button(top, text="Dismiss", command=top.destroy)
            button.pack()

    def back(self):
        self.opp_sel_frame.pack_forget()
        self.or_frame.pack_forget()
        self.project_name_frame.pack_forget()
        self.project_category_frame.pack_forget()
        self.project_zip_frame.pack_forget()
        self.customer_frame.pack_forget()
        # self.terms_frame.pack_forget()
        self.billing_frame.pack_forget()
        self.labor_frame.pack_forget()
        self.control_frame.pack_forget()
        title = WizardTitle(root)

    def clear(self):
        self.opp_dir.delete('1.0', 'end')
        self.project_name_var.set('')
        self.project_zip_var.set('')
        self.customer_var.set('')
        menu = self.customer_button['menu']
        menu.delete(0, 'end')

        self.labor_text.delete('1.0', END)
        self.labor_code_list = []

        # self.opp_sel_var.set('Opportunity')


class WizardConfirmation:
    def __init__(self, master, folder_type):
        self.master = master
        self.folder_type = folder_type
        master.title(f"GPS Folder Wizard  ({version})")
        style = ttk.Style()
        style.theme_use('winnative')

        app_width = 400
        app_height = 150
        root.geometry(f'{app_width}x{app_height}+{int((screen_width - app_width)/2)}+{int((screen_height - app_height)/2)}')

       # message-------------------------------------------
        self.message_frame = Frame()
        self.message_frame.pack(fill=BOTH, anchor=W, padx=10, pady=5)

        if folder_type == 'opportunity':
            message = f'{opportunity}\n\nFolder was successfully created!!'
            Label(self.message_frame, text=message).pack(side=LEFT)

            # below is for testing only
            # print(opportunity.quote_number)
            # print(opportunity.project_name)
            # print(opportunity.project_type)
            # print(opportunity.project_zip)
            # print(opportunity.customer_list)
            # print(opportunity.bid_due)
        else:
            message = f'{project}\n\nFolder was successfully created!!'
            Label(self.message_frame, text=message).pack(side=LEFT)

            # below is for testing only
            # print(project.project_number)
            # print(project.project_name)
            # print(project.project_type)
            # print(project.project_zip)
            # print(project.customer)
            # print(project.quote)
            # print(project.terms)
            # print(project.tax)
            # print(project.billing)
            # print(project.labor_code)

        # control buttons  ----------------------------------------
        self.control_frame = Frame()
        self.control_frame.pack(fill=BOTH, anchor=W, padx=10, pady=10)
        self.ok = Button(self.control_frame, width=15, text="Ok", command=self.ok)
        self.ok.pack(padx=5, pady=20)

    def ok(self):
        root.quit()


if __name__ == "__main__":
    root = Tk()
    # center window on screen
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    app_width = 550
    app_height = 410
    root.geometry(f'{app_width}x{app_height}+{int((screen_width - app_width)/2)}+{int((screen_height - app_height)/2)}')
    title = WizardTitle(root)
    root.mainloop()


# notes:
# need to limit characters on name entry to max 27 *** completed 09/15/19 ***
# need to limit characters on zip entry to max 5 *** completed 09/15/19 ***
# Need to make previsions for door service number on projects.
# need to add pack_forget for customer_button
