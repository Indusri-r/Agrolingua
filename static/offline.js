// Agrolinga Offline Logic
// Handles no-network scenarios with fallbacks

// Offline advice data
const OFFLINE_ADVICE = {
  organic_tips: [
    'Maintain soil moisture between 40-60%',
    'Use organic mulch to retain water',
    'Test soil pH regularly (ideal 6.5-7.5)',
    'Apply vermicompost 2 tons/acre',
    'Crop rotation every season',
    'Neem oil for natural pest control'
  ],
  markets: {
    telangana: 'Hyderabad Rythu Bazaar: Maize ₹2200/qt, Rice ₹2800/qt',
    ap: 'Vijayawada Market: Chilli ₹8000/qt'
  }
};

// Check offline and show banner
function checkOffline() {
  const banner = document.getElementById('offline-banner');
  if (!navigator.onLine) {
    banner.textContent = '⚠️ Offline Mode - Using cached data & basic advice';
    banner.style.display = 'block';
    loadOfflineAdvice();
  } else {
    banner.style.display = 'none';
  }
}

// Load fallback advice
function loadOfflineAdvice() {
  const adviceContent = document.getElementById('organic-advice-content') || document.getElementById('advice-content');
  if (adviceContent) {
    let html = '<h4>🌿 Offline Organic Tips:</h4><ul>';
    OFFLINE_ADVICE.organic_tips.forEach(tip => {
      html += `<li>${tip}</li>`;
    });
    html += '</ul>';
    html += `<p><strong>Markets:</strong> ${OFFLINE_ADVICE.markets.telangana}</p>`;
    adviceContent.innerHTML = html;
  }
}

// Mock sensor data for offline
function setOfflineSensors() {
  const sensors = {
    'soil-moisture': 50,
    'temperature': 25,
    'ph-level': 7.0,
    'npk-n': 40,
    'npk-p': 20,
    'npk-k': 30,
    'ec': 1.0,
    'co2': 400
  };
  Object.entries(sensors).forEach(([id, value]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  });
}

// Mock weather
function setOfflineWeather() {
  document.getElementById('current-temp').textContent = '28°C';
  document.getElementById('humidity').textContent = '65%';
  document.getElementById('rainfall').textContent = '5mm';
  document.getElementById('wind-speed').textContent = '12km/h';
  document.getElementById('forecast').textContent = 'Partly Cloudy';
}

// Network status listeners
window.addEventListener('online', () => {
  location.reload();
});

window.addEventListener('offline', checkOffline);

// Init on load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', checkOffline);
} else {
  checkOffline();
}

// Override fetch for offline fallbacks
const originalFetch = window.fetch;
window.fetch = function(...args) {
  if (!navigator.onLine) {
    console.log('Offline - using fallback');
    return Promise.reject(new Error('Offline'));
  }
  return originalFetch.apply(this, args);
};
