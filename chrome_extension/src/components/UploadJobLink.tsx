import { Send } from '@mui/icons-material';
import LinkIcon from '@mui/icons-material/Link';
import { Button } from '@mui/material';
import { useState } from 'react';
import SuccessPopup from './SuccessPopup';

const submitURL = async (url: string) => {
  // Open the tab
  chrome.tabs.create({ url }, async (tab) => {
    // Wait for the tab to finish loading
    const tabId = tab.id;

    if (!tabId) return;

    // Optional: poll until tab is ready
    const waitForLoad = () =>
      new Promise<void>((resolve) => {
        const checkTab = () => {
          chrome.tabs.get(tabId, (updatedTab) => {
            if (updatedTab.status === "complete") {
              resolve();
            } else {
              setTimeout(checkTab, 500);
            }
          });
        };
        checkTab();
      });

    await waitForLoad();

    // Inject the script dynamically
    chrome.scripting.executeScript({
      target: { tabId },
      files: ["js/scrapeScript.js"]
    });
  });
}

function UploadJobLink() {
    const [inputValue, setInputValue] = useState('');
    const [success, setSuccess] = useState(false);

    const handleSubmit = (e: React.FormEvent) =>{
        e.preventDefault();
        submitURL(inputValue);
        setInputValue('');
        setSuccess(true);
    };

    const handleCloseSuccess = () => {
      setSuccess(false);
    }

    return (
        <div className="flex flex-col items-center justify-center space-y-6 pt-12">
          <LinkIcon className="w-64 h-64 text-gray-400" />
          <div className="text-center space-y-2">
            <h1 className="text-xl font-semibold text-gray-900">
              Upload a Job Link
            </h1>
            <p className="text-gray-600">
              By uploading a job link, we will scrape the job descriptions and craft personalized interview guidance.
            </p>
          </div>

          <div className="w-full max-w-md">
                <form onSubmit={handleSubmit} className="flex flex-col gap-2">
                  <div className="flex">
                    <div className="flex-1 relative flex-row">
                        <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                        placeholder="Input Job posting URL..."
                        />
                    </div>
                    <Button
                        type="submit" 
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg"
                        endIcon={<Send />}
                    >
                        <span>Upload</span>
                    </Button>
                  </div>
                </form>
          </div>
          <SuccessPopup
            open={success}
            message="URL uploaded successfully!"
            onClose={handleCloseSuccess}
            duration={6000}
          />
        </div>
    );
}

export default UploadJobLink;
