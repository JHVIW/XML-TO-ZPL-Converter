import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText
import xml.etree.ElementTree as ET
import requests
from io import BytesIO
from PIL import Image, ImageTk, ImageDraw
import os

# File to save the XML data
XML_FILE = "saved_xml.txt"

# Global variables
throttle_id = None
grid_visible = False  # Track grid visibility
original_image = None  # Store the original PIL image
image_with_grid = None  # Store the PIL image with the grid

def parse_xml_to_zpl(xml_string):
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()

    zpl_lines = []
    zpl_lines.append("^XA")  # Start of ZPL command

    for elem in root:
        if elem.tag == "TEXT":
            zpl_lines.append(handle_text_element(elem))
        elif elem.tag == "BARCODE":
            zpl_lines.append(handle_barcode_element(elem))

    zpl_lines.append("^XZ")  # End of ZPL command
    return "\n".join(zpl_lines)

def handle_text_element(elem):
    origin_x = elem.attrib.get("originX", "0")
    origin_y = elem.attrib.get("originY", "0")
    font = elem.attrib.get("font", "A")
    height = elem.attrib.get("heightmagnification", "1")
    width = elem.attrib.get("widthmagnification", "1")
    rotation = elem.attrib.get("rotation", "N")  # Handle rotation
    text = elem.text if elem.text else f"^FN{elem.attrib.get('name', '0')}"
    zpl = f"^FO{origin_x},{origin_y}^A{font},{rotation},{height},{width}^FD{text}^FS"
    return zpl

def handle_barcode_element(elem):
    origin_x = elem.attrib.get("originX", "0")
    origin_y = elem.attrib.get("originY", "0")
    barcode_type = elem.attrib.get("barcodetype", "BC-CODE39").replace("BC-", "")
    width = elem.attrib.get("barcodewidth", "1")
    ratio = elem.attrib.get("barcoderatio", "1")
    height = elem.attrib.get("heightmagnification", "50")
    add_check_digit = elem.attrib.get("addcheckdigit", "N")
    rotation = elem.attrib.get("rotation", "N")  # Handle rotation
    zpl = f"^FO{origin_x},{origin_y}^BY{width},{ratio}^B{barcode_type}{rotation},{height},{add_check_digit}^FN{elem.attrib.get('name', '0')}^FS"
    return zpl

def fetch_preview():
    xml_input = xml_text.get("1.0", tk.END).strip()
    if xml_input:
        try:
            zpl_output = parse_xml_to_zpl(xml_input)
            render_zpl(zpl_output)
        except Exception as e:
            # Handle parsing errors gracefully
            preview_label.config(text=f"Error: {str(e)}", image='')
    else:
        preview_label.config(text="No XML content to preview.", image='')

def render_zpl(zpl):
    global original_image, image_with_grid
    url = "http://api.labelary.com/v1/printers/8dpmm/labels/3.94x3.94/0/"
    files = {'file': zpl}
    headers = {"Accept": "image/png"}

    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        original_image = Image.open(image_data)
        original_image.thumbnail((800, 800))  # Resize the image to fit in the preview
        image_with_grid = original_image.copy()  # Create a copy of the original image for grid overlay
        photo = ImageTk.PhotoImage(original_image)
        preview_label.config(image=photo)
        preview_label.image = photo
        if grid_visible:
            draw_grid_overlay()  # Draw grid overlay on the image
    else:
        preview_label.config(text=f"Error: Unable to render ZPL (status code: {response.status_code})", image='')

def draw_grid_overlay():
    global image_with_grid
    if original_image:
        draw = ImageDraw.Draw(image_with_grid)
        width, height = image_with_grid.size
        # Draw the horizontal and vertical lines
        draw.line([(width / 2, 0), (width / 2, height)], fill="red", width=2)
        draw.line([(0, height / 2), (width, height / 2)], fill="red", width=2)
        photo_with_grid = ImageTk.PhotoImage(image_with_grid)
        preview_label.config(image=photo_with_grid)
        preview_label.image = photo_with_grid

def toggle_grid():
    global grid_visible
    grid_visible = not grid_visible
    if grid_visible:
        draw_grid_overlay()  # Redraw grid overlay on the current image
    else:
        # Show the original image without grid
        if original_image:
            photo = ImageTk.PhotoImage(original_image)
            preview_label.config(image=photo)
            preview_label.image = photo

def find_text(event=None):
    search_query = simpledialog.askstring("Find", "Enter text to search:")
    if search_query:
        start_idx = xml_text.search(search_query, "1.0", tk.END)
        if start_idx:
            end_idx = f"{start_idx}+{len(search_query)}c"
            xml_text.tag_add("highlight", start_idx, end_idx)
            xml_text.tag_config("highlight", background="yellow", foreground="black")
            xml_text.mark_set(tk.INSERT, end_idx)
            xml_text.see(tk.INSERT)
        else:
            messagebox.showinfo("Find", "Text not found.")

def save_xml():
    save_xml_to_file()
    messagebox.showinfo("Save", "XML content saved successfully.")

def quit_program():
    save_xml_to_file()  # Save the XML data to a file before quitting
    root.destroy()

def save_xml_to_file():
    with open(XML_FILE, "w") as file:
        file.write(xml_text.get("1.0", tk.END))

def load_xml_from_file():
    if os.path.exists(XML_FILE):
        with open(XML_FILE, "r") as file:
            xml_content = file.read()
            xml_text.delete("1.0", tk.END)
            xml_text.insert(tk.END, xml_content)
            if xml_content.strip():  # Fetch preview only if there's content
                fetch_preview()

def on_text_change(event=None):
    global throttle_id
    if throttle_id is not None:
        root.after_cancel(throttle_id)
    throttle_id = root.after(500, fetch_preview)  # Throttle requests to every 500ms

root = tk.Tk()
root.title("XML to ZPL Converter with Preview")

# Make the window fullscreen
root.attributes('-fullscreen', True)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Top control frame with buttons
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X)

# Exit button
exit_button = tk.Button(control_frame, text="Exit", command=quit_program)
exit_button.pack(side=tk.RIGHT)

# Grid toggle button
toggle_grid_button = tk.Button(control_frame, text="Toggle Grid", command=toggle_grid)
toggle_grid_button.pack(side=tk.RIGHT)

# Save button
save_button = tk.Button(control_frame, text="Save", command=save_xml)
save_button.pack(side=tk.RIGHT)

# XML input on the left
xml_text = ScrolledText(main_frame, height=20)
xml_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
xml_text.bind("<KeyRelease>", on_text_change)  # Bind text changes to the function

# ZPL preview on the right
preview_label = tk.Label(main_frame)
preview_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Load XML data and update preview on startup
load_xml_from_file()

# Bind Ctrl+F to find_text function
root.bind("<Control-f>", find_text)
# Bind Ctrl+S to save_xml function
root.bind("<Control-s>", lambda event: save_xml())

root.mainloop()
