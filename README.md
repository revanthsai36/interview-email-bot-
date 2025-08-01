# Interview Email Bot

A Python script that connects to your Gmail inbox and lists recent interview-related emails.  
Great for job hunting and staying organized.

## 🔧 Setup

1. Clone the repo
2. Install requirements  
   ```
   pip install -r requirements.txt
   ```
3. Create a Google Cloud project and download `credentials.json`
4. Run the script  
   ```
   python interview_email_bot.py
   ```

## 🔒 Security

- Your Gmail access is local-only
- `credentials.json` and `token.json` are gitignored
- The app uses read-only Gmail access
