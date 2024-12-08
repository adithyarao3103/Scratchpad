import json
import os
import sys
import webview

class TextScratchpadApp:
    def __init__(self):
        exe_dir = os.path.dirname(sys.executable)
        self.config_path = os.path.join(exe_dir, 'display_config.json')
        self.load_configuration()
        
    def load_configuration(self):
        """Load display configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            self.config = {
                "font": {
                    "family": "Arial, sans-serif",
                    "size": "16px",
                    "url": ""
                },
                "editor": {
                    "backgroundColor": "#FFFFFF",
                    "textColor": "#000000",
                    "lineHeight": "1.6",
                    "letterSpacing": "0.02em",
                    "padding": "20px"
                }
            }
        
    def get_html(self):
        """Generate HTML with dynamic styling from configuration"""
        font_config = self.config.get('font', {})
        editor_config = self.config.get('editor', {})
        
        font_link = f'<link href="{font_config.get("url", "")}" rel="stylesheet">' if font_config.get("url") else ""
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Text Scratchpad</title>
            {font_link}
            <style>
                html, body {{
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    overflow: hidden;
                }}
                #editor {{
                    width: 100%;
                    height: 100%;
                    border: none;
                    outline: none;
                    resize: none;
                    font-family: {font_config.get("family", "Arial, sans-serif")};
                    font-size: {font_config.get("size", "16px")};
                    background-color: {editor_config.get("backgroundColor", "#FFFFFF")};
                    color: {editor_config.get("textColor", "#000000")};
                    line-height: {editor_config.get("lineHeight", "1.6")};
                    letter-spacing: {editor_config.get("letterSpacing", "0.02em")};
                    padding: {editor_config.get("padding", "20px")};
                    box-sizing: border-box;
                }}
            </style>
        </head>
        <body>
            <textarea id="editor" placeholder="Start typing or paste your text here..."></textarea>

            <script>

                const editor = document.getElementById('editor');
                
                editor.focus();

                document.addEventListener('keydown', (e) => {{
                    // Ctrl+W: Close window
                    if (e.ctrlKey && e.key === 'w') {{
                        e.preventDefault();
                        window.pywebview.api.quit();
                    }}
                    // Ctrl + Increase font size
                    if (e.ctrlKey && e.key === '=') {{
                        e.preventDefault();
                        const currentFontSize = parseFloat(getComputedStyle(editor).fontSize);
                        editor.style.fontSize = (currentFontSize + 1) + 'px';
                    }};

                    // Ctrl - Decrease font size
                    if (e.ctrlKey && e.key === '-') {{
                        e.preventDefault();
                        const currentFontSize = parseFloat(getComputedStyle(editor).fontSize);
                        editor.style.fontSize = (currentFontSize - 1) + 'px';
                    }}
                }});
            </script>
        </body>
        </html>
        '''

class Api:  
    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def quit(self):
        self._window.destroy()

def main():
    app = TextScratchpadApp()
    api = Api()
    
    window = webview.create_window(
        title='Scratchpad', 
        html=app.get_html(), 
        js_api=api,
        frameless=True,
        resizable=True,
        width=800,
        height=600
    )
    
    api.set_window(window)
    webview.start(debug=False)


if __name__ == '__main__':
    main()