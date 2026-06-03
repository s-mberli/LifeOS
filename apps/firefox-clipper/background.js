// background.js

chrome.action.onClicked.addListener(async (tab) => {
  if (!tab.url) {
    console.error("No URL found for the active tab.");
    return;
  }

  console.log(`Sending URL to MarkusOS: ${tab.url}`);

  // Create a minimal visual indicator on the extension icon
  chrome.action.setBadgeText({ text: "...", tabId: tab.id });
  chrome.action.setBadgeBackgroundColor({ color: "#FFD700", tabId: tab.id });

  try {
    const response = await fetch("http://localhost:8000/ingest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: tab.url })
    });

    if (response.ok) {
      console.log("Successfully sent to MarkusOS.");
      chrome.action.setBadgeText({ text: "OK", tabId: tab.id });
      chrome.action.setBadgeBackgroundColor({ color: "#4CAF50", tabId: tab.id });
    } else {
      console.error(`Failed to send. Status: ${response.status}`);
      chrome.action.setBadgeText({ text: "ERR", tabId: tab.id });
      chrome.action.setBadgeBackgroundColor({ color: "#F44336", tabId: tab.id });
    }
  } catch (error) {
    console.error("Error communicating with MarkusOS API:", error);
    chrome.action.setBadgeText({ text: "ERR", tabId: tab.id });
    chrome.action.setBadgeBackgroundColor({ color: "#F44336", tabId: tab.id });
  }

  // Clear badge after 3 seconds
  setTimeout(() => {
    chrome.action.setBadgeText({ text: "", tabId: tab.id });
  }, 3000);
});
