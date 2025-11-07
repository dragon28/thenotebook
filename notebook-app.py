import flet as ft
import json
import os
from typing import Dict, List


class MarkdownFile:
    """Represents a markdown file with its content and metadata"""
    
    def __init__(self, name: str, content: str = "# New Note\n\nStart writing here..."):
        self.name = name
        self.content = content
        self.created_at = None
        self.modified_at = None


class FileManager:
    """Handles file operations and storage"""
    
    STORAGE_KEY = "notebook_files"
    
    def __init__(self, page: ft.Page):
        self.page = page
        self._files: Dict[str, MarkdownFile] = {}
        self._load_files()
    
    def _load_files(self):
        """Load files from browser local storage"""
        try:
            stored_data = self.page.client_storage.get(self.STORAGE_KEY)
            if stored_data:
                files_data = json.loads(stored_data) if isinstance(stored_data, str) else stored_data
                for name, data in files_data.items():
                    self._files[name] = MarkdownFile(name, data.get('content', ''))
            else:
                # Create default file if no files exist
                default_file = MarkdownFile("Welcome.md", "# Welcome to Notebook\n\nThis is your first note. You can:\n\n- Create new files\n- Edit markdown content\n- See live preview\n- All data is saved locally in your browser\n\n## Getting Started\n\nClick the **New File** button to create a new note.")
                self._files["Welcome.md"] = default_file
                self._save_files()
        except Exception as e:
            print(f"Error loading files: {e}")
            # Create default file on error
            default_file = MarkdownFile("Welcome.md", "# Welcome to Notebook\n\nStart writing your notes here...")
            self._files["Welcome.md"] = default_file
    
    def _save_files(self):
        """Save files to browser local storage"""
        try:
            files_data = {
                name: {"content": file.content}
                for name, file in self._files.items()
            }
            self.page.client_storage.set(self.STORAGE_KEY, json.dumps(files_data))
        except Exception as e:
            print(f"Error saving files: {e}")
    
    def get_files(self) -> List[str]:
        """Get list of file names"""
        return list(self._files.keys())
    
    def get_file(self, name: str) -> MarkdownFile:
        """Get file by name"""
        return self._files.get(name)
    
    def create_file(self, name: str) -> MarkdownFile:
        """Create a new file"""
        if not name.endswith('.md'):
            name += '.md'
        
        file = MarkdownFile(name)
        self._files[name] = file
        self._save_files()
        return file
    
    def update_file(self, name: str, content: str):
        """Update file content"""
        if name in self._files:
            self._files[name].content = content
            self._save_files()
    
    def delete_file(self, name: str):
        """Delete a file"""
        if name in self._files and len(self._files) > 1:  # Keep at least one file
            del self._files[name]
            self._save_files()
            return True
        return False


