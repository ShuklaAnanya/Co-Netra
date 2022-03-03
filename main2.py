from kivy.metrics import dp              # dp=Density Independent Pixels ~~> Measurements
from kivy.lang import Builder            # To connect Design file to the Main file
from kivy.core.window import Window      # To control size of the window

from kivymd.app import MDApp                     # The Main app
from kivymd.uix.datatables import MDDataTable    # Table to show Records
from kivymd.uix.menu import MDDropdownMenu       # Dropdown for visualise

import mysql.connector as s              # To establish python and MySQL connectivity

import matplotlib.pyplot as plt          # To derive graphs from the data accumulated

Window.maximize()                # Initializing the window screen as maximum
Window.minimum_width=875         # Specifying minimum size for window screen if minimized
Window.minimum_height=650
#MAIN-----------------------------------------------------------------------------------------------------------------------------------
class CONETRA(MDApp):    # Creating a class 'CONETRA' which is a user defined datastructure that holds attributes (member functions) to create instances of the class
   authority = 0
   user = 0
   checks = []
   instance_row_list = []
   #-----------------------------------------------------------------------------------------------------------------------------------
   #1 SELF:  IT REFERS TO 'CONETRA' THE APP
   #2 build: It is the function being run as soon as the app is run
   #3 root:  It refers to the design file
   #4 self.root : From the conetra app ,Returning the design file
   #5 ids : Referring to the ID of a widget

   def build(self):
       self.theme_cls.primary_palette = "Teal"   # Setting the primary background colour to Teal

       mycon = s.connect(host="localhost", user="root", passwd="dpsbn")  # Setting up Python-MySQL connectivity
       if mycon.is_connected() == False:
           print("Error connecting to MySQL Database!")
       else:
           cursor = mycon.cursor()
           cursor.execute("CREATE DATABASE IF NOT EXISTS CONETRA")
           mycon.commit()
           cursor.execute("USE CONETRA")
           mycon.commit()
           cursor.execute("CREATE TABLE IF NOT EXISTS USER_SIGNUP(AADHAAR DECIMAL(12,0) PRIMARY KEY, NAME VARCHAR(20) NOT NULL, AGE INTEGER NOT NULL, GENDER VARCHAR(6) NOT NULL, VACCINE VARCHAR(10), VACCINE_STATUS VARCHAR(20), COVID VARCHAR(10))")
           mycon.commit()

           #1st Table : user_signup ~~> aadhar,name,age,gender,vaccine_brand,vaccine_status,covid_details

           cursor.execute("CREATE TABLE IF NOT EXISTS ADMIN_SIGNUP(AADHAAR DECIMAL(12,0), FOREIGN KEY(AADHAAR) REFERENCES USER_SIGNUP(AADHAAR))")
           mycon.commit()

           #2nd Table : admin_signup ~~> aadhar

           # Inserting first dummy record:
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE AADHAAR=111122223333")
           cursor.fetchall()
           if cursor.rowcount == 0:
               cursor.execute("INSERT INTO USER_SIGNUP VALUES(111122223333,'Jemima',17,'Female','Covaxin','First Dose','No')")  # Inserting 1st Dummy record in user_signup
               mycon.commit()
           cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR=111122223333")
           cursor.fetchall()
           if cursor.rowcount == 0:
               cursor.execute("INSERT INTO ADMIN_SIGNUP VALUES(111122223333)")  # Inserting 1st Dummy record in admin_signup
               mycon.commit()

           # Inserting 2nd dummy record:
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE AADHAAR=444455556666")
           cursor.fetchall()
           if cursor.rowcount ==0:
               cursor.execute("INSERT INTO USER_SIGNUP VALUES(444455556666,'Ananya',17,'Female','Covaxin','First Dose','No')")  # Inserting 2nd Dummy record in user_signup
               mycon.commit()
           cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR=444455556666")
           cursor.fetchall()
           if cursor.rowcount == 0:
               cursor.execute("INSERT INTO ADMIN_SIGNUP VALUES(444455556666)")  # Inserting 2nd Dummy record in admin_signup
               mycon.commit()

           #inserting 3rd dummy record:
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE AADHAAR=818100008181")
           cursor.fetchall()
           if cursor.rowcount == 0:
               cursor.execute("INSERT INTO USER_SIGNUP VALUES(818100008181,'Aayushi Baijal',18,'Female','Covishield','Second Dose','Yes')")  # Inserting 3rd Dummy record in user_signup
               mycon.commit()
           cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR=818100008181")
           cursor.fetchall()
           if cursor.rowcount == 0:
               cursor.execute("INSERT INTO ADMIN_SIGNUP VALUES(818100008181)")  # Inserting 3rd Dummy record in admin_signup
               mycon.commit()
           mycon.close()

       #AUTHORITY PAGE: DATA TABLE
       self.data_tables = MDDataTable(
           pos_hint={"center_x": 0.5, "y": 0.05},     # Initializing the position of datatable on the window
           size_hint=(1,1),
           use_pagination=True,                       # When there is a lot of data , putting it in multiple pages
           check=True,                                # Checkboxes
           column_data=[("Aadhaar No.", dp(50)),      # Column Width
                        ("Name", dp(41)),
                        ("Age", dp(20)),
                        ("Gender", dp(35)),
                        ("Vaccine", dp(35)),
                        ("Vaccine Status", dp(35)),
                        ("Covid", dp(20))],
           sorted_on="Aadhaar No.",                   # Sorting the data on basis of Aadhar Number in ascending order
           sorted_order="ASC",                        # Similar to order by
       )

       self.data_tables.bind(on_check_press=self.on_check_press, on_row_press=self.on_row_press)
       self.root = Builder.load_file("design.kv")      # Builder loads the file into the variable named self.root (from the app we call the design file)
       self.root.ids.body.add_widget(self.data_tables) # Adding the data table to the box layout in the authority table

       #DROP DOWN ITEMS
       #1)VISUALIZE
       #2)GENDER
       #3)VACCINE_BRAND
       #4)VACCINE_STATUS
       #5)COVID_DETAILS

       # -------------------------------------------------------------
       #1)VISUALISE

       visualize_menu_items = [         # Defining the Visualize menu items
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Vaccination by Gender Trend",
               "on_release": lambda x="Vaccination by Gender Trend": self.visualize_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Vaccination by Type Trend",
               "on_release": lambda x="Vaccination by Type Trend": self.visualize_set_item(x),
           }]

       self.visualize_menu = MDDropdownMenu(        # Making the visualize dropdown list
           caller=self.root.ids.visualize,
           items=visualize_menu_items,
           position="bottom",
           width_mult=4)

       #-------------------------------------------------------------
       #2)GENDER

       gender_menu_items = [      # Defining the Gender menu items
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Male",
               "on_release": lambda x="Male": self.gender_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Female",
               "on_release": lambda x="Female": self.gender_set_item(x),
           }]

       self.gender_menu = MDDropdownMenu(         # Making the Gender dropdown list
           caller=self.root.ids.new_gender,
           items=gender_menu_items,
           position="bottom",
           width_mult=4)
       # -------------------------------------------------------------
       # 3)VACCINE_BRAND

       vaccine_menu_items = [
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Not Taken",
               "on_release": lambda x="Not Taken": self.vaccine_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Covishield",
               "on_release": lambda x="Covishield": self.vaccine_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Covaxin",
               "on_release": lambda x="Covaxin": self.vaccine_set_item(x),
           }]

       self.vaccine_menu = MDDropdownMenu(
           caller=self.root.ids.new_vaccine,
           items=vaccine_menu_items,
           position="bottom",
           width_mult=4)
       # -------------------------------------------------------------
       #4)VACCINE_STATUS

       vaccine_status_menu_items = [
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Not Taken",
               "on_release": lambda x="Not Taken": self.vaccine_status_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "First Dose",
               "on_release": lambda x="First Dose": self.vaccine_status_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Second Dose",
               "on_release": lambda x="Second Dose": self.vaccine_status_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Booster Shot",
               "on_release": lambda x="Booster Shot": self.vaccine_status_set_item(x),
           }]

       self.vaccine_status_menu = MDDropdownMenu(
           caller=self.root.ids.new_vaccine_status,
           items=vaccine_status_menu_items,
           position="bottom",
           width_mult=4)
       # -------------------------------------------------------------
       #5)COVID_DETAILS

       covid_menu_items = [
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "No",
               "on_release": lambda x="No": self.covid_set_item(x),
           },
           {
               "viewclass": "OneLineListItem",
               "height": dp(56),
               "text": "Yes",
               "on_release": lambda x="Yes": self.covid_set_item(x),
           }]

       self.covid_menu = MDDropdownMenu(
           caller=self.root.ids.new_covid,
           items=covid_menu_items,
           position="bottom",
           width_mult=4,)

       return self.root    # From the Conetra App , Returning the Design file

