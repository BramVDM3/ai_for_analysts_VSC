# Get Started: AI for Analysts

This file contains only the functional setup steps for the project.

For pure analysis work, you do not need Node.js or Python unless your chosen AI assistant or optional local app setup requires it.

---

## 1. Install Visual Studio Code

1. Go to [https://code.visualstudio.com](https://code.visualstudio.com).
2. Download the installer for your operating system.
3. Run the installer.
4. Open Visual Studio Code.

---

## 2. Open the Project Folder

1. In VS Code, select **File** -> **Open Folder**.
2. Select the main project folder.
3. Confirm that the Explorer shows these folders:

```text
analysis
backend
frontend
mock-database
```

---

## 3. Install VS Code Add-ons

Install these add-ons from the VS Code Extensions panel.

1. Open VS Code.
2. Click the **Extensions** icon in the left sidebar.
3. Search for the add-on name.
4. Click **Install**.

### Required

- **Markdown Preview Enhanced** by Yiyi Wang  
  Search for `Markdown Preview Enhanced`.

- **Mermaid Diagram Syntax** by Jhammond  
  Search for `Mermaid Diagram Syntax`.

- **Camunda Modeler** by Miragon  
  Search for `Camunda Modeler`.

### Recommended

- **Python** by Microsoft  
  Search for `Python`.

- **Pylance** by Microsoft  
  Search for `Pylance`.

---

## 4. Set Up an AI Assistant

Use the assistant provided by your instructor or organization.

You only need one of the options below.

### Option A: GitHub Copilot

Use this option if your instructor or organization provides GitHub Copilot access.

1. Open VS Code.
2. Click the **Accounts** icon in the bottom-left corner.
3. Sign in with your GitHub account.
4. Open the **Extensions** panel.
5. Search for `GitHub Copilot`.
6. Install **GitHub Copilot** if VS Code has not installed it automatically.
7. Open the **Chat** view from the left sidebar.
8. Sign in or authorize Copilot if VS Code asks.

Node.js is not required for this setup.

### Option B: Codex in VS Code

Use this option if your instructor or organization provides Codex access through ChatGPT.

1. Open VS Code.
2. Open the **Extensions** panel.
3. Search for `Codex`.
4. Install the Codex extension from OpenAI if it is available for your account.
5. Open Codex from the VS Code sidebar, status bar, or command palette.
6. Sign in with your ChatGPT account when prompted.

Node.js is not required when using the VS Code extension.

### Option C: Claude Code in VS Code

Use this option if your instructor or organization provides Claude Code access.

1. Open VS Code.
2. Open the **Extensions** panel.
3. Search for `Claude Code`.
4. Install **Claude Code**.
5. Open the Command Palette with `Ctrl + Shift + P`.
6. Search for `Claude Code`.
7. Select **Claude Code: Open in New Tab** or the closest available Claude Code command.
8. Sign in when prompted.

Node.js is not required for the VS Code extension setup.

### Option D: Kilo Code

1. Open VS Code.
2. Open the **Extensions** panel.
3. Search for `Kilo Code`.
4. Click the dropdown arrow next to **Install**.
5. Select **Install Pre-Release Version**.
6. Complete the sign-in or setup steps shown by Kilo Code.

Node.js is not required for the VS Code extension setup.

### Option E: Codex from the Terminal

Use this option only if you need the terminal version of Codex.

Install Node.js first:

1. Go to [https://nodejs.org](https://nodejs.org).
2. Download the LTS version.
3. Run the installer.
4. Restart VS Code after installation.

Install Codex:

```powershell
npm install -g @openai/codex
```

Sign in:

```powershell
codex --login
```

Start Codex from the project folder:

```powershell
codex
```

### Option F: Claude Code from the Terminal

Use this option only if you need the terminal version of Claude Code.

Install Node.js first:

1. Go to [https://nodejs.org](https://nodejs.org).
2. Download the LTS version.
3. Run the installer.
4. Restart VS Code after installation.

Install Claude Code:

```powershell
npm install -g @anthropic-ai/claude-code
```

Check the installation:

```powershell
claude --version
```

Start Claude Code from the project folder:

```powershell
claude
```

---

## 5. Optional: Install Python

Python is needed only if you want to run the backend locally.

1. Go to [https://www.python.org/downloads](https://www.python.org/downloads).
2. Download Python 3.11 or higher.
3. Run the installer.
4. On Windows, select **Add Python to PATH** before installing.
5. Restart VS Code after installation.

Check the installation:

```powershell
python --version
```

---

## 6. Optional: Set Up the Backend

Run these commands from the main project folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Activate it on Mac or Linux:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

---

## 7. Optional: Run the Backend

Activate the virtual environment if it is not active yet:

```powershell
.venv\Scripts\activate
```

Go to the backend folder:

```powershell
cd backend
```

Start the backend:

```powershell
uvicorn app.main:app --port 8000 --app-dir .
```

Check it in a browser:

```text
http://127.0.0.1:8000
```

Expected response:

```json
{"message":"Library AI for Analysts backend is running."}
```

Leave this terminal running while using the frontend.

---

## 8. Optional: Run the Frontend

The frontend requires Node.js.

If Node.js is not installed yet:

1. Go to [https://nodejs.org](https://nodejs.org).
2. Download the LTS version.
3. Run the installer.
4. Restart VS Code after installation.

Open a second VS Code terminal.

Go to the frontend folder:

```powershell
cd frontend
```

Copy the environment file on Windows:

```powershell
copy ..\.env.example .env
```

Copy the environment file on Mac or Linux:

```bash
cp ../.env.example .env
```

Install frontend dependencies:

```powershell
npm install
```

Start the frontend:

```powershell
npm run dev
```

Open the local frontend URL shown in the terminal. It is usually:

```text
http://localhost:5173
```

---

## 9. Optional: Run Tests

### Backend tests

From the main project folder:

```powershell
.venv\Scripts\activate
```

```powershell
cd backend
```

```powershell
python -m pytest tests -p no:cacheprovider
```

### Frontend build check

From the main project folder:

```powershell
cd frontend
```

```powershell
npm run build
```

---

## Troubleshooting

### Python is not found

- Reinstall Python.
- Select **Add Python to PATH** during installation.
- Restart VS Code.

### Node.js or npm is not found

- Reinstall the Node.js LTS version.
- Restart VS Code.

### Backend port 8000 is already in use

Check what is using port 8000:

```powershell
netstat -ano | findstr :8000
```

Use another backend port:

```powershell
uvicorn app.main:app --port 8001 --app-dir .
```

If you use another backend port, update `frontend\.env`:

```text
VITE_BACKEND_URL=http://127.0.0.1:8001
```

Restart the frontend after changing `frontend\.env`.

### Frontend packages are missing

From the `frontend` folder:

```powershell
npm install
```
