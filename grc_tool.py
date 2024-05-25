import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, db
import time
import hashlib

class PasswordLock:
    def __init__(self, firebase_db):
        self.firebase_db = firebase_db
        self.root = tk.Tk()
        self.root.title("Password Lock")
        self.root.geometry("300x150")
        self.password_given = False  # Flag to track whether password was given or not
        
        self.create_widgets()
    
    def create_widgets(self):
        self.password_label = ttk.Label(self.root, text="Enter Password:")
        self.password_label.pack(pady=5)
        
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        self.unlock_button = ttk.Button(self.root, text="Unlock", command=self.check_password)
        self.unlock_button.pack(pady=5)
        
        # Bind a function to handle closing event of the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def check_password(self):
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Replace this with your actual hashed password
        actual_password = "6f5df9690af768d6a12c83ad028ed35078ed8e1b739acb47f9b8f6d8d8b21497"  # Hash of "sangit"
        
        if hashed_password == actual_password:
            self.password_given = True  # Set flag to True if password is correct
            self.root.destroy()  # Close the password dialog
            self.open_main_app()
        else:
            messagebox.showerror("Error", "Incorrect password!")
    
    def open_main_app(self):
        import grc_tool
        grc_tool.main(self.firebase_db)
    
    def on_close(self):
        self.root.withdraw()  # Hide the password dialog
        self.root.quit()  # Quit the Tkinter application


class Risk:
    def __init__(self, name, description, likelihood, impact):
        self.name = name
        self.description = description
        self.likelihood = likelihood
        self.impact = impact
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp when Risk object is created

    def to_dict(self):
        return {'name': self.name, 'description': self.description, 'likelihood': self.likelihood, 'impact': self.impact, 'timestamp': self.timestamp}

class LeadershipPractice:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp when LeadershipPractice object is created

    def to_dict(self):
        return {'name': self.name, 'description': self.description, 'timestamp': self.timestamp}

class Compliance:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp when Compliance object is created

    def to_dict(self):
        return {'name': self.name, 'description': self.description, 'timestamp': self.timestamp}

class GRC_Tool:
    def __init__(self, firebase_db):
        self.firebase_db = firebase_db
        self.risks = []
        self.leadership_practices = []
        self.compliances = []

    def add_risk(self, risk):
        self.risks.append(risk)
        self.firebase_db.child('risks').push().set(risk.to_dict())  # Push data to Firebase

    def remove_risk(self, risk_name):
        self.risks = [r for r in self.risks if r.name != risk_name]

    def add_leadership_practice(self, practice):
        self.leadership_practices.append(practice)
        self.firebase_db.child('leadership_practices').push().set(practice.to_dict())  # Push data to Firebase

    def remove_leadership_practice(self, practice_name):
        self.leadership_practices = [p for p in self.leadership_practices if p.name != practice_name]

    def add_compliance(self, compliance):
        self.compliances.append(compliance)
        self.firebase_db.child('compliances').push().set(compliance.to_dict())  # Push data to Firebase

    def remove_compliance(self, compliance_name):
        self.compliances = [c for c in self.compliances if c.name != compliance_name]

