function checkPhishing(url) {
  fetch('http://localhost:8501/api/detect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: url }),
  })
  .then(response => response.json())
  .then(data => {
    const statusDiv = document.getElementById('status');
    
    if (data.is_phishing) {
      statusDiv.textContent = '⚠️ Phishing Detected!';
      statusDiv.className = 'phishing';
      
      // Show which model flagged it (optional)
      const details = `Model 1: ${data.model_1_result}, Model 2: ${data.model_2_result}`;
      console.log(details); // Or display in the popup
    } else {
      statusDiv.textContent = '✅ Safe Website';
      statusDiv.className = 'safe';
    }
  })
  .catch(error => {
    console.error('Error:', error);
    document.getElementById('status').textContent = 'Error analyzing URL';
  });
}