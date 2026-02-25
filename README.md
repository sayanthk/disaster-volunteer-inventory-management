# Disaster Volunteer and Resource Management System

## Prerequisites 

- Make sure you have **Python 3.8+** installed on your system.
- Make sure you are using Windows as your Operating System.

## Step-by-step Execution

1. **Open a terminal (Command Prompt or PowerShell)** and navigate to the project folder on your Desktop:
   ```cmd
   cd "C:\Users\ASUS\Desktop\project new"
   ```

2. **Activate the Virtual Environment**:
   ```cmd
   venv\Scripts\activate
   ```
   *(You should see `(venv)` appear in your terminal prompt)*

3. **Install any missing dependencies** (This is a one-time step if you just cloned the project):
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```cmd
   python app.py
   ```
   
   If successful, you will see output like this:
   ```cmd
    * Serving Flask app 'app'
    * Debug mode: on
    * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
   ```

5. **Open your Web Browser**, and go to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### Tips for Testing:
1. Start by clicking **"Register"** and create an account with the role set to **"Administrator"**. 
2. The Administrator account has full access to create Disasters, add Resources, manage Assignments, and Rate Volunteers!
