"""
Cloud Deployment Configuration for Ultra-Powerful Wafid Automation Tool
"""

import os

class CloudConfig:
    # Environment detection
    IS_CLOUD_DEPLOYMENT = os.getenv('PORT') is not None
    IS_RENDER = os.getenv('RENDER') is not None
    IS_HEROKU = os.getenv('DYNO') is not None
    
    # Chrome/ChromeDriver paths for cloud
    CHROME_BIN = os.getenv('CHROME_BIN', '/usr/bin/google-chrome')
    CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
    
    # Cloud-optimized settings
    MAX_CONCURRENT_BROWSERS = 2 if IS_CLOUD_DEPLOYMENT else 8
    HEADLESS_MODE = True if IS_CLOUD_DEPLOYMENT else False
    REDUCED_LOGGING = True if IS_CLOUD_DEPLOYMENT else False
    
    # Memory optimization for cloud
    BROWSER_TIMEOUT = 30 if IS_CLOUD_DEPLOYMENT else 60
    PAGE_LOAD_TIMEOUT = 15 if IS_CLOUD_DEPLOYMENT else 30
    
    @staticmethod
    def get_chrome_options():
        """Get Chrome options optimized for cloud deployment"""
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        
        if CloudConfig.IS_CLOUD_DEPLOYMENT:
            # Cloud-specific options
            cloud_options = [
                "--headless",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-extensions",
                "--disable-plugins",
                "--disable-images",
                "--disable-javascript",
                "--virtual-time-budget=5000",
                "--run-all-compositor-stages-before-draw",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--disable-client-side-phishing-detection",
                "--disable-crash-reporter",
                "--disable-oopr-debug-crash-dump",
                "--no-crash-upload",
                "--disable-low-res-tiling",
                "--memory-pressure-off",
                "--max_old_space_size=4096",
                "--single-process"
            ]
            
            for option in cloud_options:
                options.add_argument(option)
            
            # Set binary location if specified
            if CloudConfig.CHROME_BIN:
                options.binary_location = CloudConfig.CHROME_BIN
        
        return options
