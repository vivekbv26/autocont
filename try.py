#!/usr/bin/env python3
"""
Run this script locally ONCE to generate your refresh token.
Make sure you have client_secret.json in the same directory.
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes required for YouTube upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = "client_secret.json"  # Downloaded from Google Cloud Console

def generate_refresh_token():
    """Generate and display refresh token for GitHub Actions setup"""
    
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"❌ Error: {CLIENT_SECRETS_FILE} not found!")
        print("Please download the OAuth client JSON file from Google Cloud Console")
        return
    
    try:
        # Create the flow using the client secrets file
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        
        # Run the OAuth flow
        print("🚀 Starting OAuth flow...")
        print("📱 A browser window will open for authentication")
        
        # Try different ports in case 8080 is blocked
        ports_to_try = [8080, 8081, 8082, 9090, 3000, 5000]
        credentials = None
        
        for port in ports_to_try:
            try:
                print(f"🔍 Trying port {port}...")
                credentials = flow.run_local_server(
                    port=port,
                    access_type='offline',
                    prompt='consent'
                )
                print(f"✅ Successfully used port {port}")
                break
            except OSError as e:
                print(f"❌ Port {port} failed: {e}")
                continue
        
        if not credentials:
            print("❌ All ports failed. Trying console-based flow...")
            # Fallback to console flow
            credentials = flow.run_console()
            print("✅ Console flow completed")
        
        # Load client info for GitHub Actions setup
        with open(CLIENT_SECRETS_FILE, 'r') as f:
            client_info = json.load(f)['installed']
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Copy these values to GitHub Secrets:")
        print("="*60)
        print(f"YOUTUBE_CLIENT_ID: {client_info['client_id']}")
        print(f"YOUTUBE_CLIENT_SECRET: {client_info['client_secret']}")
        print(f"YOUTUBE_REFRESH_TOKEN: {credentials.refresh_token}")
        print("="*60)
        
        return {
            'client_id': client_info['client_id'],
            'client_secret': client_info['client_secret'],
            'refresh_token': credentials.refresh_token
        }
        
    except Exception as e:
        print(f"❌ Error during OAuth flow: {e}")
        return None

if __name__ == "__main__":
    print("🔐 YouTube OAuth Setup for GitHub Actions")
    print("-" * 50)
    
    # Install required packages reminder
    print("📦 Make sure you have installed:")
    print("   pip install google-auth google-auth-oauthlib google-api-python-client")
    print()
    
    tokens = generate_refresh_token()
    
    if tokens:
        print("\n📝 Next steps:")
        print("1. Go to your GitHub repository")
        print("2. Settings > Secrets and variables > Actions")
        print("3. Add the three secrets shown above")
        print("4. Run your GitHub Action!")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")