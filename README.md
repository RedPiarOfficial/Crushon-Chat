# Overview

This Python project provides an interactive chat system with integrated email handling and translation features. It allows users to interact with characters, manage email-based authentication, and translate messages between languages. The project is structured around a command-line interface where users can select characters to chat with, manage their login methods, and handle email-based operations.

## Key Components

### SecMailApi

- **Purpose**: Handles email operations for generating random email addresses and fetching email messages.
- **Methods**:
  - `getEmail()`: Retrieves a random email address.
  - `getMessages(email)`: Fetches messages for a given email address.
  - `openMessage(email, msgId)`: Opens a specific message by its ID.

### SimpleTranslator

- **Purpose**: Provides translation services using the Google Translate API.
- **Methods**:
  - `translate(text, target_language)`: Translates the provided text to the specified language, handling large texts by splitting them into chunks.

### ChatExample

- **Purpose**: Manages user interaction with chat characters, including logging in, selecting characters, and sending messages.
- **Methods**:
  - `chat()`: Facilitates chat interaction with characters, including message translation and history retrieval.
  - `_loginCookies(fileName)`: Logs in using cookies from a file.
  - `_login(email)`: Logs in with an email address and handles authentication link confirmation.
  - `login()`: Provides options for logging in via email, cookies, or as a guest.
  - `createGuest()`: Creates a guest account, retrieves authentication URL from email, and confirms it.
  - `_clear()`: Clears the console screen based on the operating system.

## Usage

### Login Options

- **By Email**: Enter an email address and confirm the authentication link received.
- **By Cookies**: Load cookies from a file for login.
- **As Guest**: Automatically generate a guest email, retrieve authentication details, and log in.

### Chat Functionality

- Select characters from recommendations or inbox.
- View chat history with translated messages.
- Send and receive messages with translation support.

### Email Management

- Generate random email addresses.
- Retrieve and read messages from these addresses.

### Translation

- Translate messages between various languages using the Google Translate API.

## Dependencies

- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing HTML content.
- `json`: For handling JSON data.
- `time`: For managing delays.
- `os`: For interacting with the operating system.

## Example Usage

1. **Start the Program**: Run the script, and it will prompt you to allow NSFW content and select a language for translation.
2. **Login**: Choose a login method (email, cookies, or guest).
3. **Chat**: Select a character, view chat history, and interact through translated messages.

This project combines email management, character-based chat interactions, and language translation into a cohesive command-line tool, providing a versatile and user-friendly experience.
