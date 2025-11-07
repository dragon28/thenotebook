# Notebook - Multi-File Markdown Editor

## Project Overview

The **Notebook** is a browser-based, three-panel Markdown editor built with Python 3.12 and Flet framework (v0.24+). It provides a clean, intuitive interface for creating, managing, and editing multiple Markdown files with real-time preview functionality.

## Features

### Core Functionality
- **Three-Panel Layout**: File list (left), editor (middle), and live preview (right)
- **Multi-File Management**: Create, edit, delete, and switch between multiple Markdown files
- **Real-Time Preview**: Instant Markdown rendering with GitHub Web extensions
- **Browser Storage**: All data persists locally in browser storage
- **Responsive Design**: Adapts to different screen sizes with responsive columns

### User Interface
- **Clean Design**: Modern, professional appearance with proper spacing and typography
- **File Operations**: New file creation with dialog, file deletion with confirmation
- **Auto-Save**: Content automatically saved to local storage on every change
- **Manual Save**: Ctrl+S support with visual confirmation
- **Error Handling**: Graceful handling of storage errors and edge cases

### Technical Features
- **GitHub Flavored Markdown**: Full support for GFM syntax and extensions
- **Monospace Editor**: Code-friendly font for better readability
- **Selectable Preview**: Users can select and copy text from preview
- **Auto-Focus**: Smart focus management for better user experience

## Architecture

### Class Structure

#### `MarkdownFile`
Represents individual markdown files with metadata:
- `name`: File name
- `content`: Markdown content
- `created_at`: Creation timestamp (future feature)
- `modified_at`: Last modification timestamp (future feature)

#### `FileManager`
Handles all file operations and storage:
- **Storage Management**: Save/load files from browser localStorage
- **CRUD Operations**: Create, read, update, delete files
- **Data Persistence**: JSON serialization for browser storage
- **Error Handling**: Graceful fallbacks and error recovery

#### `NotebookApp`
Main application controller:
- **UI Management**: Three-panel responsive layout
- **Event Handling**: User interactions and real-time updates
- **File Operations**: Integration with FileManager
- **State Management**: Current file selection and editor state

## Technical Implementation

### Storage Strategy
The application uses Flet's `page.client_storage` API which maps to:
- **Web**: Browser localStorage
- **Desktop**: JSON file storage
- **Mobile**: Platform-specific storage (SharedPreferences/NSUserDefaults)

### Real-Time Updates
- **On-Change Events**: Editor changes trigger immediate preview updates
- **Auto-Save**: Content automatically persisted to storage
- **State Synchronization**: File list updates reflect current selection

### Responsive Layout
Uses Flet's `ResponsiveRow` with breakpoint-based column allocation:
- **Mobile (xs, sm)**: Single column, stacked panels
- **Tablet (md)**: Three columns (3-5-4 ratio)
- **Desktop (lg, xl)**: Optimized three columns (2-5-5 ratio)

## Installation and Setup

### Prerequisites
- Python 3.12+
- Flet 0.24+

### Clone the GitHub repository
```bash
# Clone the GitHub repository

git clone https://github.com/dragon28/thenotebook.git

```

### Change into "thenotebook" directory
```bash
# Change into "thenotebook" directory

cd thenotebook

```

### Installation
```bash
# Install Flet
pip install flet

```

### Run the application
```bash
# Run the application
python notebook-app.py
```

### Development Mode
```bash
# Hot reload for development
flet -r notebook-app.py
```

## Usage Guide

### Getting Started
1. Launch the application - opens in default browser
2. Start with the welcome file or create a new file
3. Type Markdown in the editor panel
4. See real-time preview in the right panel

### File Management
- **New File**: Click the "+" button in the file panel
- **Select File**: Click any file in the file list
- **Delete File**: Use the delete button in the editor header
- **Auto-Save**: Content is automatically saved on every change

### Keyboard Shortcuts
- **Ctrl+S**: Manual save with confirmation message

## Comparison with Reference Projects

### vs. StackEdit
- **Similarities**: Three-panel layout, real-time preview, browser-based
- **Differences**: Simplified UI, local-only storage, Python backend
- **Advantages**: No server dependency, instant startup, privacy-focused

### vs. Dillinger
- **Similarities**: Markdown editing, live preview, file management
- **Differences**: Multi-file support, local storage, desktop-capable
- **Advantages**: Offline capability, no cloud dependency, faster performance

### vs. Editor.md
- **Similarities**: Feature-rich Markdown support, extensible architecture
- **Differences**: Native Python application, simplified feature set
- **Advantages**: Better integration, easier customization, cross-platform

## Development Considerations

