import os
import threading
import http.server
import socketserver
import webview


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS support."""
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")  # Allow GET and OPTIONS
        self.send_header("Access-Control-Allow-Headers", "Content-Type")  # Allow Content-Type header
        super().end_headers()


class LocalHTTPServer:
    def __init__(self, directory, port=8000):
        self.directory = directory
        self.port = port

    def start(self):
        """Start the HTTP server in a separate thread"""
        handler = CORSRequestHandler
        os.chdir(self.directory)
        self.httpd = socketserver.TCPServer(("localhost", self.port), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def stop(self):
        """Stop the HTTP server"""
        self.httpd.shutdown()
        self.thread.join()


class TextScratchpadApp:
    def __init__(self, server_port):
        self.server_port = server_port

    def get_html(self):
        """Generate HTML with dynamic JavaScript fetching the configuration"""
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Text Scratchpad</title>
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
                    box-sizing: border-box;
                }}
            </style>
        </head>
        <body>
            <textarea id="editor" placeholder="Start typing or paste your text here..."></textarea>

            <script>
                async function applyConfig() {{
                    try {{
                        // Fetch the configuration JSON file from the local server
                        const response = await fetch('http://localhost:{self.server_port}/display_config.json');
                        const config = await response.json();

                        const editor = document.getElementById('editor');
                        const fontConfig = config.font || {{}};
                        const editorConfig = config.editor || {{}};

                        // Apply font settings
                        if (fontConfig.family) editor.style.fontFamily = fontConfig.family;
                        if (fontConfig.size) editor.style.fontSize = fontConfig.size;

                        // Apply editor settings
                        editor.style.backgroundColor = editorConfig.backgroundColor || '#FFFFFF';
                        editor.style.color = editorConfig.textColor || '#000000';
                        editor.style.lineHeight = editorConfig.lineHeight || '1.6';
                        editor.style.letterSpacing = editorConfig.letterSpacing || '0.02em';
                        editor.style.padding = editorConfig.padding || '20px';
                    }} catch (error) {{
                        console.error('Failed to load configuration:', error);
                    }}
                }}

                applyConfig();

                document.getElementById('editor').focus();

                document.addEventListener('keydown', (e) => {{
                    const editor = document.getElementById('editor');
                    
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
                    }}

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
    # Serve the current directory over HTTP
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_port = 8888
    server = LocalHTTPServer(directory=current_dir, port=server_port)
    server.start()

    try:
        app = TextScratchpadApp(server_port)
        api = Api()

        # Create a borderless window
        window = webview.create_window(
            title='Scratchpad',
            html=app.get_html(),
            js_api=api,
            frameless=True,  # Removes title bar
            resizable=True,
            width=800,
            height=600
        )

        api.set_window(window)
        # Start the webview
        webview.start(debug=False)
    finally:
        server.stop()  # Stop the server when done


if __name__ == '__main__':
    main()
