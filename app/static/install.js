// PWA Install Prompt Handler
let deferredPrompt;
let installButton;

window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent the mini-infobar from appearing on mobile
  e.preventDefault();
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  // Show install button
  showInstallButton();
});

function showInstallButton() {
  // Check if button already exists
  if (document.getElementById('pwa-install-button')) {
    document.getElementById('pwa-install-button').style.display = 'block';
    return;
  }
  
  // Create install button
  installButton = document.createElement('button');
  installButton.id = 'pwa-install-button';
  installButton.innerHTML = `
    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
    </svg>
    Install App
  `;
  installButton.className = 'fixed bottom-4 right-4 z-50 flex items-center px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 font-medium';
  installButton.style.display = 'block';
  
  installButton.addEventListener('click', async () => {
    if (!deferredPrompt) {
      return;
    }
    // Show the install prompt
    deferredPrompt.prompt();
    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response to install prompt: ${outcome}`);
    // Clear the deferredPrompt
    deferredPrompt = null;
    // Hide the install button
    installButton.style.display = 'none';
  });
  
  document.body.appendChild(installButton);
}

// Hide install button if already installed
window.addEventListener('appinstalled', () => {
  console.log('PWA was installed');
  if (installButton) {
    installButton.style.display = 'none';
  }
});

// Check if app is in standalone mode (already installed)
if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
  console.log('App is running in standalone mode');
  // Hide install button if it exists
  const btn = document.getElementById('pwa-install-button');
  if (btn) {
    btn.style.display = 'none';
  }
}