### Scalability
- **File Limits**: Browser storage limitations (~5-10MB typical)
- **Performance**: Efficient real-time updates with minimal DOM manipulation
- **Memory**: Lazy loading and efficient state management

### Future Enhancements
- **Export Options**: HTML, PDF export functionality
- **Themes**: Dark/light theme support
- **Syntax Highlighting**: Code block syntax highlighting
- **Search**: Global search across all files
- **Import/Export**: File system integration
- **Collaboration**: Real-time collaborative editing

### Browser Compatibility
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Storage**: localStorage API support required
- **Features**: ES6+ JavaScript features via Flet runtime

## Security Considerations

### Data Privacy
- **Local Storage**: All data remains in browser, no server transmission
- **No Analytics**: No external tracking or data collection
- **Sandboxed**: Browser security model isolation

### Input Validation
- **File Names**: Sanitized file name input
- **Content**: Markdown content is safely rendered
- **Storage**: JSON serialization with error handling

## Performance Optimization

### Real-Time Updates
- **Debounced Saves**: Efficient storage updates
- **Minimal Re-renders**: Targeted UI updates
- **Lazy Loading**: On-demand file loading

### Memory Management
- **Efficient Storage**: Compact JSON serialization
- **State Cleanup**: Proper component lifecycle management
- **Resource Management**: Minimal memory footprint

This implementation provides a solid foundation for a modern, browser-based Markdown editor that meets all the specified requirements while maintaining clean architecture and excellent user experience.

## Project Choice

The "Notebook" - Multi-File Markdown Editor

## Justification for used Tools

- **GPT-5**: Because it was one of the best model trained with the lastest information. 
- **Perplexity Pro**: Allow prompt engineer to use **deep research** agent with unlimited access. Plus, it allowed the agent to access features which are **web search** (MCP), **social** (MCP) and **GitHub** (MCP) to gather more information and make better decesion. The model selected was **Best** based on the prompt.
- **Python Verson 3.12**: Python was one of the programming language which can be consider easy to be master by both human and artifical intelliegent (AI). The reason for choosing version 3.12 because it was one of the most stable version that supported by different python's libraries, packages and frameworks.
- **Flet**: Based on the requirements or specification of the project, the best framework to solve most of the requirements or specification of the project was **Flutter**. As a result, prompt engineer chosen **Flet** which was derive from **Flutter**. For more information, please refer to https://flet.dev/ .

## High-Level Approach

Step 1: Research on prompt engineering for software development.

Step 2: Draft the prompt.

Step 3: Use GPT-5 to refine the prompt on step 2. And interact with GPT-5 to generate the desire prompt based of the requirement and specification.

Step 4: Use Perplexity execute the refined prompt that produced by GPT-5.

Step 5: Futher test the software which generated by Perplexity. If any error or issue found, mentioned it and ask the AI to test and fix it.

## Final Prompts

