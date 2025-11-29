import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
import requests
import json



class TokenManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Okta Token Manager")
        self.root.geometry("1000x900")
        self.root.minsize(900, 800)

        # Configure style
        self.configure_styles()

        self.tokens = []
        self.current_file = None

        self.create_widgets()
        self.setup_layout()

    def configure_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors - Professional gradient background colors
        self.primary_color = '#2c3e50'
        self.secondary_color = '#3498db'
        self.success_color = '#27ae60'
        self.warning_color = '#f39c12'
        self.danger_color = '#e74c3c'
        self.light_bg = '#f8f9fa'
        self.dark_bg = '#34495e'
        self.accent_color = '#2980b9'
        self.sidebar_color = '#2c3e50'

        # Configure main background
        style.configure('Main.TFrame', background=self.light_bg)
        style.configure('Sidebar.TFrame', background=self.sidebar_color)
        style.configure('Header.TFrame', background=self.dark_bg)

        # Configure labels
        style.configure('Header.TLabel', background=self.dark_bg, foreground='white',
                        font=('Segoe UI', 10, 'bold'))
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'),
                        foreground=self.primary_color, background=self.light_bg)
        style.configure('Light.TLabel', background=self.light_bg, foreground=self.primary_color)

        # Configure button styles
        style.configure('Primary.TButton', background=self.secondary_color, foreground='white',
                        borderwidth=0, focuscolor='none', font=('Segoe UI', 9, 'bold'))
        style.map('Primary.TButton',
                  background=[('active', '#2980b9'), ('pressed', '#21618c')])

        style.configure('Success.TButton', background=self.success_color, foreground='white',
                        font=('Segoe UI', 9, 'bold'))
        style.map('Success.TButton',
                  background=[('active', '#229954'), ('pressed', '#1e8449')])

        style.configure('Warning.TButton', background=self.warning_color, foreground='white',
                        font=('Segoe UI', 9, 'bold'))
        style.map('Warning.TButton',
                  background=[('active', '#e67e22'), ('pressed', '#ca6f1e')])

        style.configure('Danger.TButton', background=self.danger_color, foreground='white',
                        font=('Segoe UI', 9, 'bold'))
        style.map('Danger.TButton',
                  background=[('active', '#cb4335'), ('pressed', '#a93226')])

        # Configure labelframe styles
        style.configure('Custom.TLabelframe', background=self.light_bg, bordercolor='#bdc3c7')
        style.configure('Custom.TLabelframe.Label', background=self.light_bg,
                        foreground=self.primary_color, font=('Segoe UI', 10, 'bold'))

    def create_widgets(self):
        # Create main container with modern styling
        main_container = ttk.Frame(self.root, style='Main.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header with gradient effect
        header_frame = ttk.Frame(main_container, style='Header.TFrame', height=70)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        # Smaller font for the title (changed from 18 to 14)
        title_label = ttk.Label(header_frame, text="🔐 Okta Token Manager",
                                style='Header.TLabel', font=('Segoe UI', 14, 'bold'))
        title_label.pack(side=tk.LEFT, padx=25, pady=20)

        # Status label
        self.status_label = ttk.Label(header_frame, text="🚀 Ready", style='Header.TLabel',
                                      font=('Segoe UI', 10))
        self.status_label.pack(side=tk.RIGHT, padx=25, pady=20)

        # Content container
        content_container = ttk.Frame(main_container, style='Main.TFrame')
        content_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Configuration section
        self.create_config_section(content_container)

        # Actions section with centered buttons - ALL IN ONE ROW
        self.create_actions_section(content_container)

        # Data section
        self.create_data_section(content_container)

    def create_config_section(self, parent):
        config_frame = ttk.LabelFrame(parent, text="⚙️ Okta Configuration",
                                      padding=15, style='Custom.TLabelframe')
        config_frame.pack(fill=tk.X, pady=(0, 15))

        # Portal configuration
        portal_row = ttk.Frame(config_frame, style='Main.TFrame')
        portal_row.pack(fill=tk.X, pady=8)

        ttk.Label(portal_row, text="Portal URL:", width=15, anchor=tk.W,
                  style='Light.TLabel').pack(side=tk.LEFT)
        self.portal_entry = ttk.Entry(portal_row, font=('Segoe UI', 10))
        self.portal_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))
        self.portal_entry.insert(0, "https://trial-6581012.okta.com/api/v1/users/")

        # API Token
        token_row = ttk.Frame(config_frame, style='Main.TFrame')
        token_row.pack(fill=tk.X, pady=8)

        ttk.Label(token_row, text="API Token:", width=15, anchor=tk.W,
                  style='Light.TLabel').pack(side=tk.LEFT)
        self.token_entry = ttk.Entry(token_row, show="•", font=('Segoe UI', 10))
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))

        # Authenticator ID
        auth_row = ttk.Frame(config_frame, style='Main.TFrame')
        auth_row.pack(fill=tk.X, pady=8)

        ttk.Label(auth_row, text="Authenticator ID:", width=15, anchor=tk.W,
                  style='Light.TLabel').pack(side=tk.LEFT)
        self.authenticator_entry = ttk.Entry(auth_row, font=('Segoe UI', 10))
        self.authenticator_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))
        self.authenticator_entry.insert(0, "autxrdb3e8EPwTYQM697")

        # Test connection button - centered
        test_container = ttk.Frame(config_frame, style='Main.TFrame')
        test_container.pack(fill=tk.X, pady=(10, 0))

        test_btn = ttk.Button(test_container, text="🔍 Test Connection",
                              command=self.test_connection, style='Primary.TButton',
                              width=20)
        test_btn.pack(pady=5)

    def create_actions_section(self, parent):
        actions_frame = ttk.LabelFrame(parent, text="🚀 Actions", padding=20,
                                       style='Custom.TLabelframe')
        actions_frame.pack(fill=tk.X, pady=(0, 15))

        # Main button container for centering - ALL BUTTONS IN ONE ROW
        main_button_container = ttk.Frame(actions_frame, style='Main.TFrame')
        main_button_container.pack(expand=True)

        # ALL BUTTONS IN ONE ROW
        button_row = ttk.Frame(main_button_container, style='Main.TFrame')
        button_row.pack(pady=5)

        # Define all buttons in order with their styles
        buttons = [
            ("📁 Load CSV", self.load_csv_file, 'Primary.TButton'),
            ("🆔 Get User IDs", self.get_okta_user_ids, 'Primary.TButton'),
            ("👥 Get Users", self.get_okta_users, 'Primary.TButton'),
            ("➕ Add Factors", self.add_factors_to_users, 'Success.TButton'),
            ("🗑️ Clear Data", self.clear_data, 'Danger.TButton'),
            ("📋 Clear Details", self.clear_details, 'Warning.TButton'),
        ]

        # Create all buttons in one row
        for text, command, style_name in buttons:
            btn = ttk.Button(button_row, text=text, command=command, style=style_name, width=15)
            btn.pack(side=tk.LEFT, padx=6, pady=5)

    def create_data_section(self, parent):
        # Create notebook for tabs with better styling
        notebook_style = ttk.Style()
        notebook_style.configure('TNotebook', background=self.light_bg, borderwidth=0)
        notebook_style.configure('TNotebook.Tab', background='#ecf0f1', foreground=self.primary_color,
                                 padding=[15, 5], font=('Segoe UI', 9, 'bold'))
        notebook_style.map('TNotebook.Tab', background=[('selected', self.secondary_color),
                                                        ('active', '#2980b9')],
                           foreground=[('selected', 'white')])

        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Tokens tab
        tokens_tab = ttk.Frame(notebook, padding=15, style='Main.TFrame')
        notebook.add(tokens_tab, text="📊 Token Data")

        # File info with better styling
        info_container = ttk.Frame(tokens_tab, style='Main.TFrame')
        info_container.pack(fill=tk.X, pady=(0, 15))

        self.info_label = ttk.Label(info_container, text="📋 No file loaded",
                                    style='Title.TLabel', font=('Segoe UI', 11))
        self.info_label.pack(anchor=tk.W)

        # Table with scrollbars
        table_frame = ttk.Frame(tokens_tab, style='Main.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview with better styling
        columns = ('email', 'serial', 'secret_key', 'interval', 'manufacturer', 'model')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        # Configure headers with better styling
        headers = {
            'email': '📧 Email Address',
            'serial': '🔢 Serial Number',
            'secret_key': '🔑 Secret Key',
            'interval': '⏱️ Interval',
            'manufacturer': '🏭 Manufacturer',
            'model': '📱 Model'
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text)

        # Configure column widths
        self.tree.column('email', width=200, minwidth=150)
        self.tree.column('serial', width=130, minwidth=100)
        self.tree.column('secret_key', width=220, minwidth=150)
        self.tree.column('interval', width=90, minwidth=60)
        self.tree.column('manufacturer', width=130, minwidth=100)
        self.tree.column('model', width=130, minwidth=100)

        # Style the treeview
        style = ttk.Style()
        style.configure('Treeview', background='white', fieldbackground='white',
                        foreground=self.primary_color, rowheight=25)
        style.configure('Treeview.Heading', background='#ecf0f1', foreground=self.primary_color,
                        font=('Segoe UI', 9, 'bold'))
        style.map('Treeview.Heading', background=[('active', '#bdc3c7')])

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid layout for table and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Details tab
        details_tab = ttk.Frame(notebook, padding=15, style='Main.TFrame')
        notebook.add(details_tab, text="📝 Operation Details")

        # Details text area with better styling
        detail_label = ttk.Label(details_tab, text="🔍 Operation Details:",
                                 style='Title.TLabel', font=('Segoe UI', 11))
        detail_label.pack(anchor=tk.W, pady=(0, 10))

        detail_container = ttk.Frame(details_tab, style='Main.TFrame')
        detail_container.pack(fill=tk.BOTH, expand=True)

        self.detail_text = tk.Text(detail_container, wrap=tk.WORD, font=('Consolas', 10),
                                   bg='#ffffff', fg='#2c3e50', relief=tk.FLAT,
                                   borderwidth=1, padx=12, pady=12, highlightthickness=1,
                                   highlightbackground='#bdc3c7', highlightcolor=self.secondary_color)

        detail_v_scrollbar = ttk.Scrollbar(detail_container, orient=tk.VERTICAL, command=self.detail_text.yview)
        detail_h_scrollbar = ttk.Scrollbar(detail_container, orient=tk.HORIZONTAL, command=self.detail_text.xview)
        self.detail_text.configure(yscrollcommand=detail_v_scrollbar.set,
                                   xscrollcommand=detail_h_scrollbar.set)

        self.detail_text.grid(row=0, column=0, sticky='nsew')
        detail_v_scrollbar.grid(row=0, column=1, sticky='ns')
        detail_h_scrollbar.grid(row=1, column=0, sticky='ew')
        detail_container.grid_rowconfigure(0, weight=1)
        detail_container.grid_columnconfigure(0, weight=1)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_token_select)

    def setup_layout(self):
        """Setup grid weights for proper resizing"""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def update_status(self, message, status_type="info"):
        """Update status label with colored message"""
        colors = {
            "info": '#ffffff',
            "success": '#2ecc71',
            "warning": '#f1c40f',
            "error": '#e74c3c'
        }
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        self.status_label.config(
            text=f"{icons.get(status_type, 'ℹ️')} {message}",
            foreground=colors.get(status_type, '#ffffff')
        )

    def clear_details(self):
        """Clear the detailed information text area"""
        self.detail_text.delete(1.0, tk.END)
        self.update_status("Details cleared", "info")

    def test_connection(self):
        """Test connection to Okta API"""
        portal_link = self.portal_entry.get().strip()
        api_token = self.token_entry.get().strip()

        if not portal_link:
            messagebox.showerror("Error", "Please enter a portal link")
            return

        if not api_token:
            messagebox.showerror("Error", "Please enter an API token")
            return

        self.update_status("Testing connection...", "info")

        try:
            headers = {
                'Authorization': f'SSWS {api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            response = requests.get(portal_link, headers=headers, timeout=10)

            if response.status_code == 200:
                self.update_status("Connection successful!", "success")
                messagebox.showinfo("Success", "✅ Connection successful! API is accessible.")
            else:
                self.update_status("Connection failed", "error")
                messagebox.showerror("Error",
                                     f"❌ Connection failed. Status code: {response.status_code}\nResponse: {response.text}")

        except requests.exceptions.RequestException as e:
            self.update_status("Connection error", "error")
            messagebox.showerror("Error", f"❌ Connection error: {str(e)}")

    def get_okta_user_id(self, email):
        """Get Okta user ID based on email address"""
        portal_link = self.portal_entry.get().strip()
        api_token = self.token_entry.get().strip()

        if not portal_link or not api_token:
            return None

        try:
            headers = {
                'Authorization': f'SSWS {api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            # Search for user by email
            search_url = f"{portal_link}?search=profile.login eq \"{email}\""
            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                users = response.json()
                if users and len(users) > 0:
                    return users[0].get('id')

            return None

        except requests.exceptions.RequestException:
            return None

    def get_okta_user_ids(self):
        """Get Okta user IDs for all emails in the loaded CSV"""
        if not self.tokens:
            messagebox.showerror("Error", "Please load a CSV file first")
            return

        portal_link = self.portal_entry.get().strip()
        api_token = self.token_entry.get().strip()

        if not portal_link:
            messagebox.showerror("Error", "Please enter a portal link")
            return

        if not api_token:
            messagebox.showerror("Error", "Please enter an API token")
            return

        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, "🔍 Fetching user IDs from Okta...\n\n")
        self.update_status("Fetching user IDs...", "info")

        success_count = 0
        error_count = 0

        for token in self.tokens:
            email = token['upn']
            self.detail_text.insert(tk.END, f"Searching for: {email}... ")

            user_id = self.get_okta_user_id(email)

            if user_id:
                self.detail_text.insert(tk.END, f"✅ Found - ID: {user_id}\n")
                success_count += 1
            else:
                self.detail_text.insert(tk.END, "❌ Not found\n")
                error_count += 1

        self.detail_text.insert(tk.END, f"\n--- 📊 Summary ---\n")
        self.detail_text.insert(tk.END, f"✅ Successful: {success_count}\n")
        self.detail_text.insert(tk.END, f"❌ Not found: {error_count}\n")
        self.detail_text.insert(tk.END, f"📋 Total: {len(self.tokens)}")

        self.update_status(f"User ID lookup completed - Found: {success_count}", "success")
        messagebox.showinfo("Complete",
                            f"User ID lookup completed!\n✅ Found: {success_count}\n❌ Not found: {error_count}")

    def add_factor_to_user(self, user_id, token_data):
        """Add factor to specific user"""
        portal_link = self.portal_entry.get().strip()
        api_token = self.token_entry.get().strip()
        authenticator_id = self.authenticator_entry.get().strip()

        if not portal_link or not api_token or not authenticator_id:
            return False, "Missing configuration"

        try:
            headers = {
                'Authorization': f'SSWS {api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            # Construct the URL for adding factors
            factors_url = f"{portal_link}{user_id}/factors?activate=true"

            # Prepare the request body
            request_body = {
                "factorType": "token:hotp",
                "factorProfileId": authenticator_id,
                "provider": "CUSTOM",
                "profile": {
                    "credentialId": token_data['upn'],
                    "sharedSecret": token_data['secret_key'],
                    "timeStep": int(token_data['timeinterval']),
                    "keyLength": 6,
                    "algorithm": "SHA1"
                }
            }

            response = requests.post(factors_url, headers=headers, json=request_body, timeout=10)

            if response.status_code == 200:
                return True, "Factor added successfully"
            else:
                return False, f"HTTP {response.status_code}: {response.text}"

        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}"

    def add_factors_to_users(self):
        """Add factors to all users based on CSV data"""
        if not self.tokens:
            messagebox.showerror("Error", "Please load a CSV file first")
            return

        portal_link = self.portal_entry.get().strip()
        api_token = self.token_entry.get().strip()
        authenticator_id = self.authenticator_entry.get().strip()

        if not portal_link:
            messagebox.showerror("Error", "Please enter a portal link")
            return

        if not api_token:
            messagebox.showerror("Error", "Please enter an API token")
            return

        if not authenticator_id:
            messagebox.showerror("Error", "Please enter an Authenticator ID")
            return

        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, "➕ Adding factors to users...\n\n")
        self.update_status("Adding factors to users...", "info")

        success_count = 0
        error_count = 0

        for token in self.tokens:
            email = token['upn']
            self.detail_text.insert(tk.END, f"Processing: {email}... ")

            # First get user ID
            user_id = self.get_okta_user_id(email)

            if user_id:
                # Add factor to user
                success, message = self.add_factor_to_user(user_id, token)
                if success:
                    self.detail_text.insert(tk.END, f"✅ SUCCESS - Factor added\n")
                    success_count += 1
                else:
                    self.detail_text.insert(tk.END, f"❌ FAILED - {message}\n")
                    error_count += 1
            else:
                self.detail_text.insert(tk.END, "❌ FAILED - User not found in Okta\n")
                error_count += 1

        self.detail_text.insert(tk.END, f"\n--- 📊 Summary ---\n")
        self.detail_text.insert(tk.END, f"✅ Successful: {success_count}\n")
        self.detail_text.insert(tk.END, f"❌ Failed: {error_count}\n")
        self.detail_text.insert(tk.END, f"📋 Total: {len(self.tokens)}")

        self.update_status(f"Factor addition completed - Successful: {success_count}", "success")
        messagebox.showinfo("Complete",
                            f"Factor addition completed!\n✅ Successful: {success_count}\n❌ Failed: {error_count}")

    def get_okta_users(self):
        """Get users from Okta API"""
        portal_link = self.portal_entry.get().strip()
        api_token = self.token_entry.get().strip()

        if not portal_link:
            messagebox.showerror("Error", "Please enter a portal link")
            return

        if not api_token:
            messagebox.showerror("Error", "Please enter an API token")
            return

        try:
            headers = {
                'Authorization': f'SSWS {api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, "👥 Fetching users from Okta...\n")
            self.update_status("Fetching users from Okta...", "info")

            response = requests.get(portal_link, headers=headers, timeout=10)

            if response.status_code == 200:
                users = response.json()
                self.display_okta_users(users)
                self.update_status(f"Retrieved {len(users)} users", "success")
                messagebox.showinfo("Success", f"✅ Successfully retrieved {len(users)} users from Okta")
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                self.detail_text.insert(tk.END, error_msg)
                self.update_status("Failed to get users", "error")
                messagebox.showerror("Error", f"❌ Failed to get users. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            self.detail_text.insert(tk.END, error_msg)
            self.update_status("Connection error", "error")
            messagebox.showerror("Error", error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"JSON decode error: {str(e)}"
            self.detail_text.insert(tk.END, error_msg)
            self.update_status("JSON error", "error")
            messagebox.showerror("Error", error_msg)

    def display_okta_users(self, users):
        """Display Okta users in the detail text area"""
        self.detail_text.delete(1.0, tk.END)

        if not users:
            self.detail_text.insert(tk.END, "❌ No users found in the response.")
            return

        self.detail_text.insert(tk.END, f"✅ Found {len(users)} users:\n\n")

        for i, user in enumerate(users, 1):
            self.detail_text.insert(tk.END, f"👤 User #{i}:\n")
            self.detail_text.insert(tk.END, f"  🆔 ID: {user.get('id', 'N/A')}\n")
            self.detail_text.insert(tk.END, f"  📊 Status: {user.get('status', 'N/A')}\n")

            # Extract profile information
            profile = user.get('profile', {})
            self.detail_text.insert(tk.END, f"  🔑 Login: {profile.get('login', 'N/A')}\n")
            self.detail_text.insert(tk.END, f"  📧 Email: {profile.get('email', 'N/A')}\n")
            self.detail_text.insert(tk.END, f"  👤 First Name: {profile.get('firstName', 'N/A')}\n")
            self.detail_text.insert(tk.END, f"  👥 Last Name: {profile.get('lastName', 'N/A')}\n")

            self.detail_text.insert(tk.END, "─" * 50 + "\n")

    def load_csv_file(self):
        """Load CSV file"""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            self.read_tokens_from_csv(filename)
            self.current_file = filename
            self.update_status(f"Loaded {len(self.tokens)} tokens", "success")

    def read_tokens_from_csv(self, filename):
        """Read tokens from CSV file"""
        self.tokens = []

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    self.tokens.append({
                        'upn': row['upn'],
                        'serial_number': row['serial number'],
                        'secret_key': row['secret key'],
                        'timeinterval': row['timeinterval'],
                        'manufacturer': row['manufacturer'],
                        'model': row['model']
                    })

            self.update_display()
            file_name = os.path.basename(filename)
            self.info_label.config(text=f"📊 Loaded {len(self.tokens)} tokens from: {file_name}")

        except FileNotFoundError:
            self.update_status("File not found", "error")
            messagebox.showerror("Error", f"❌ File {filename} not found")
        except Exception as e:
            self.update_status("Error reading file", "error")
            messagebox.showerror("Error", f"❌ Error reading file: {e}")

    def update_display(self):
        """Update data display in table"""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fill table with new data
        for token in self.tokens:
            self.tree.insert('', tk.END, values=(
                token['upn'],
                token['serial_number'],
                token['secret_key'],
                token['timeinterval'],
                token['manufacturer'],
                token['model']
            ))

    def on_token_select(self, event):
        """Handle token selection in table"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, 'values')

            detail_info = f"""🔍 Detailed Token Information

📧 Email: {values[0]}
🔢 Serial Number: {values[1]}
🔑 Secret Key: {values[2]}
⏱️ Time Interval: {values[3]} sec
🏭 Manufacturer: {values[4]}
📱 Model: {values[5]}
"""
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(1.0, detail_info)

    def clear_data(self):
        """Clear all data"""
        self.tokens = []
        self.current_file = None
        self.update_display()
        self.info_label.config(text="📋 No file loaded")
        self.detail_text.delete(1.0, tk.END)
        self.update_status("All data cleared", "info")
        messagebox.showinfo("Clear", "🗑️ All data cleared")


def main():
    root = tk.Tk()

    # Set window icon (if you have one)
    # root.iconbitmap('icon.ico')

    # Center the window
    root.eval('tk::PlaceWindow . center')

    app = TokenManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()