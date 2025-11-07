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

### Installation
```bash
# Install Flet
pip install flet

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