class GRC_Tool_GUI:
    def __init__(self, root, grc_tool, firebase_db):
        self.root = root
        self.root.title("Khatra GRC")

        self.grc_tool = grc_tool
        self.firebase_db = firebase_db

        # Create background image
        bg_image = Image.open("grc.png")  # Open the image file with Pillow
        self.bg_photo = ImageTk.PhotoImage(bg_image)  # Convert the image to PhotoImage format compatible with Tkinter
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create header
        header_label = ttk.Label(self.root, text="Khatra GRC", font=('Helvetica', 36, 'bold'), foreground="#FFFFFF", background="#0078D7")
        header_label.place(relx=0.5, y=20, anchor="center")

        # Create frame for tabs
        self.frame = ttk.Frame(self.root, width=600, height=400, style='Inner.TFrame')
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.risk_tab = ttk.Frame(self.notebook)
        self.lp_tab = ttk.Frame(self.notebook)
        self.comp_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.risk_tab, text='Risks')
        self.notebook.add(self.lp_tab, text='Leadership Practices')
        self.notebook.add(self.comp_tab, text='Compliances')

        # Initialize widgets
        self.init_risk_tab()
        self.init_lp_tab()
        self.init_comp_tab()

    def init_risk_tab(self):
        # Labels
        ttk.Label(self.risk_tab, text="Name:", font=('Helvetica', 14)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.risk_tab, text="Description:", font=('Helvetica', 14)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.risk_tab, text="Likelihood:", font=('Helvetica', 14)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.risk_tab, text="Impact:", font=('Helvetica', 14)).grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Entry fields
        self.risk_name_entry = ttk.Entry(self.risk_tab)
        self.risk_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.risk_desc_entry = ttk.Entry(self.risk_tab)
        self.risk_desc_entry.grid(row=1, column=1, padx=10, pady=10)
        self.risk_likelihood_entry = ttk.Entry(self.risk_tab)
        self.risk_likelihood_entry.grid(row=2, column=1, padx=10, pady=10)
        self.risk_impact_entry = ttk.Entry(self.risk_tab)
        self.risk_impact_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(self.risk_tab, text="Add Risk", command=self.add_risk, style='PaddedButton.TButton').grid(row=4, column=0, columnspan=2, padx=10, pady=20, sticky='we')

    def init_lp_tab(self):
        # Labels
        ttk.Label(self.lp_tab, text="Name:", font=('Helvetica', 14)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.lp_tab, text="Description:", font=('Helvetica', 14)).grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Entry fields
        self.lp_name_entry = ttk.Entry(self.lp_tab)
        self.lp_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.lp_desc_entry = ttk.Entry(self.lp_tab)
        self.lp_desc_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(self.lp_tab, text="Add Leadership Practice", command=self.add_lp, style='PaddedButton.TButton').grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky='we')

    def init_comp_tab(self):
        # Labels
        ttk.Label(self.comp_tab, text="Name:", font=('Helvetica', 14)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.comp_tab, text="Description:", font=('Helvetica', 14)).grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Entry fields
        self.comp_name_entry = ttk.Entry(self.comp_tab)
        self.comp_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.comp_desc_entry = ttk.Entry(self.comp_tab)
        self.comp_desc_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(self.comp_tab, text="Add Compliance", command=self.add_comp, style='PaddedButton.TButton').grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky='we')

    def add_risk(self):
        name = self.risk_name_entry.get()
        description = self.risk_desc_entry.get()
        likelihood = self.risk_likelihood_entry.get()
        impact = self.risk_impact_entry.get()
        risk = Risk(name, description, likelihood, impact)
        self.grc_tool.add_risk(risk)
        self.clear_risk_fields()
        print("Risk added successfully!")  # You can replace this with a messagebox or status update

    def add_lp(self):
        name = self.lp_name_entry.get()
        description = self.lp_desc_entry.get()
        lp = LeadershipPractice(name, description)
        self.grc_tool.add_leadership_practice(lp)
        self.clear_lp_fields()
        print("Leadership Practice added successfully!")  # You can replace this with a messagebox or status update

    def add_comp(self):
        name = self.comp_name_entry.get()
        description = self.comp_desc_entry.get()
        comp = Compliance(name, description)
        self.grc_tool.add_compliance(comp)
        self.clear_comp_fields()
        print("Compliance added successfully!")  # You can replace this with a messagebox or status update

    def clear_risk_fields(self):
        self.risk_name_entry.delete(0, 'end')
        self.risk_desc_entry.delete(0, 'end')
        self.risk_likelihood_entry.delete(0, 'end')
        self.risk_impact_entry.delete(0, 'end')

    def clear_lp_fields(self):
        self.lp_name_entry.delete(0, 'end')
        self.lp_desc_entry.delete(0, 'end')

    def clear_comp_fields(self):
        self.comp_name_entry.delete(0, 'end')
        self.comp_desc_entry.delete(0, 'end')

def main(firebase_db):
    root = tk.Tk()
    root.geometry("800x600")  # Set initial size of the window
    grc_tool = GRC_Tool(firebase_db)
    app = GRC_Tool_GUI(root, grc_tool, firebase_db)

    # Styling
    style = ttk.Style(root)
    style.configure('PaddedButton.TButton', padding=(10, 5), font=('Helvetica', 12))
    style.configure('Inner.TFrame', background='#FFFFFF')

    root.mainloop()

if __name__ == "__main__":
    cred = credentials.Certificate('C:/Users/Asus/Desktop/new/serviceaccount.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://grc-project-a0eba-default-rtdb.firebaseio.com/'})
    firebase_db = db.reference()

    lock = PasswordLock(firebase_db)
    lock.root.mainloop()

    
