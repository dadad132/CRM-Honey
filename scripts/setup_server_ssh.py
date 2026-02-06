#!/usr/bin/env python3
"""
SSH Key Setup for Private Repository Access
Generates a new SSH key on the server and configures git
"""
import os
import subprocess
from pathlib import Path

def setup_ssh():
    print("=" * 60)
    print("SSH Key Setup for Private Repository")
    print("=" * 60)
    
    home = Path.home()
    ssh_dir = home / ".ssh"
    key_path = ssh_dir / "crm_deploy_key"
    pub_key_path = ssh_dir / "crm_deploy_key.pub"
    
    # Create .ssh directory
    ssh_dir.mkdir(mode=0o700, exist_ok=True)
    
    # Generate new key if it doesn't exist
    if not key_path.exists():
        print("\n[1/4] Generating new SSH key...")
        subprocess.run([
            "ssh-keygen", "-t", "ed25519", 
            "-C", "crm-server-deploy-key",
            "-f", str(key_path),
            "-N", ""  # No passphrase
        ], check=True)
        print("✓ SSH key generated")
    else:
        print("\n[1/4] SSH key already exists")
    
    # Add GitHub to known hosts
    print("\n[2/4] Adding GitHub to known hosts...")
    known_hosts = ssh_dir / "known_hosts"
    result = subprocess.run(
        ["ssh-keyscan", "github.com"],
        capture_output=True, text=True
    )
    if result.stdout:
        with open(known_hosts, "a") as f:
            f.write(result.stdout)
        print("✓ GitHub added to known hosts")
    
    # Update git remote to SSH
    print("\n[3/4] Updating git remote to SSH...")
    try:
        subprocess.run([
            "git", "remote", "set-url", "origin",
            "git@github.com:dadad132/cem-backend.git"
        ], check=True)
        print("✓ Git remote updated to SSH")
    except:
        print("⚠ Could not update git remote")
    
    # Show public key
    print("\n[4/4] Your PUBLIC KEY (add this to GitHub):")
    print("=" * 60)
    if pub_key_path.exists():
        print(pub_key_path.read_text())
    print("=" * 60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Copy the public key above")
    print("2. Go to: https://github.com/dadad132/cem-backend/settings/keys")
    print("3. Click 'Add deploy key'")
    print("4. Paste the key and save")
    print("5. Then the Update button will work!\n")

if __name__ == "__main__":
    setup_ssh()