#2.VISULASE PAGE-----------------------------------------------------------------------------------------------------------------------------------

   def on_visualize_dropdown_press(self):
       self.visualize_menu.open()

   def visualize_set_item(self, text__item):
       self.visualize_menu.dismiss()      # Close the Visualize dropdown list
       if text__item == "Vaccination by Gender Trend":
           self.vaccination_by_gender_trend()   # Opens up Vaccination by Gender Trend graph
       else:
           self.vaccination_by_type_trend()     # Opens up Vaccination by Type Trend graph
   #1st GRAPH (Pie Plot)

   def vaccination_by_gender_trend(self):
       mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
       if mycon.is_connected() == False:
           print("Error connecting to MySQL Database!")
       else:

           cursor = mycon.cursor()
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE GENDER='Male' AND VACCINE_STATUS IS NOT NULL AND VACCINE_STATUS!='Not Taken'")
           cursor.fetchall()
           No_Male = cursor.rowcount        #NUMBER OF MALES THAT HAVE TAKEN THE VACCINE
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE GENDER='Female' AND VACCINE_STATUS IS NOT NULL AND VACCINE_STATUS!='Not Taken'")
           cursor.fetchall()
           No_Female = cursor.rowcount      #NUMBER OF FEMALES THAT HAVE TAKEN THE VACCINE
           mycon.close()

           # create data
           names = 'Male', 'Female'          # Name of plot sections [Labels]
           values = [No_Male, No_Female]
           colors = ['#d16949', '#8bd09f']   # Setting the colours of the plot section

           # Create a pieplot (USING MATPLOTLIB)
           plt.pie(values)

           # Label Distance: Gives the space between labels and the center of the pie
           plt.pie(values, labels=names, labeldistance=1.15, wedgeprops={'linewidth': 3, 'edgecolor': 'white'},colors=colors)

           # Set title for plot
           plt.title("Vaccination by Gender Trend", size=18)
           plt.show()

   #2nd GRAPH
   def vaccination_by_type_trend(self):
       mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
       if mycon.is_connected() == False:
           print("Error connecting to MySQL Database!")
       else:
           cursor = mycon.cursor()
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE VACCINE='Covaxin'")
           cursor.fetchall()
           No_Covax = cursor.rowcount     #NUMBER OF PEOPLE WHO GOT COVAXIN
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE VACCINE='Covishield'")
           cursor.fetchall()
           No_Coshield = cursor.rowcount  #NUMBER OF PEOPLE WHO GOT COVISHIELD
           mycon.close()

           # create data
           names = ['Covaxin', 'Covishield']
           size = [No_Covax, No_Coshield]

           # Create a circle at the center of the donut plot
           my_circle = plt.Circle((0,0),0.5, color='white')

           # Custom wedges
           plt.pie(size, labels=names, wedgeprops={'linewidth': 7, 'edgecolor': 'white'})
           p = plt.gcf() #get current figure
           p.gca().add_artist(my_circle)

           # Set title for plot
           plt.title("Vaccination by Type Trend", size=18)
           plt.show()

