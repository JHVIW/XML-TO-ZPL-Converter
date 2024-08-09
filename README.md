
# XML to ZPL Converter with Preview

This is a Python-based GUI application that allows users to convert XML data to ZPL (Zebra Programming Language) and preview the output. The application is built using Tkinter for the GUI, PIL (Pillow) for image handling, and requests for interacting with the Labelary API to render the ZPL preview.

## Features

- **XML to ZPL Conversion**: Parse XML input to generate corresponding ZPL commands.
- **ZPL Preview**: Visualize the generated ZPL as an image using the Labelary API.
- **Grid Overlay**: Toggle a red grid overlay on the ZPL preview for easier positioning.
- **Find and Highlight Text**: Search for specific text within the XML input and highlight occurrences.
- **Auto-Preview**: Automatically update the ZPL preview as you edit the XML.
- **Fullscreen Mode**: The application runs in fullscreen mode for better visibility and user experience.
- **Save and Load XML**: Save your XML input to a file and load it automatically on startup.

## Installation

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/JHVIW/XML-TO-ZPL.git](https://github.com/JHVIW/XML-TO-ZPL-Converter.git)
   cd xml-to-zpl-converter
   ```

2. **Install Dependencies**
   Ensure you have Python 3.x installed. Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should contain:
   ```
   requests
   Pillow
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## Usage

- **XML Input**: Enter or paste your XML data into the left pane.
- **ZPL Preview**: The right pane displays the ZPL preview. The preview updates automatically as you edit the XML.
- **Save XML**: Save your current XML input by clicking the "Save" button or pressing `Ctrl+S`.
- **Toggle Grid**: Click the "Toggle Grid" button to overlay a red grid on the preview image.
- **Find Text**: Press `Ctrl+F` to search for text within the XML input.
- **Exit**: Exit the application by clicking the "Exit" button.

## XML Structure

The XML should follow a specific structure for the conversion to work correctly. Here is an example:

```xml
<root>
    <TEXT originX="100" originY="200" font="A" heightmagnification="10" widthmagnification="10" rotation="N">Sample Text</TEXT>
    <BARCODE originX="300" originY="400" barcodetype="BC-CODE39" barcodewidth="2" barcoderatio="3" heightmagnification="100" addcheckdigit="N" rotation="N">123456</BARCODE>
</root>
```

- **TEXT**: Represents a text element.
- **BARCODE**: Represents a barcode element.

## API Integration

The application uses the [Labelary API](http://labelary.com/service.html) to convert ZPL into a preview image. Make sure you have an active internet connection when running the application.

## Notes

- The application automatically saves your XML input to a file (`saved_xml.txt`) upon exiting. This file is loaded back into the application when you start it again.
- The grid overlay is a helpful feature to assist in designing and aligning elements within the ZPL preview.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