class NotebookApp:
    """Main application class for the Notebook markdown editor"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.file_manager = FileManager(page)
        self.current_file = None
        
        # UI Components
        self.file_list = ft.ListView(
            expand=True,
            spacing=5,
            padding=ft.padding.all(10)
        )
        
        self.markdown_editor = ft.TextField(
            multiline=True,
            expand=True,
            hint_text="Start writing your markdown here...",
            border_color=ft.colors.OUTLINE,
            on_change=self._on_editor_change,
            text_style=ft.TextStyle(font_family="monospace", size=14)
        )
        
        self.markdown_preview = ft.Markdown(
            value="",
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            auto_follow_links=True,
            expand=True
        )
        
        self._setup_ui()
        self._load_initial_file()
    
    def _setup_ui(self):
        """Setup the user interface"""
        self.page.title = "Notebook - Markdown Editor"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        
        # File panel (left)
        file_panel = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                            "Files",
                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.IconButton(
                            icon=ft.icons.ADD,
                            tooltip="New File",
                            on_click=self._create_new_file
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(15),
                    bgcolor=ft.colors.SURFACE_VARIANT
                ),
                ft.Container(
                    content=self.file_list,
                    expand=True,
                    bgcolor=ft.colors.SURFACE
                )
            ]),
            width=280,
            bgcolor=ft.colors.SURFACE,
            border=ft.border.only(right=ft.border.BorderSide(2, ft.colors.OUTLINE_VARIANT))
        )
        
        # Editor panel (middle)
        editor_panel = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                            "Editor",
                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.SAVE,
                                tooltip="Save (Ctrl+S)",
                                on_click=self._save_current_file
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Delete File",
                                on_click=self._delete_current_file
                            )
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(15),
                    bgcolor=ft.colors.SURFACE_VARIANT
                ),
                ft.Container(
                    content=self.markdown_editor,
                    expand=True,
                    padding=ft.padding.all(15)
                )
            ]),
            expand=True,
            bgcolor=ft.colors.SURFACE,
            border=ft.border.only(right=ft.border.BorderSide(2, ft.colors.OUTLINE_VARIANT))
        )
        
        # Preview panel (right)
        preview_panel = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(
                        "Preview",
                        style=ft.TextThemeStyle.HEADLINE_SMALL,
                        weight=ft.FontWeight.BOLD
                    ),
                    padding=ft.padding.all(15),
                    bgcolor=ft.colors.SURFACE_VARIANT
                ),
                ft.Container(
                    content=ft.Column([
                        self.markdown_preview
                    ], scroll=ft.ScrollMode.AUTO),
                    expand=True,
                    padding=ft.padding.all(15)
                )
            ]),
            expand=True,
            bgcolor=ft.colors.SURFACE
        )
        
        # Main layout - three panel responsive row
        main_layout = ft.ResponsiveRow([
            ft.Container(
                content=file_panel,
                col={"xs": 12, "sm": 12, "md": 3, "lg": 3, "xl": 2}
            ),
            ft.Container(
                content=editor_panel,
                col={"xs": 12, "sm": 12, "md": 5, "lg": 5, "xl": 5}
            ),
            ft.Container(
                content=preview_panel,
                col={"xs": 12, "sm": 12, "md": 4, "lg": 4, "xl": 5}
            )
        ])
        
        self.page.add(main_layout)
        self._refresh_file_list()
    
    def _load_initial_file(self):
        """Load the first available file"""
        files = self.file_manager.get_files()
        if files:
            self._select_file(files[0])
    
    def _refresh_file_list(self):
        """Refresh the file list in the UI"""
        self.file_list.controls.clear()
        
        files = self.file_manager.get_files()
        for filename in sorted(files):
            file_item = ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.icons.INSERT_DRIVE_FILE, size=20),
                    title=ft.Text(filename, size=14),
                    on_click=lambda e, name=filename: self._select_file(name),
                    selected=filename == (self.current_file.name if self.current_file else None)
                ),
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=5)
            )
            self.file_list.controls.append(file_item)
        
        self.page.update()
    
    def _select_file(self, filename: str):
        """Select and load a file for editing"""
        file = self.file_manager.get_file(filename)
        if file:
            self.current_file = file
            self.markdown_editor.value = file.content
            self.markdown_preview.value = file.content
            self._refresh_file_list()
            self.page.update()
    
    def _on_editor_change(self, e):
        """Handle editor content changes - real-time preview update"""
        if self.current_file:
            content = self.markdown_editor.value
            self.markdown_preview.value = content
            # Auto-save to local storage
            self.file_manager.update_file(self.current_file.name, content)
            self.page.update()
    
    def _create_new_file(self, e):
        """Create a new markdown file"""
        def create_file_dialog(e):
            filename = filename_input.value.strip()
            if filename:
                if not filename.endswith('.md'):
                    filename += '.md'
                
                # Check if file already exists
                if filename in self.file_manager.get_files():
                    error_text.value = "File already exists!"
                    self.page.update()
                    return
                
                # Create new file
                file = self.file_manager.create_file(filename)
                self._select_file(file.name)
                self._refresh_file_list()
                dialog.open = False
                self.page.update()
        
        filename_input = ft.TextField(
            label="File name",
            hint_text="my-note.md",
            autofocus=True,
            on_submit=create_file_dialog
        )
        
        error_text = ft.Text("", color=ft.colors.ERROR, size=12)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Create New File"),
            content=ft.Column([
                filename_input,
                error_text
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("Create", on_click=create_file_dialog)
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _save_current_file(self, e):
        """Save current file (manual save trigger)"""
        if self.current_file:
            content = self.markdown_editor.value
            self.file_manager.update_file(self.current_file.name, content)
            # Show save confirmation
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Saved {self.current_file.name}"),
                    duration=2000
                )
            )
    
    def _delete_current_file(self, e):
        """Delete the current file"""
        if not self.current_file:
            return
        
        def confirm_delete(e):
            if self.file_manager.delete_file(self.current_file.name):
                # Load first available file
                files = self.file_manager.get_files()
                if files:
                    self._select_file(files[0])
                else:
                    # Create a new default file
                    new_file = self.file_manager.create_file("untitled.md")
                    self._select_file(new_file.name)
                
                self._refresh_file_list()
                dialog.open = False
                self.page.update()
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("File deleted"),
                        duration=2000
                    )
                )
            else:
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Cannot delete the last file"),
                        duration=2000
                    )
                )
                dialog.open = False
                self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Delete File"),
            content=ft.Text(f"Are you sure you want to delete '{self.current_file.name}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton(
                    "Delete",
                    color=ft.colors.ERROR,
                    on_click=confirm_delete
                )
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


def main(page: ft.Page):
    """Main entry point for the Flet application"""
    app = NotebookApp(page)


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)