'''
You are a highly experienced software developer (20+ years) proficient in Python and UI development. You will now develop a software application using **Python 3.12** and the **Flet framework v0.24+**. Follow the requirements closely and produce correct, working code without any hallucinations or errors.

**Project:** "The Notebook" – Multi-File Markdown Editor  
**Description:** A lightweight, browser-based note-taking application with a three-panel layout. It will have:  
1. **File List Panel (left)** – a panel showing a list of markdown files (notes) that the user has created or can open.  
2. **Markdown Editor Panel (center)** – a text editor area where the user can write or edit Markdown text.  
3. **Live Preview Panel (right)** – a preview area that renders the formatted Markdown in real time as the user writes.

The interface should allow users to create new notes, switch between notes by selecting from the file list, edit the content, and see the preview update live. All note data should be saved locally on the user’s device (e.g., as files on disk).

**Target Users:** People who need a simple persistent tool for organizing and writing Markdown notes in their browser (writers, developers, students, etc.). This means the app should be intuitive and data should persist between sessions (no data loss when they close and reopen the app).

**Technical Requirements and Implementation Details:**

- Use **Flet (Python)** for the entire UI. The app will run as a local web application in the browser (use `flet.app` with `view=ft.WEB_BROWSER` to launch it in the default browser:contentReference[oaicite:10]{index=10}). Ensure the UI is responsive in a desktop browser window.  
- The layout must consist of three main panels side-by-side:
  - **File List Panel (Left):** Use a vertical list control (e.g. `Column` or `ListView`) to display the list of markdown files. Each entry should be clickable/selectable to open that note. Include a way to create a new note (for example, a button at the top of this panel labeled "New Note"). When a new note is created, give it a default unique name (like “Untitled.md” or “Note1.md, Note2.md”, etc.) and add it to the list.  
  - **Editor Panel (Center):** Use a multiline text input control for editing markdown text. In Flet, you can use `ft.TextField` with `multiline=True` for this purpose:contentReference[oaicite:11]{index=11}. The text field should expand to fill its panel and allow the user to input large amounts of text (enable scrolling if text exceeds the area).  
  - **Preview Panel (Right):** Use Flet’s `ft.Markdown` control to render the markdown text as HTML preview:contentReference[oaicite:12]{index=12}. This panel should update whenever the user types or the content changes in the editor. The preview should be read-only (no editing in this panel, just display). Allow it to scroll if content is long (you can place the `Markdown` control inside a scrollable container if needed).  
- **Behavior:**
  - **Opening a Note:** When the user selects a file from the File List Panel, the application should load that file’s content into the Editor Panel for editing *and* simultaneously update the Preview Panel. 
  - **Live Preview:** Implement live preview functionality. This means as the user types or makes changes in the Editor Panel, the Preview Panel should update to reflect the formatted Markdown. You can achieve this by handling the text field’s change event (`on_change`) and updating the `Markdown` control’s `value` accordingly:contentReference[oaicite:13]{index=13}:contentReference[oaicite:14]{index=14}. The update should happen either on every keystroke or on a short debounce (for simplicity, on every change event is fine).  
  - **Saving Notes:** All notes should be saved locally to disk so that data persists. Implement saving functionality such that whenever a note is modified, it is saved to a `.md` file on the user’s device (for example, in a folder named "notes" within the app’s directory). You may auto-save after each change or at a regular interval, and/or provide a “Save” button for manual saves. At minimum, ensure that when the user switches notes or closes the app, the latest changes are written to file. Use Python file I/O to write the text content to markdown files. (If using auto-save on each edit, be mindful of performance; otherwise, a manual save button or save on exit is acceptable). Ensure that the necessary directory (e.g., "./notes") exists or create it programmatically if not.  
  - **New Note Creation:** When the user clicks "New Note", create a new empty markdown file (e.g., "Untitled.md" or "Untitled1.md", etc., not clashing with existing names). Add this new file to the file list and open it in the editor for the user to start writing. (The Preview panel will initially be blank or show any template text if you start with some default content).  
  - **UI Details:** Add an application title (e.g., in the window title or an AppBar). You can use `ft.AppBar` for a header if desired (for example, showing the app name and perhaps a save icon). Include any helpful icons or indicators for usability (like a save button, or icons for new file, etc., using `ft.IconButton` in the AppBar actions). These are optional but improve user experience.  
- **Error Handling:** The program should handle basic errors (for example, if a file fails to save or load, it should catch the exception and perhaps show an alert message using Flet). Ensure that file paths are handled correctly. Also, avoid any hard-coded platform-specific paths; use relative paths or Python’s `os` module to build paths (so it works on any OS).  
- **Performance Considerations:** Since the preview updates live, ensure the approach is efficient (Flet’s markdown rendering is efficient for typical note sizes). If a file is very large, consider if needed to throttle the updates (but that is an extra optimization – not mandatory if not easily implemented).  
- **No External Libraries for Markdown:** Use the Flet built-in Markdown control for rendering. Do not use external markdown libraries or web frameworks – they are not needed because Flet provides the functionality out-of-the-box:contentReference[oaicite:15]{index=15}. This keeps the app lightweight.  
- **Avoid Nonexistent Features:** **Do not invent any APIs or classes.** Use only the Flet controls and Python standard libraries. For example, do not use any pseudo-code or placeholders. Everything in the output should be real code that can run. (Flet provides `TextField`, `Markdown`, `Row`, `Column`, `ListView`, `FilePicker`, etc., so use those as appropriate. If something is needed like a dialog or confirmation, use Flet’s controls for that as well.)  
- **Output Format:** Provide the **complete Python code** for the application in a single code block. The code should include all necessary imports (e.g. `import flet as ft`) and the `ft.app(target=main, view=ft.WEB_BROWSER)` call to launch the app in a browser:contentReference[oaicite:16]{index=16}. The code should be well-structured (you can define helper functions or classes if needed) and include comments to explain major sections, reflecting best practices of a 20-year veteran developer. Do not include any additional explanation outside the code – just output the code itself, ready to be run. Make sure this final code has no syntax errors or undefined variables.  

Remember, the goal is to create a functional, polished Markdown editor with multiple files support, live preview, and local persistence. Keep the user experience simple and smooth, similar to known editors like *StackEdit* or *Dillinger* (e.g., edit on left, preview on right, files list on the side):contentReference[oaicite:17]{index=17}. **Double-check your solution** for accuracy and completeness before finalizing. Now, please generate the full Python code for this application.
'''

