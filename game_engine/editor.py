import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os
import subprocess
import json

class GameEditor:
    def __init__(self, root, project_path):
        self.root = root
        self.root.title("2Darti Game Editor")
        self.root.geometry("800x600")
        self.project_path = project_path  # Path to the project

        # Canvas for the game objects
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=500)
        self.canvas.pack(pady=10)
        
        # Label to display project path
        self.project_label = tk.Label(self.root, text=f"Editing Project: {project_path}")
        self.project_label.pack()

        # Buttons at the top (OPEN PROJECT, RUN, SAVE AS .DD FILE, SETTINGS, SCRIPT)
        self.top_buttons_frame = tk.Frame(self.root)
        self.top_buttons_frame.pack(pady=10)

        # Open Project Button
        self.open_project_button = tk.Button(self.top_buttons_frame, text="Open Project", command=self.open_project)
        self.open_project_button.pack(side="left", padx=5)

        # Run Button
        self.run_button = tk.Button(self.top_buttons_frame, text="RUN", command=self.run_game)
        self.run_button.pack(side="left", padx=5)

        # Save Button
        self.save_button = tk.Button(self.top_buttons_frame, text="SAVE AS .DD FILE", command=self.save_game)
        self.save_button.pack(side="left", padx=5)

        # Settings Button
        self.settings_button = tk.Button(self.top_buttons_frame, text="SETTINGS", command=self.open_settings)
        self.settings_button.pack(side="left", padx=5)

        # Script Button
        self.script_button = tk.Button(self.top_buttons_frame, text="SCRIPT", command=self.open_script_editor)
        self.script_button.pack(side="left", padx=5)

        # Add Object Button
        self.add_object_button = tk.Button(self.root, text="Add Object", command=self.open_add_object_window)
        self.add_object_button.pack(pady=20)

        # Add Text Button
        self.add_text_button = tk.Button(self.root, text="Add Text", command=self.open_add_text_window)
        self.add_text_button.pack(pady=5)

        # Edit Object Button
        self.edit_object_button = tk.Button(self.root, text="Edit Object", command=self.open_edit_object_window)
        self.edit_object_button.pack(pady=5)

        # Delete Object Button
        self.delete_object_button = tk.Button(self.root, text="Delete Object", command=self.delete_object)
        self.delete_object_button.pack(pady=5)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_editor)
        self.exit_button.pack(pady=5)

        # List of objects on the canvas
        self.objects = []  # Will hold all objects on the canvas (rectangles, circles, texts)
        self.selected_object = None  # Track the currently selected object for movement or editing
        
        # Bind the canvas mouse events
        self.canvas.bind("<Button-1>", self.select_object)
        self.canvas.bind("<B1-Motion>", self.move_object)

    def open_project(self):
        """ Open an existing project """
        project_path = filedialog.askdirectory(title="Select Project Folder")
        
        if not project_path:
            return
        
        if not os.path.exists(project_path):
            messagebox.showerror("Error", "Project folder does not exist.")
            return
        
        try:
            # Assuming the project data is stored as a .dd file inside the project folder
            project_data_file = os.path.join(project_path, "project.dd")
            
            if not os.path.exists(project_data_file):
                messagebox.showerror("Error", "Project data file (project.dd) not found.")
                return
            
            # Load the project data (this function would read the .dd file)
            project_data = self.load_project_data(project_data_file)
            
            # Open the editor window with the loaded project data
            self.open_editor_window(project_path, project_data)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open project: {str(e)}")

    def run_game(self):
        """ Run the game by executing the script associated with the project """
        # Assuming the script is named 'game.py' and is located in the project folder
        script_path = os.path.join(self.project_path, "game.py")
        
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Game script not found: {script_path}")
            return
        
        try:
            # Run the script using subprocess
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run the game: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def save_game(self):
        """ Save the current game state to a .dd file """
        file_path = filedialog.asksaveasfilename(defaultextension=".dd", filetypes=[("Game Files", "*.dd")])
        if file_path:
            try:
                # Assuming `self.objects` contains the game data (objects, positions, etc.)
                game_data = {
                    "objects": self.objects
                }
                
                with open(file_path, 'w') as f:
                    json.dump(game_data, f, indent=4)
                messagebox.showinfo("Save Game", f"Game saved as: {file_path}")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the game: {e}")

    def open_settings(self):
        """ Placeholder function for settings """
        messagebox.showinfo("Settings", "Settings (this is just a placeholder).")
        
    def open_script_editor(self):
        """ Open the script editor where the user can write code """
        self.script_editor_window = tk.Toplevel(self.root)
        self.script_editor_window.title("Script Editor")
        self.script_editor_window.geometry("600x400")
        
        self.script_text = tk.Text(self.script_editor_window, wrap=tk.WORD, height=20, width=60)
        self.script_text.pack(padx=10, pady=10)
        
        save_button = tk.Button(self.script_editor_window, text="Save Script", command=self.save_script)
        save_button.pack(pady=10)

    def save_script(self):
        """ Save the script written in the script editor """
        script_content = self.script_text.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(script_content)
            messagebox.showinfo("Save Script", f"Script saved as: {file_path}")

    def open_add_object_window(self):
        """ Open a window to add a new object (rectangle) to the canvas """
        self.add_object_window = tk.Toplevel(self.root)
        self.add_object_window.title("Add New Object")
        
        # Name Entry
        tk.Label(self.add_object_window, text="Name:").pack()
        self.object_name = tk.Entry(self.add_object_window)
        self.object_name.pack()
        
        # Shape Selection
        tk.Label(self.add_object_window, text="Shape:").pack()
        self.shape_var = tk.StringVar(value="Rectangle")
        self.shape_menu = tk.OptionMenu(self.add_object_window, self.shape_var, "Rectangle", "Circle")
        self.shape_menu.pack()

        # Color Selection
        tk.Label(self.add_object_window, text="Color:").pack()
        self.color_var = tk.StringVar(value="blue")
        self.color_menu = tk.OptionMenu(self.add_object_window, self.color_var, "blue", "red", "green", "yellow", "black")
        self.color_menu.pack()

        # Width and Height for shape dimensions
        tk.Label(self.add_object_window, text="Width:").pack()
        self.width_entry = tk.Entry(self.add_object_window)
        self.width_entry.pack()

        tk.Label(self.add_object_window, text="Height:").pack()
        self.height_entry = tk.Entry(self.add_object_window)
        self.height_entry.pack()

        # Submit Button
        submit_button = tk.Button(self.add_object_window, text="Add", command=self.add_object)
        submit_button.pack(pady=10)

    def add_object(self):
        """ Add an object (rectangle or circle) to the canvas """
        name = self.object_name.get()
        shape = self.shape_var.get()
        color = self.color_var.get()
        
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Width and Height must be integers.")
            return
        
        if shape == "Rectangle":
            obj_id = self.canvas.create_rectangle(50, 50, 50 + width, 50 + height, fill=color)
        elif shape == "Circle":
            obj_id = self.canvas.create_oval(50, 50, 50 + width, 50 + height, fill=color)
        
        # Store the object details in the objects list
        self.objects.append({
            "name": name,
            "id": obj_id,
            "shape": shape,
            "color": color,
            "width": width,
            "height": height
        })
        
        messagebox.showinfo("Success", f"Object '{name}' added!")
        self.add_object_window.destroy()

    def open_add_text_window(self):
        """ Open a window to add a new text object to the canvas """
        self.add_text_window = tk.Toplevel(self.root)
        self.add_text_window.title("Add Text Object")
        
        # Text Entry
        tk.Label(self.add_text_window, text="Text:").pack()
        self.text_entry = tk.Entry(self.add_text_window)
        self.text_entry.pack()

        # Text Color Selection
        tk.Label(self.add_text_window, text="Color:").pack()
        self.text_color_var = tk.StringVar(value="black")
        self.text_color_menu = tk.OptionMenu(self.add_text_window, self.text_color_var, "black", "blue", "red", "green")
        self.text_color_menu.pack()

        # Submit Button
        submit_button = tk.Button(self.add_text_window, text="Add Text", command=self.add_text)
        submit_button.pack(pady=10)

    def add_text(self):
        """ Add text to the canvas """
        text = self.text_entry.get()
        color = self.text_color_var.get()
        text_id = self.canvas.create_text(50, 50, text=text, fill=color)
        
        # Store the text object
        self.objects.append({
            "name": text,
            "id": text_id,
            "shape": "Text",
            "color": color
        })

        messagebox.showinfo("Success", f"Text '{text}' added to the canvas!")
        self.add_text_window.destroy()

    def open_edit_object_window(self):
        """ Open a window to edit the selected object's properties """
        if self.selected_object is None:
            messagebox.showwarning("Edit Object", "No object selected.")
            return
        
        # Find the selected object by ID
        selected_obj = next((obj for obj in self.objects if obj["id"] == self.selected_object), None)
        
        if selected_obj is None:
            messagebox.showwarning("Edit Object", "Object not found.")
            return
        
        self.edit_object_window = tk.Toplevel(self.root)
        self.edit_object_window.title("Edit Object")
        
        # Name Entry
        tk.Label(self.edit_object_window, text="Name:").pack()
        self.edit_name_entry = tk.Entry(self.edit_object_window)
        self.edit_name_entry.insert(0, selected_obj["name"])
        self.edit_name_entry.pack()

        # Color Selection
        tk.Label(self.edit_object_window, text="Color:").pack()
        self.edit_color_var = tk.StringVar(value=selected_obj["color"])
        self.edit_color_menu = tk.OptionMenu(self.edit_object_window, self.edit_color_var, "black", "blue", "red", "green")
        self.edit_color_menu.pack()

        # Width and Height for shape dimensions (only for rectangle/circle)
        if selected_obj["shape"] in ["Rectangle", "Circle"]:
            tk.Label(self.edit_object_window, text="Width:").pack()
            self.edit_width_entry = tk.Entry(self.edit_object_window)
            self.edit_width_entry.insert(0, selected_obj["width"])
            self.edit_width_entry.pack()

            tk.Label(self.edit_object_window, text="Height:").pack()
            self.edit_height_entry = tk.Entry(self.edit_object_window)
            self.edit_height_entry.insert(0, selected_obj["height"])
            self.edit_height_entry.pack()

        # Submit Button
        submit_button = tk.Button(self.edit_object_window, text="Save Changes", command=self.save_object_changes)
        submit_button.pack(pady=10)

    def save_object_changes(self):
        """ Save changes made to an object """
        new_name = self.edit_name_entry.get()
        new_color = self.edit_color_var.get()
        
        try:
            new_width = int(self.edit_width_entry.get()) if self.edit_width_entry.get() else None
            new_height = int(self.edit_height_entry.get()) if self.edit_height_entry.get() else None
        except ValueError:
            messagebox.showerror("Error", "Width and Height must be integers.")
            return
        
        # Update object properties
        selected_obj = next((obj for obj in self.objects if obj["id"] == self.selected_object), None)
        
        if selected_obj:
            selected_obj["name"] = new_name
            selected_obj["color"] = new_color
            if new_width and new_height:
                selected_obj["width"] = new_width
                selected_obj["height"] = new_height
                # Update object on canvas (for rectangle/circle)
                if selected_obj["shape"] == "Rectangle":
                    self.canvas.coords(selected_obj["id"], 50, 50, 50 + new_width, 50 + new_height)
                elif selected_obj["shape"] == "Circle":
                    self.canvas.coords(selected_obj["id"], 50, 50, 50 + new_width, 50 + new_height)
            
            messagebox.showinfo("Edit Object", "Object updated successfully!")
            self.edit_object_window.destroy()
        else:
            messagebox.showwarning("Edit Object", "Selected object not found.")
    
    def delete_object(self):
        """ Delete the selected object from the canvas """
        if self.selected_object is not None:
            self.canvas.delete(self.selected_object)
            self.objects = [obj for obj in self.objects if obj["id"] != self.selected_object]
            self.selected_object = None
            messagebox.showinfo("Delete Object", "Object deleted.")
        else:
            messagebox.showwarning("Delete Object", "No object selected.")
    
    def select_object(self, event):
        """ Select an object on the canvas """
        self.selected_object = self.canvas.find_closest(event.x, event.y)[0]

    def move_object(self, event):
        """ Move the selected object on the canvas """
        if self.selected_object is not None:
            self.canvas.coords(self.selected_object, event.x - 50, event.y - 50, event.x + 50, event.y + 50)

    def exit_editor(self):
        """ Exit the editor """
        self.root.quit()
