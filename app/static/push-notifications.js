// Push Notifications Manager for CEM PWA
(function() {
  'use strict';

  // Check if service workers and push notifications are supported
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    console.log('Push notifications not supported');
    return;
  }

  // Request notification permission
  async function requestNotificationPermission() {
    try {
      const permission = await Notification.requestPermission();
      console.log('Notification permission:', permission);
      
      if (permission === 'granted') {
        await subscribeToPushNotifications();
      } else if (permission === 'denied') {
        console.log('Notification permission denied');
      }
      
      return permission;
    } catch (error) {
      console.error('Error requesting notification permission:', error);
    }
  }

  // Subscribe to push notifications
  async function subscribeToPushNotifications() {
    try {
      const registration = await navigator.serviceWorker.ready;
      
      // Check if already subscribed
      const existingSubscription = await registration.pushManager.getSubscription();
      if (existingSubscription) {
        console.log('Already subscribed to push notifications');
        await sendSubscriptionToServer(existingSubscription);
        return existingSubscription;
      }

      // Create new subscription
      // Note: For production, you should generate VAPID keys on the server
      // For now, we'll use a simple notification system without server-side push
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: null  // Would need VAPID keys for real push notifications
      });

      console.log('Subscribed to push notifications:', subscription);
      await sendSubscriptionToServer(subscription);
      
      return subscription;
    } catch (error) {
      console.error('Error subscribing to push notifications:', error);
    }
  }

  // Send subscription to server
  async function sendSubscriptionToServer(subscription) {
    try {
      const response = await fetch('/web/push/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          subscription: subscription.toJSON()
        })
      });

      if (!response.ok) {
        console.error('Failed to send subscription to server');
      } else {
        console.log('Subscription sent to server successfully');
      }
    } catch (error) {
      console.error('Error sending subscription to server:', error);
    }
  }

  // Check current notification permission
  function checkNotificationPermission() {
    if ('Notification' in window) {
      return Notification.permission;
    }
    return 'unsupported';
  }

  // Show a test notification (local)
  async function showTestNotification() {
    if (Notification.permission !== 'granted') {
      await requestNotificationPermission();
      return;
    }

    const registration = await navigator.serviceWorker.ready;
    
    registration.showNotification('CEM Test Notification', {
      body: 'This is a test notification from CEM!',
      icon: '/static/icons/icon-192x192.png',
      badge: '/static/icons/icon-72x72.png',
      vibrate: [200, 100, 200],
      data: {
        url: '/web/dashboard'
      },
      actions: [
        {
          action: 'open',
          title: 'Open'
        }
      ]
    });
  }

  // Initialize notification button if it exists
  function initializeNotificationUI() {
    const notificationBtn = document.getElementById('enableNotificationsBtn');
    const notificationStatus = document.getElementById('notificationStatus');
    
    if (notificationBtn) {
      const permission = checkNotificationPermission();
      
      if (permission === 'granted') {
        notificationBtn.textContent = 'Test Notification';
        if (notificationStatus) {
          notificationStatus.textContent = 'Enabled';
          notificationStatus.className = 'text-sm text-green-600 font-medium';
        }
        notificationBtn.onclick = showTestNotification;
      } else if (permission === 'denied') {
        notificationBtn.textContent = 'Blocked';
        notificationBtn.disabled = true;
        if (notificationStatus) {
          notificationStatus.textContent = 'Blocked';
          notificationStatus.className = 'text-sm text-red-600 font-medium';
        }
      } else {
        notificationBtn.textContent = 'Enable Notifications';
        if (notificationStatus) {
          notificationStatus.textContent = 'Disabled';
          notificationStatus.className = 'text-sm text-slate-500 font-medium';
        }
        notificationBtn.onclick = requestNotificationPermission;
      }
    }
  }

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeNotificationUI);
  } else {
    initializeNotificationUI();
  }

  // Expose functions globally
  window.cemPushNotifications = {
    requestPermission: requestNotificationPermission,
    subscribe: subscribeToPushNotifications,
    checkPermission: checkNotificationPermission,
    showTest: showTestNotification,
    init: initializeNotificationUI
  };

})();
