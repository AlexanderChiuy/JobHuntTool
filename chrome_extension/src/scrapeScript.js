async function getAuthToken() {
    const tryGetToken = () => {
      return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage({ action: "getAuthToken" }, (response) => {
          if (response && response.token) {
            resolve(response.token);
          } else {
            reject(response && response.error);
          }
        });
      });
    };
  
    try {
      return await tryGetToken();
    } catch (error) {
      console.error("Error getting auth token, retrying:", error);
      // Wait 1 second before retrying
      await new Promise((res) => setTimeout(res, 1000));
      return tryGetToken();
    }
}

function extractRelevantHTMLFromDOM() {
    const allowedTags = ['span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    const elements = Array.from(document.querySelectorAll(allowedTags.join(',')));
    return elements
        .map(el => el.innerText.trim())
        .filter(text => text.length > 0);
}

// Need to set a timeout because we need some time for page to load
setTimeout(async () => {
    try {
        const filteredHTML = extractRelevantHTMLFromDOM();
        const token = await getAuthToken();

        await fetch("http://127.0.0.1:8080/company/company-job-url-crew-ai", {
        method: "POST",
        body: JSON.stringify({ "job_post_url": filteredHTML.join(" ") }),
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
        });

    } catch (error) {
        console.error("Failed to send DOM:", error);
    }
}, 3000);
