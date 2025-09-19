// Initialize map
var map = L.map('map').setView([20.5937, 78.9629], 5);

// Base layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
}).addTo(map);

// Example heatmap data
var trafficData = [
  [28.7041, 77.1025, 1],
  [19.0760, 72.8777, 0.8],
  [13.0827, 80.2707, 0.6],
  [22.5726, 88.3639, 0.4],
  [12.9716, 77.5946, 0.2]
];

// Add heatmap
var heatLayer = L.heatLayer(trafficData, {
  radius: 25,
  blur: 15,
  maxZoom: 17,
  gradient: {0.2: 'green', 0.6: 'yellow', 1.0: 'red'}
}).addTo(map);

// Function to search location
function searchLocation() {
  let query = document.getElementById("searchBox").value;

  if (!query) {
    alert("Please enter a location!");
    return;
  }

  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`)
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        let lat = parseFloat(data[0].lat);
        let lon = parseFloat(data[0].lon);

        // Move map to location
        map.setView([lat, lon], 14);

        // Add marker
        L.marker([lat, lon]).addTo(map)
          .bindPopup(`<b>${query}</b>`)
          .openPopup();
      } else {
        alert("Location not found!");
      }
    })
    .catch(err => console.error("Error fetching location:", err));
}
