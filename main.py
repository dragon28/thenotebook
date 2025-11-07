import flet as ft
import os
from pathlib import Path
from datetime import datetime
import asyncio
import time
import threading

# Directory to store notes
NOTES_DIR = Path("notes")

class NotebookApp:
    """Multi-file Markdown Editor with live preview"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "The Notebook - Markdown Editor"
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Ensure notes directory exists
        NOTES_DIR.mkdir(exist_ok=True)
        
        # Application state
        self.current_file = None
        self.files = []
        self.is_loading = False
        self.save_timer = None
        
        # UI Components
        self.file_list = ft.ListView(
            spacing=5,
            padding=10,
            expand=True,
        )
        
        self.editor = ft.TextField(
            multiline=True,
            min_lines=1,
            max_lines=None,
            expand=True,
            border_color=ft.Colors.GREY_400,
            text_size=14,
            on_change=self.on_editor_change,
        )
        
        self.preview = ft.Markdown(
            value="",
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=self.handle_link_click,
            expand=True,
        )
        
        self.current_file_label = ft.Text(
            "No file selected",
            size=14,
            weight=ft.FontWeight.BOLD,
        )
        
        self.save_status = ft.Text(
            "",
            size=12,
            color=ft.Colors.GREEN_700,
        )
        
        # Build UI
        self.build_ui()
        
        # Load existing files
        self.load_files()
    
    async def handle_link_click(self, e):
        """Handle markdown link clicks (async handler)"""
        await self.page.launch_url_async(e.data)
        
    def build_ui(self):
        """Construct the three-panel layout"""
        
        # AppBar
        self.page.appbar = ft.AppBar(
            title=ft.Text("The Notebook", size=20, weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.Colors.BLUE_700,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.SAVE,
                    tooltip="Save (Ctrl+S)",
                    on_click=self.save_current_file,
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    tooltip="Refresh file list",
                    on_click=lambda _: self.load_files(),
                ),
            ],
        )
        
        # Left Panel - File List
        new_note_btn = ft.ElevatedButton(
            "New Note",
            icon=ft.Icons.ADD,
            on_click=self.create_new_note,
            width=200,
        )
        
        left_panel = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=new_note_btn,
                    padding=10,
                ),
                ft.Divider(height=1),
                ft.Container(
                    content=ft.Text("Your Notes", size=16, weight=ft.FontWeight.BOLD),
                    padding=ft.padding.only(left=10, top=10, bottom=5),
                ),
                self.file_list,
            ]),
            width=250,
            bgcolor=ft.Colors.GREY_100,
            border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
        )
        
        # Center Panel - Editor
        editor_header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.EDIT, size=16),
                self.current_file_label,
                self.save_status,
            ], spacing=10),
            padding=10,
            bgcolor=ft.Colors.GREY_200,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
        )
        
        center_panel = ft.Container(
            content=ft.Column([
                editor_header,
                ft.Container(
                    content=self.editor,
                    padding=10,
                    expand=True,
                ),
            ], spacing=0, expand=True),
            expand=2,
            border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
        )
        
        # Right Panel - Preview
        preview_header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.VISIBILITY, size=16),
                ft.Text("Preview", size=14, weight=ft.FontWeight.BOLD),
            ], spacing=10),
            padding=10,
            bgcolor=ft.Colors.GREY_200,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
        )
        
        preview_container = ft.Container(
            content=self.preview,
            padding=10,
            expand=True,
        )
        
        right_panel = ft.Container(
            content=ft.Column([
                preview_header,
                ft.Column([preview_container], scroll=ft.ScrollMode.AUTO, expand=True),
            ], spacing=0, expand=True),
            expand=2,
        )
        
        # Main layout
        main_content = ft.Row(
            [left_panel, center_panel, right_panel],
            spacing=0,
            expand=True,
        )
        
        self.page.add(main_content)
        self.page.update()
        
    def load_files(self):
        """Load all markdown files from notes directory"""
        try:
            self.files = sorted(
                [f for f in NOTES_DIR.iterdir() if f.suffix == '.md'],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            self.file_list.controls.clear()
            
            if not self.files:
                self.file_list.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "No notes yet.\nClick 'New Note' to start!",
                            size=12,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=20,
                    )
                )
            else:
                for file_path in self.files:
                    is_selected = self.current_file == file_path
                    self.file_list.controls.append(
                        self.create_file_list_item(file_path, is_selected)
                    )
            
            self.page.update()
            
        except Exception as e:
            self.show_error(f"Error loading files: {str(e)}")
    
    def create_file_list_item(self, file_path: Path, is_selected: bool):
        """Create a clickable file list item"""
        
        # Get file modified time
        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        time_str = mod_time.strftime("%b %d, %Y %H:%M")
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    file_path.name,
                    size=14,
                    weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL,
                    color=ft.Colors.BLUE_700 if is_selected else ft.Colors.BLACK,
                ),
                ft.Text(
                    time_str,
                    size=10,
                    color=ft.Colors.GREY_600,
                ),
            ], spacing=2),
            padding=10,
            bgcolor=ft.Colors.BLUE_50 if is_selected else ft.Colors.WHITE,
            border_radius=5,
            on_click=lambda _, fp=file_path: self.open_file(fp),
            ink=True,
        )
    
    def create_new_note(self, e):
        """Create a new markdown note"""
        try:
            # Generate unique filename
            base_name = "Untitled"
            counter = 1
            file_name = f"{base_name}.md"
            file_path = NOTES_DIR / file_name
            
            while file_path.exists():
                file_name = f"{base_name}{counter}.md"
                file_path = NOTES_DIR / file_name
                counter += 1
            
            # Create empty file
            file_path.write_text("# New Note\n\nStart writing here...", encoding='utf-8')
            
            # Reload files and open the new one
            self.load_files()
            self.open_file(file_path)
            
        except Exception as ex:
            self.show_error(f"Error creating new note: {str(ex)}")
    
    def open_file(self, file_path: Path):
        """Open a file for editing"""
        try:
            self.is_loading = True
            
            # Save current file before switching
            if self.current_file and self.current_file != file_path:
                self.save_current_file(None, show_status=False)
            
            # Load file content
            content = file_path.read_text(encoding='utf-8')
            
            self.current_file = file_path
            self.editor.value = content
            self.preview.value = content
            self.current_file_label.value = file_path.name
            
            # Update file list to show selection
            self.load_files()
            
            self.is_loading = False
            self.page.update()
            
        except Exception as ex:
            self.is_loading = False
            self.show_error(f"Error opening file: {str(ex)}")
    
    def on_editor_change(self, e):
        """Handle editor text changes for live preview"""
        if not self.is_loading:
            # Update preview in real-time
            self.preview.value = self.editor.value if self.editor.value else ""
            self.page.update()
            
            # Debounced auto-save
            if self.save_timer:
                self.save_timer.cancel()
            
            self.save_timer = threading.Timer(1.0, lambda: self.save_current_file(None, auto=True))
            self.save_timer.daemon = True
            self.save_timer.start()
    
    def save_current_file(self, e, auto=False, show_status=True):
        """Save the current file to disk"""
        if not self.current_file:
            return
        
        try:
            content = self.editor.value or ""
            self.current_file.write_text(content, encoding='utf-8')
            
            if not auto and show_status:
                self.save_status.value = "✓ Saved"
                self.page.update()
                
                # Clear status after 2 seconds
                def clear_status():
                    time.sleep(2)
                    self.save_status.value = ""
                    try:
                        self.page.update()
                    except:
                        pass  # Page might be closed
                
                threading.Thread(target=clear_status, daemon=True).start()
                
        except Exception as ex:
            if show_status:
                self.show_error(f"Error saving file: {str(ex)}")
    
    def show_error(self, message: str):
        """Display error dialog"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


def main(page: ft.Page):
    """Main entry point for the application"""
    NotebookApp(page)


# Launch the application in a web browser
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
