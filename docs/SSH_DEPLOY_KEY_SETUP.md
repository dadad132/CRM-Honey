# SSH Deploy Key Setup for Private Repository

This guide explains how to set up SSH deploy keys so the server can pull updates from a private GitHub repository.

## Why Use SSH Deploy Keys?

- Makes the repository private so only authorized servers can access the code
- More secure than storing passwords or tokens
- Allows automated updates without exposing credentials

## Setup Steps

### 1. Generate SSH Key on the Server

SSH into your server and generate a new SSH key:

```bash
# Connect to your server
ssh user@your-server-ip

# Generate a new SSH key (Ed25519 is recommended)
ssh-keygen -t ed25519 -C "crm-deploy-key" -f ~/.ssh/crm_deploy_key -N ""
```

This creates two files:
- `~/.ssh/crm_deploy_key` - Private key (keep this secret!)
- `~/.ssh/crm_deploy_key.pub` - Public key (add this to GitHub)

### 2. Add the Public Key to GitHub

1. Copy the public key:
   ```bash
   cat ~/.ssh/crm_deploy_key.pub
   ```

2. Go to your GitHub repository → **Settings** → **Deploy keys**

3. Click **Add deploy key**

4. Give it a name like "Production Server"

5. Paste the public key content

6. ✅ Check "Allow write access" if you want to push from server (usually not needed)

7. Click **Add key**

### 3. Configure SSH on the Server

Create or edit `~/.ssh/config`:

```bash
nano ~/.ssh/config
```

Add the following:

```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/crm_deploy_key
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
```

Set proper permissions:

```bash
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/crm_deploy_key
chmod 644 ~/.ssh/crm_deploy_key.pub
```

### 4. Test the SSH Connection

```bash
ssh -T git@github.com
```

You should see:
```
Hi dadad132/cem-backend! You've successfully authenticated...
```

### 5. Update Git Remote to Use SSH

Check your current remote:
```bash
cd ~/crm-backend
git remote -v
```

If it shows HTTPS, change it to SSH:
```bash
# Change from HTTPS to SSH
git remote set-url origin git@github.com:dadad132/cem-backend.git

# Verify the change
git remote -v
```

### 6. Make the GitHub Repository Private

1. Go to your GitHub repository → **Settings**

2. Scroll down to **Danger Zone**

3. Click **Change visibility**

4. Select **Make private**

5. Confirm the change

## How the Update System Uses SSH

The CRM update system automatically detects SSH keys in these locations (in order):

1. `~/.ssh/github_deploy_key`
2. `~/.ssh/crm_deploy_key`
3. `~/.ssh/deploy_key`
4. `~/.ssh/id_ed25519`
5. `~/.ssh/id_rsa`

When an SSH key is found, the system automatically configures git to use it for pulling updates.

## Troubleshooting

### "Permission denied (publickey)"

1. Check that the key is properly added to GitHub:
   ```bash
   ssh -vT git@github.com
   ```

2. Verify key permissions:
   ```bash
   chmod 600 ~/.ssh/crm_deploy_key
   ```

3. Make sure the correct key is being used:
   ```bash
   ssh -T -i ~/.ssh/crm_deploy_key git@github.com
   ```

### "Repository not found"

- The deploy key might not have been added to the correct repository
- The repository name in the URL might be wrong
- Check if the repository is actually private

### Update Fails from Web Interface

Check the logs:
```bash
sudo journalctl -u crm-backend -n 100 --no-pager
```

Look for SSH-related errors and verify the key path.

## Multiple Servers

If you have multiple servers, you can either:

1. **Use the same deploy key** on all servers (easier but less secure)

2. **Create separate deploy keys** for each server:
   - Generate a unique key on each server
   - Add each public key to GitHub's deploy keys
   - Name them descriptively (e.g., "Production Server", "Staging Server")

## Security Best Practices

1. **Never share the private key** - It should only exist on your server

2. **Don't enable write access** unless absolutely necessary

3. **Rotate keys periodically** - Remove old keys from GitHub when servers are decommissioned

4. **Use Ed25519 keys** - They are more secure and smaller than RSA keys

5. **Consider IP restrictions** - GitHub Enterprise allows restricting deploy key access by IP

## Quick Commands Reference

```bash
# Generate new key
ssh-keygen -t ed25519 -C "crm-deploy-key" -f ~/.ssh/crm_deploy_key -N ""

# View public key
cat ~/.ssh/crm_deploy_key.pub

# Test connection
ssh -T git@github.com

# Change remote to SSH
git remote set-url origin git@github.com:dadad132/cem-backend.git

# Manual pull with specific key
GIT_SSH_COMMAND='ssh -i ~/.ssh/crm_deploy_key' git pull origin main
```