#3.-----------------------------------------------------------------------------------------------------------------------------------

   def login_1_to_homepage(self):
       self.root.current = "homepage"
       self.root.ids.aadhaar.text = ""

       self.root.ids.aadhaar.required = False                 # Removing all the errors
       self.root.ids.aadhaar.error = False
       self.root.ids.aadhaar.helper_text_mode = "on_focus"    # Helper text inside the box in login page
       self.root.ids.aadhaar.helper_text = '.'
       self.root.ids.aadhaar.focus = True                     # Focuses on a text input field when clicked upon

   def login_1_to_signup_1(self):
       self.root.ids.new_account.text = "New Account"
       self.root.ids.new_account.font_size = 30
       self.root.current = "signup_1"
       self.root.ids.aadhaar.required = False
       self.root.ids.aadhaar.helper_text_mode = "on_focus"
       self.root.ids.aadhaar.helper_text = '.'
       self.root.ids.aadhaar.error = False
       self.root.ids.aadhaar.focus = True
       self.root.ids.aadhaar.text = ""

   def signup_1_to_homepage(self):
       self.root.ids.error_icon_1.text_color = 1, 1, 1, 1   # Making the error icon White when it goes back
       self.root.ids.error_1.text = ""                      # To remove to error message
       if CONETRA.authority == 1 or CONETRA.user == 1:
           self.root.current = "login_2"
       else:
           self.root.current = "homepage"
           self.root.ids.aadhaar.required = False
           self.root.ids.aadhaar.helper_text_mode = "on_focus"
           self.root.ids.aadhaar.helper_text = "."
           self.root.ids.aadhaar.focus = True

       self.root.ids.new_aadhaar.text = ""               # Removing all the text fields when the user goes back from the signup page
       self.root.ids.new_aadhaar.disabled = False
       self.root.ids.new_name.text = ""
       self.root.ids.new_age.text = ""
       self.root.ids.new_gender.text = ""

   def on_gender_dropdown_press(self): # Disabling entering the text into the dropdown,but allows to edit your previous choice from dropdown list
       if self.root.ids.new_gender.disabled == True:
           self.root.ids.new_gender.disabled = False
       else:
           self.root.ids.new_gender.disabled = True
       self.gender_menu.open()

   def gender_set_item(self, text__item):
       self.root.ids.new_gender.text = text__item
       self.gender_menu.dismiss()                            # Dismissing the menu once the option is chosen
       self.root.ids.new_gender.disabled = False             # Allowing them to edit the previous choice

   def signup_1_to_login_2(self):
       self.root.ids.error_icon_1.text_color = 1, 1, 1, 1  # Setting the error icon as white
       self.root.ids.error_1.text = ""                     # Removing the error text
       aadhaar=self.root.ids.new_aadhaar.text              # Retrieving the text entered for aadhar,name,age,gender
       name = self.root.ids.new_name.text
       age = self.root.ids.new_age.text
       gender = self.root.ids.new_gender.text
       if aadhaar=="" or name=="" or age=="" or gender=="":    # Checking constraints
           self.root.ids.error_icon_1.text_color=0.89, 0.02, 0, 1  # Setting error text colour to red
           self.root.ids.error_1.text="[color=#e30400]All fields are required!"
       elif aadhaar.isdigit()==False:
           self.root.ids.error_icon_1.text_color=0.89, 0.02, 0, 1
           self.root.ids.error_1.text = "[color=#e30400]Incorrect aadhaar entered!"
       elif len(aadhaar)!=12:
           self.root.ids.error_icon_1.text_color =0.89, 0.02, 0, 1
           self.root.ids.error_1.text = "[color=#e30400]Incorrect aadhaar entered! Aadhaar must be 12 digits long."
       elif age.isdigit()==False or int(age)>125:
           self.root.ids.error_icon_1.text_color=0.89, 0.02, 0, 1
           self.root.ids.error_1.text = "[color=#e30400]Incorrect age entered!"
       else:
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               aadhaar = int(aadhaar)
               age = int(age)
               cursor = mycon.cursor()
               if CONETRA.user == 0:      # When it's not a user ~~> value=0
                   cursor.execute("SELECT * FROM USER_SIGNUP WHERE AADHAAR={}".format(aadhaar))    # Checking if aadhaar number already exists
                   data = cursor.fetchall()
                   if cursor.rowcount == 0:
                       cursor.execute("INSERT INTO USER_SIGNUP(NAME,AGE,AADHAAR,GENDER) VALUES ('{}',{},{},'{}')".format(name, age, aadhaar, gender))
                       mycon.commit()
                       CONETRA.user = 1#when it's a user -->value=1
                   else:
                       self.root.ids.error_icon_1.text_color = 0.89, 0.02, 0, 1  # Show error if user is already registered
                       self.root.ids.error_1.text = "[color=#e30400]Incorrect aadhaar entered! Aadhaar no. already exists."
               else:    # If already a user, updating basic details
                   cursor.execute("UPDATE USER_SIGNUP SET NAME='{}',AGE={},GENDER='{}' WHERE AADHAAR={}".format(name,age,gender,aadhaar))
                   mycon.commit()
               mycon.close()
               if CONETRA.user == 1:   #  Only if the record has been successfully inserted into the database
                   #  only if the aadhaar number already does not exist
                   self.root.ids.log_aadhaar.text = str(aadhaar)
                   self.root.ids.log_name.text = name
                   self.root.ids.log_age.text = str(age)
                   self.root.ids.log_gender.text = gender
                   self.root.ids.log_vaccine.text = "N/A"
                   self.root.ids.log_vaccine_status.text = "N/A"
                   self.root.ids.log_covid.text = "N/A"
                   self.root.ids.add_authority_icon.icon = ""

                   self.root.current = "login_2"
                   # Removing text from the labels of sign_up
                   self.root.ids.new_account.text = "New Account"
                   self.root.ids.new_aadhaar.text = ""
                   self.root.ids.new_aadhaar.disabled = False
                   self.root.ids.new_name.text = ""
                   self.root.ids.new_age.text = ""
                   self.root.ids.new_gender.text = ""

   def login_1_to_login_2(self):
       aadhaar = self.root.ids.aadhaar.text
       if aadhaar=="":
           self.root.ids.aadhaar.helper_text = "This field is required"
           self.root.ids.aadhaar.helper_text_mode = "on_error"
           self.root.ids.aadhaar.required = True  # 'all fields are required'~~> error to be displayed
           self.root.ids.aadhaar.focus = True
       elif aadhaar.isdigit()==False:
           self.root.ids.aadhaar.text = ""
           self.root.ids.aadhaar.helper_text = "Incorrect Aadhaar entered"
           self.root.ids.aadhaar.helper_text_mode = "on_error"
           self.root.ids.aadhaar.error = True
           self.root.ids.aadhaar.focus = True
       else:
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               aadhaar=int(aadhaar)
               cursor = mycon.cursor()
               cursor.execute("SELECT * FROM USER_SIGNUP WHERE AADHAAR={}".format(aadhaar))    # Checking if user is already signed up
               data = cursor.fetchall()
               if cursor.rowcount ==0:    # Account doesn't exist (user is logging-in)
                   self.root.ids.aadhaar.text = ""
                   self.root.ids.aadhaar.helper_text = "Incorrect Aadhaar entered"
                   self.root.ids.aadhaar.helper_text_mode = "on_error"
                   self.root.ids.aadhaar.error = True
                   self.root.ids.aadhaar.focus = True
               else:    # Account exists
                   CONETRA.user = 1
                   #displaying the details of the person logged in (in login-2 page) (as labels)
                   self.root.ids.log_aadhaar.text = str(data[0][0])
                   self.root.ids.log_name.text = data[0][1]
                   self.root.ids.log_age.text = str(data[0][2])
                   self.root.ids.log_gender.text = data[0][3]
                   if data[0][4] == None:
                       self.root.ids.log_vaccine.text = "N/A"
                   else:
                       self.root.ids.log_vaccine.text = data[0][4]
                   if data[0][5] == None:
                       self.root.ids.log_vaccine_status.text = "N/A"
                   else:
                       self.root.ids.log_vaccine_status.text = data[0][5]
                   if data[0][6] == None:
                       self.root.ids.log_covid.text = "N/A"
                   else:
                       self.root.ids.log_covid.text = data[0][6]

                   self.root.ids.add_authority_icon.icon = ""   # Not displaying the authority icon

                   self.root.current = "login_2"

                   self.root.ids.aadhaar.required = False             # Removing whatever errors are present
                   self.root.ids.aadhaar.helper_text_mode = "on_focus"
                   self.root.ids.aadhaar.helper_text = '.'
                   self.root.ids.aadhaar.error = False
                   self.root.ids.aadhaar.focus = True
                   self.root.ids.aadhaar.text = ""
               mycon.close()

   def login_2_to_homepage(self):
       if CONETRA.authority == 1: # If the person in an authority
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               cursor = mycon.cursor()
               cursor.execute("SELECT * FROM USER_SIGNUP")
               data = cursor.fetchall()
               self.data_tables.row_data = []               # Clearing the rows in the datatable and updating the rows
               for i in data:                               # i is one entire record (tuple)   #data is a list
                   i = list(i)
                   if i[4] == None:
                       i[4] = "N/A"
                   if i[5] == None:
                       i[5] = "N/A"
                   if i[6] == None:
                       i[6] = "N/A"
                   self.data_tables.row_data.append(i)
               mycon.close()
               self.root.current = "authority"  # From signup 2 to authority page
       else:
           CONETRA.user = 0  # If person logging in is user
           self.root.current = "homepage"

       self.root.ids.log_aadhaar.text = ""   # Removing any text input in fields
       self.root.ids.log_name.text = ""
       self.root.ids.log_age.text = ""
       self.root.ids.log_gender.text = ""
       self.root.ids.log_vaccine.text = ""
       self.root.ids.log_vaccine_status.text = ""
       self.root.ids.log_covid.text= ""

   def login_2_update(self):   # Authority goes to signup_2 but user will go to update_signup_1
       if CONETRA.authority == 1:
           self.root.ids.update_aadhaar.text = self.root.ids.log_aadhaar.text
           if self.root.ids.log_vaccine.text == "N/A":
               self.root.ids.new_vaccine.text = ""
           else:
               self.root.ids.new_vaccine.text = self.root.ids.log_vaccine.text
           if self.root.ids.log_vaccine.text == "N/A":
               self.root.ids.new_vaccine_status.text = ""
           else:
               self.root.ids.new_vaccine_status.text = self.root.ids.log_vaccine_status.text
           if self.root.ids.log_vaccine.text == "N/A":
               self.root.ids.new_covid.text = ""
           else:
               self.root.ids.new_covid.text = self.root.ids.log_covid.text

           self.root.current = "signup_2"

       else:   # If user wishes to update data
           self.root.ids.new_account.text = "Change Details:"
           self.root.ids.new_account.font_size = 20
           self.root.ids.new_aadhaar.text = self.root.ids.log_aadhaar.text   # Cannot edit Aadhaar Number
           self.root.ids.new_aadhaar.disabled = True
           self.root.ids.new_name.text = self.root.ids.log_name.text
           self.root.ids.new_age.text = self.root.ids.log_age.text
           self.root.ids.new_gender.text = self.root.ids.log_gender.text

           self.root.current = "signup_1"

   def signup_2_back_to_login_2(self): # On pressing the back button
       self.root.ids.error_icon_2.text_color = 1, 1, 1, 1   # Error icon colour changed to white
       self.root.ids.error_2.text = ""                      # Error text removed
       aadhaar = self.root.ids.update_aadhaar.text
       mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
       if mycon.is_connected() == False:
           print("Error connecting to MySQL Database!")
       else:
           cursor = mycon.cursor()
           cursor.execute("SELECT * FROM USER_SIGNUP WHERE AADHAAR={}".format(aadhaar))
           data = cursor.fetchone()

           # Entering details into the login_2 page
           # data=(111122223333,'Ananya',17,'Female','Covaxin','Second Dose','Yes')

           self.root.ids.log_aadhaar.text = aadhaar
           self.root.ids.log_name.text = data[1]
           self.root.ids.log_age.text = str(data[2])
           self.root.ids.log_gender.text = data[3]
           if data[4] == None:
               self.root.ids.log_vaccine.text = "N/A"
           else:
               self.root.ids.log_vaccine.text = data[4]
           if data[5] == None:
               self.root.ids.log_vaccine_status.text = "N/A"
           else:
               self.root.ids.log_vaccine_status.text = data[5]
           if data[6] == None:
               self.root.ids.log_covid.text = "N/A"
           else:
               self.root.ids.log_covid.text = data[6]

           self.root.current = "login_2"
           # Clearing the signup_2 page

           self.root.ids.update_aadhaar.text = ""
           self.root.ids.new_vaccine.text = ""
           self.root.ids.new_vaccine_status.text = ""
           self.root.ids.new_covid.text = ""

   def signup_2_to_login_2(self):  # On pressing the Submit Button
       self.root.ids.error_icon_2.text_color = 1, 1, 1, 1   # Setting error icon colour to white
       self.root.ids.error_2.text = ""                      # Removing error text
       vaccine = self.root.ids.new_vaccine.text
       vaccine_status = self.root.ids.new_vaccine_status.text
       covid = self.root.ids.new_covid.text
       aadhaar = self.root.ids.update_aadhaar.text

       if vaccine=="" or vaccine_status=="" or covid=="":    # Checking if all vaccine related details have been entered
           self.root.ids.error_icon_2.text_color = 0.89, 0.02, 0, 1  # Changing error text to red
           self.root.ids.error_2.text = "[color=#e30400]All fields are required!"
       else:
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               cursor = mycon.cursor()    # Authority updating users' vaccine related details
               cursor.execute("UPDATE USER_SIGNUP SET VACCINE='{}',VACCINE_STATUS='{}',COVID='{}' WHERE AADHAAR={}".format(vaccine,vaccine_status,covid,aadhaar))
               mycon.commit()
               cursor.execute("SELECT * FROM USER_SIGNUP WHERE AADHAAR={}".format(aadhaar))
               data=cursor.fetchone()
                                        # Filling the labels details in the login_2 page after updating the vaccine information
               self.root.ids.log_aadhaar.text = aadhaar
               self.root.ids.log_name.text = data[1]
               self.root.ids.log_age.text = str(data[2])
               self.root.ids.log_gender.text = data[3]
               self.root.ids.log_vaccine.text = vaccine
               self.root.ids.log_vaccine_status.text = vaccine_status
               self.root.ids.log_covid.text = covid

               self.root.current = "login_2"

               self.root.ids.update_aadhaar.text = ""         # Removing text in the labels of the signup_2 page
               self.root.ids.new_vaccine.text = ""
               self.root.ids.new_vaccine_status.text = ""
               self.root.ids.new_covid.text = ""

   def delete_record(self):    # Delete icon
       mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
       if mycon.is_connected() == False:
           print("Error connecting to MySQL Database!")
       else:
           aadhaar = self.root.ids.log_aadhaar.text
           cursor = mycon.cursor()
           # If you are trying to delete an admin record, first it is to be deleted from the admin_table , only then from the user table
           # (else foreign key error or refrential integrity constraint is violated)
           cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(aadhaar))
           cursor.fetchone()
           if cursor.rowcount == 1:
               cursor.execute("DELETE FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(aadhaar))
               mycon.commit()
           cursor.execute("DELETE FROM USER_SIGNUP WHERE AADHAAR={}".format(aadhaar))   # Deleting the record from user_signup table
           mycon.commit()
           if CONETRA.authority == 1:
               self.root.current = "authority"
           else:
               self.root.current = "homepage"
           self.root.ids.log_aadhaar.text = ""                 # Clearing all text fields from login_2 page
           self.root.ids.log_name.text = ""
           self.root.ids.log_age.text = ""
           self.root.ids.log_gender.text = ""
           self.root.ids.log_vaccine.text = ""
           self.root.ids.log_vaccine_status.text = ""
           self.root.ids.log_covid.text = ""

   def login_1_to_authority(self):
       aadhaar = self.root.ids.aadhaar.text
       if aadhaar == "":
           self.root.ids.aadhaar.required = True
           self.root.ids.aadhaar.helper_text = "This field is required"  # Showing error text if no aadhar number is entered
           self.root.ids.aadhaar.helper_text_mode = "on_error"
           self.root.ids.aadhaar.focus = True
       elif aadhaar.isdigit() == False:
           self.root.ids.aadhaar.text = ""
           self.root.ids.aadhaar.helper_text = "Incorrect Aadhaar entered"  # Showing error text if Aadhar number entered is text
           self.root.ids.aadhaar.helper_text_mode = "on_error"
           self.root.ids.aadhaar.error = True
           self.root.ids.aadhaar.focus = True
       else:
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               aadhaar = int(aadhaar)
               cursor = mycon.cursor()
               cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(aadhaar))  # Checking whether its an admin then only they can login as admin
               data = cursor.fetchall()
               if cursor.rowcount ==0:   # Not an admin
                   self.root.ids.aadhaar.text = ""
                   self.root.ids.aadhaar.helper_text = "Incorrect Aadhaar entered"
                   self.root.ids.aadhaar.helper_text_mode = "on_error"
                   self.root.ids.aadhaar.error = True
                   self.root.ids.aadhaar.focus = True
               else:     # It is an admin
                   CONETRA.authority = 1
                   cursor.execute("SELECT * FROM USER_SIGNUP")
                   data=cursor.fetchall()
                   for i in data:
                       i=list(i)
                       if i[4] == None:
                           i[4] = "N/A"
                       if i[5] == None:
                           i[5] = "N/A"
                       if i[6] == None:
                           i[6] = "N/A"
                       self.data_tables.row_data.append(i)    # Updating the admin display table every time the authority logs in
                   self.root.current = "authority"
                   self.root.ids.aadhaar.required = False     # Rremoving the ~~> 'all fields are required' Error
                   self.root.ids.aadhaar.helper_text_mode = "on_focus"
                   self.root.ids.aadhaar.helper_text = '.'
                   self.root.ids.aadhaar.error = False
                   self.root.ids.aadhaar.focus = True
                   self.root.ids.aadhaar.text = ""
               mycon.close()

   def authority_to_homepage(self):
       self.root.current = "homepage"
       # Instance_row_list: To keep track of all the rows that have been clicked
       for i in CONETRA.instance_row_list:
           i.ids.check.state = 'normal'      # Unchecking the Check Boxes
       CONETRA.instance_row_list = []
       self.data_tables.row_data = []   # Clearing the data table when Admin exits
       CONETRA.authority=0

   def clear_search(self):    # Clearing the textfields in the search operation and showing all records in the admin display table
       self.root.ids.authority_aadhaar.text = ""
       self.root.ids.authority_name.text = ""
       self.root.ids.authority_age.text = ""
       self.root.ids.authority_gender.text = ""
       for i in CONETRA.instance_row_list:
           i.ids.check.state = 'normal'
       CONETRA.instance_row_list = []
       mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
       if mycon.is_connected() == False:
           print("Error connecting to MySQL Database!")
       else:  # To show all the records in the data table with no constraints
           cursor = mycon.cursor()
           cursor.execute("SELECT * FROM USER_SIGNUP")
           data = cursor.fetchall()
           self.data_tables.row_data = []
           for i in data:
               i=list(i)
               if i[4] == None:
                   i[4] = "N/A"
               if i[5] == None:
                   i[5] = "N/A"
               if i[6] == None:
                   i[6] = "N/A"
               self.data_tables.row_data.append(i)

   def authority_to_login_2(self):    # Authority viewing the user account page
       if len(CONETRA.checks) == 1:
           self.root.ids.log_aadhaar.text = str(CONETRA.checks[0][0])
           self.root.ids.log_name.text = CONETRA.checks[0][1]
           self.root.ids.log_age.text = str(CONETRA.checks[0][2])
           self.root.ids.log_gender.text = CONETRA.checks[0][3]
           self.root.ids.log_vaccine.text = CONETRA.checks[0][4]
           self.root.ids.log_vaccine_status.text = CONETRA.checks[0][5]
           self.root.ids.log_covid.text = CONETRA.checks[0][6]

           aadhaar = CONETRA.checks[0][0]
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               cursor = mycon.cursor()
               cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(aadhaar))
               cursor.fetchall()
               if cursor.rowcount ==0:
                   self.root.ids.add_authority_icon.icon = "account-plus"  # Checking whether Admin or not and displaying the appropriate icon
               else:
                   self.root.ids.add_authority_icon.icon = "account-cancel"
               mycon.close()

           self.root.current = "login_2"

           for i in CONETRA.instance_row_list:
               i.ids.check.state = 'normal'
           CONETRA.instance_row_list = []

   def add_authority(self):
       if CONETRA.user == 0:
           aadhaar = int(self.root.ids.log_aadhaar.text)
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               cursor = mycon.cursor()
               cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(aadhaar))
               cursor.fetchall()
               if cursor.rowcount ==0:
                   cursor.execute("INSERT INTO ADMIN_SIGNUP VALUES({})".format(aadhaar))
                   self.root.ids.add_authority_icon.icon = "account-cancel"  # Updating the admin icon
               else:
                   cursor.execute("DELETE FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(aadhaar))
                   self.root.ids.add_authority_icon.icon = "account-plus"
               mycon.commit()
               mycon.close()

#----------------------------------------------------------------
   def on_vaccine_dropdown_press(self):# Disabling entering the text into the dropdown,but allows to edit your previous choice from dropdown list
       if self.root.ids.new_vaccine.disabled == True:
           self.root.ids.new_vaccine.disabled = False
       else:
           self.root.ids.new_vaccine.disabled = True
       self.vaccine_menu.open()

   def vaccine_set_item(self, text__item):
       self.root.ids.new_vaccine.text = text__item
       self.vaccine_menu.dismiss()
       self.root.ids.new_vaccine.disabled = False
# ----------------------------------------------------------------
   def on_vaccine_status_dropdown_press(self):
       if self.root.ids.new_vaccine_status.disabled == True:
           self.root.ids.new_vaccine_status.disabled = False
       else:
           self.root.ids.new_vaccine_status.disabled = True
       self.vaccine_status_menu.open()

   def vaccine_status_set_item(self, text__item):
       self.root.ids.new_vaccine_status.text = text__item
       self.vaccine_status_menu.dismiss()
       self.root.ids.new_vaccine_status.disabled = False
# ----------------------------------------------------------------
   def on_covid_dropdown_press(self):
       if self.root.ids.new_covid.disabled == True:
           self.root.ids.new_covid.disabled = False
       else:
           self.root.ids.new_covid.disabled = True
       self.covid_menu.open()

   def covid_set_item(self, text__item):
       self.root.ids.new_covid.text = text__item
       self.covid_menu.dismiss()
       self.root.ids.new_covid.disabled = False
#------------------------------------------------------------------
   def delete_records(self):    # Deleting multiple records at a time using admin display table
       if len(CONETRA.checks)!=0:   # Only if ,atleast 1 checkbox is pressed
           mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
           if mycon.is_connected() == False:
               print("Error connecting to MySQL Database!")
           else:
               # If you are trying to delete an admin record, first it is to be deleted from the admin_table ,
               # only then from the user table (else foreign key error or refrential integrity constraint is violated)
               cursor = mycon.cursor()
               for i in CONETRA.checks:
                   cursor.execute("SELECT * FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(i[0]))
                   cursor.fetchone()
                   if cursor.rowcount == 1:
                       cursor.execute("DELETE FROM ADMIN_SIGNUP WHERE AADHAAR={}".format(i[0]))
                       mycon.commit()
                   cursor.execute("DELETE FROM USER_SIGNUP WHERE AADHAAR={}".format(i[0]))
                   mycon.commit()
               for i in CONETRA.instance_row_list:
                   i.ids.check.state = 'normal'
               CONETRA.checks = []
               CONETRA.instance_row_list = []

               cursor.execute("SELECT * FROM USER_SIGNUP")
               data = cursor.fetchall()
               self.data_tables.row_data=[]
               for i in data:
                   i = list(i)
                   if i[4] == None:
                       i[4] = "N/A"
                   if i[5] == None:
                       i[5] = "N/A"
                   if i[6] == None:
                       i[6] = "N/A"
                   self.data_tables.row_data.append(i)    # Updating admin display table appropriately
               mycon.close()

   def authority_search(self):
       for i in CONETRA.instance_row_list:
           i.ids.check.state = 'normal'
       CONETRA.instance_row_list = []
       mycon = s.connect(host="localhost", user="root", passwd="dpsbn", database="CONETRA")
       if mycon.is_connected() == False:
           print("Error connecting to MySQL Database!")
       else:
           aadhaar = self.root.ids.authority_aadhaar.text
           name = self.root.ids.authority_name.text
           age = self.root.ids.authority_age.text
           gender = self.root.ids.authority_gender.text
           cursor = mycon.cursor()
           query = "SELECT * FROM USER_SIGNUP"    # Creating the search query
           l1 = []
           l2 = []
           if aadhaar != "":
               if aadhaar.isdigit() == False:
                   aadhaar = 0
               else:
                   aadhaar = int(aadhaar)
               l1.append("AADHAAR=%s")
               l2.append(aadhaar)
           if name != "":
               name = "%"+name+"%"
               l1.append("NAME LIKE '%s'")
               l2.append(name)
           if age != "":
               if age.isdigit() == False:
                   age = 1000
               else:
                   age = int(age)
               l1.append("AGE=%s")
               l2.append(age)
           if gender != "":
               l1.append("GENDER='%s'")
               l2.append(gender)
           if len(l1) != 0:
               query += " WHERE "
               for i in range(len(l1)):
                   if i == len(l1) - 1:
                       query += l1[i]
                   else:
                       query += l1[i] + " AND "
               l2 = tuple(l2)
               cursor.execute(query % l2)
           else:
               cursor.execute(query)
           data = cursor.fetchall()
           self.data_tables.row_data = []
           for i in data:
               i = list(i)
               if i[4] == None:
                   i[4] = "N/A"
               if i[5] == None:
                   i[5] = "N/A"
               if i[6] == None:
                   i[6] = "N/A"
               self.data_tables.row_data.append(i)    # Updating the datatable according to the search query by the admin

   def on_check_press(self, instance_table, current_row):
       # Called when the check box in the table row is checked
       if current_row not in CONETRA.checks:  # On clicking , we're adding it to checks list
           CONETRA.checks.append(current_row)    # Storing the values of the records that have been checked in the admin display table
       else:  # On unclicking , we're removing it from checks list
           CONETRA.checks.remove(current_row)
       if len(CONETRA.checks)>1:
           self.root.ids.delete_record.text = "Delete all("+str(len(CONETRA.checks))+")" # Changing the text of the button
       else:
           self.root.ids.delete_record.text = "Delete"

   def on_row_press(self, instance_table, instance_row): # Adding the ID of the row in the instance_row (list of the id of the row clicked)
       CONETRA.instance_row_list.append(instance_row)

CONETRA().run()
#conetra is the MD App
