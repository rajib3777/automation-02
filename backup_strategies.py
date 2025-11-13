"""
Backup Strategies for Wafid Booking Bot
Provides multiple fallback mechanisms and alternative approaches
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass
from enum import Enum

class BrowserType(Enum):
    CHROME_STEALTH = "chrome_stealth"
    CHROME_MOBILE = "chrome_mobile"
    FIREFOX_STANDARD = "firefox_standard"
    CHROME_MINIMAL = "chrome_minimal"

class FormFillStrategy(Enum):
    DIRECT_INPUT = "direct_input"
    JAVASCRIPT_INJECTION = "javascript_injection"
    ACTION_CHAINS = "action_chains"
    KEYBOARD_SIMULATION = "keyboard_simulation"

@dataclass
class BrowserConfig:
    browser_type: BrowserType
    options: List[str]
    user_agent: str
    window_size: Tuple[int, int]
    success_rate: float = 0.0
    last_used: Optional[str] = None

class BackupStrategies:
    def __init__(self, socketio_instance=None):
        self.socketio = socketio_instance
        self.browser_configs = self.initialize_browser_configs()
        self.form_strategies = [
            FormFillStrategy.DIRECT_INPUT,
            FormFillStrategy.ACTION_CHAINS,
            FormFillStrategy.JAVASCRIPT_INJECTION,
            FormFillStrategy.KEYBOARD_SIMULATION
        ]
        self.current_strategy_index = 0
        self.network_retry_configs = self.initialize_network_configs()
        
    def emit_update(self, message: str, level: str = "info"):
        """Send real-time updates to dashboard"""
        if self.socketio:
            self.socketio.emit('backup_strategy_update', {
                "message": message,
                "level": level,
                "timestamp": time.strftime("%H:%M:%S")
            })
    
    def initialize_browser_configs(self) -> List[BrowserConfig]:
        """Initialize different browser configurations as backups"""
        configs = []
        
        # Chrome Stealth Mode (Primary)
        stealth_options = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",
            "--disable-javascript",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        configs.append(BrowserConfig(
            browser_type=BrowserType.CHROME_STEALTH,
            options=stealth_options,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            window_size=(1920, 1080)
        ))
        
        # Chrome Mobile Emulation (Backup 1)
        mobile_options = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]
        configs.append(BrowserConfig(
            browser_type=BrowserType.CHROME_MOBILE,
            options=mobile_options,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            window_size=(375, 812)
        ))
        
        # Firefox Standard (Backup 2)
        firefox_options = [
            "--width=1920",
            "--height=1080"
        ]
        configs.append(BrowserConfig(
            browser_type=BrowserType.FIREFOX_STANDARD,
            options=firefox_options,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            window_size=(1920, 1080)
        ))
        
        # Chrome Minimal (Backup 3)
        minimal_options = [
            "--headless",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor"
        ]
        configs.append(BrowserConfig(
            browser_type=BrowserType.CHROME_MINIMAL,
            options=minimal_options,
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            window_size=(1366, 768)
        ))
        
        return configs
    
    def initialize_network_configs(self) -> List[Dict]:
        """Initialize different network retry configurations"""
        return [
            {
                "name": "Standard",
                "timeout": 10,
                "page_load_timeout": 30,
                "implicit_wait": 5,
                "retry_delay": 2
            },
            {
                "name": "Patient",
                "timeout": 20,
                "page_load_timeout": 60,
                "implicit_wait": 10,
                "retry_delay": 5
            },
            {
                "name": "Aggressive",
                "timeout": 5,
                "page_load_timeout": 15,
                "implicit_wait": 2,
                "retry_delay": 1
            }
        ]
    
    def create_driver_with_config(self, config: BrowserConfig) -> webdriver:
        """Create a WebDriver instance with specified configuration"""
        try:
            self.emit_update(f"🔄 Initializing {config.browser_type.value} browser configuration")
            
            if config.browser_type == BrowserType.FIREFOX_STANDARD:
                # Firefox configuration
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--headless")
                for option in config.options:
                    firefox_options.add_argument(option)
                
                firefox_options.set_preference("general.useragent.override", config.user_agent)
                firefox_options.set_preference("network.http.connection-timeout", 60)
                firefox_options.set_preference("network.http.response.timeout", 60)
                
                driver = webdriver.Firefox(options=firefox_options)
                
            else:
                # Chrome configurations
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                
                for option in config.options:
                    chrome_options.add_argument(option)
                
                # Additional anti-detection measures
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # Mobile emulation for mobile config
                if config.browser_type == BrowserType.CHROME_MOBILE:
                    mobile_emulation = {
                        "deviceMetrics": {
                            "width": config.window_size[0],
                            "height": config.window_size[1],
                            "pixelRatio": 3.0
                        },
                        "userAgent": config.user_agent
                    }
                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                
                driver = webdriver.Chrome(options=chrome_options)
            
            # Set window size
            driver.set_window_size(*config.window_size)
            
            # Execute stealth scripts for Chrome
            if "chrome" in config.browser_type.value:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": config.user_agent})
            
            self.emit_update(f"✅ Successfully initialized {config.browser_type.value}")
            return driver
            
        except Exception as e:
            self.emit_update(f"❌ Failed to initialize {config.browser_type.value}: {str(e)}", "error")
            raise
    
    def fill_form_with_strategy(self, driver, form_fields: Dict, strategy: FormFillStrategy) -> bool:
        """Fill form using specified strategy"""
        try:
            self.emit_update(f"📝 Using {strategy.value} form filling strategy")
            wait = WebDriverWait(driver, 15)
            
            if strategy == FormFillStrategy.DIRECT_INPUT:
                return self._fill_form_direct(driver, form_fields, wait)
            elif strategy == FormFillStrategy.JAVASCRIPT_INJECTION:
                return self._fill_form_javascript(driver, form_fields)
            elif strategy == FormFillStrategy.ACTION_CHAINS:
                return self._fill_form_action_chains(driver, form_fields, wait)
            elif strategy == FormFillStrategy.KEYBOARD_SIMULATION:
                return self._fill_form_keyboard(driver, form_fields, wait)
            
        except Exception as e:
            self.emit_update(f"❌ {strategy.value} strategy failed: {str(e)}", "error")
            return False
    
    def _fill_form_direct(self, driver, form_fields: Dict, wait: WebDriverWait) -> bool:
        """Standard direct input method"""
        try:
            # Country selection
            country_dropdown = wait.until(EC.element_to_be_clickable((By.NAME, "country")))
            Select(country_dropdown).select_by_visible_text(form_fields['country'])
            time.sleep(random.uniform(1, 2))
            
            # City selection
            city_dropdown = wait.until(EC.element_to_be_clickable((By.NAME, "city")))
            Select(city_dropdown).select_by_visible_text(form_fields['city'])
            time.sleep(random.uniform(1, 2))
            
            # Fill text fields
            text_fields = [
                ("country_traveling_to", form_fields.get('country_traveling_to', '')),
                ("first_name", form_fields.get('first_name', '')),
                ("last_name", form_fields.get('last_name', '')),
                ("passport_no", form_fields.get('passport_number', '')),
                ("email", form_fields.get('email_address', '')),
                ("phone", form_fields.get('phone_no', ''))
            ]
            
            for field_name, value in text_fields:
                if value:
                    try:
                        element = driver.find_element(By.NAME, field_name)
                        element.clear()
                        element.send_keys(value)
                        time.sleep(random.uniform(0.5, 1))
                    except Exception:
                        continue
            
            return True
            
        except Exception as e:
            self.emit_update(f"Direct input failed: {str(e)}")
            return False
    
    def _fill_form_javascript(self, driver, form_fields: Dict) -> bool:
        """JavaScript injection method"""
        try:
            # Use JavaScript to fill form fields directly
            js_script = """
            function fillField(name, value) {
                var element = document.querySelector('[name="' + name + '"]');
                if (element) {
                    element.value = value;
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
            """
            
            driver.execute_script(js_script)
            
            # Fill fields using JavaScript
            fields_to_fill = [
                ("country_traveling_to", form_fields.get('country_traveling_to', '')),
                ("first_name", form_fields.get('first_name', '')),
                ("last_name", form_fields.get('last_name', '')),
                ("passport_no", form_fields.get('passport_number', '')),
                ("email", form_fields.get('email_address', '')),
                ("phone", form_fields.get('phone_no', ''))
            ]
            
            for field_name, value in fields_to_fill:
                if value:
                    driver.execute_script(f"fillField('{field_name}', '{value}');")
                    time.sleep(random.uniform(0.2, 0.5))
            
            # Handle dropdowns with JavaScript
            if form_fields.get('country'):
                driver.execute_script(f"""
                    var countrySelect = document.querySelector('[name="country"]');
                    if (countrySelect) {{
                        var options = countrySelect.options;
                        for (var i = 0; i < options.length; i++) {{
                            if (options[i].text === '{form_fields["country"]}') {{
                                countrySelect.selectedIndex = i;
                                countrySelect.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                break;
                            }}
                        }}
                    }}
                """)
            
            return True
            
        except Exception as e:
            self.emit_update(f"JavaScript injection failed: {str(e)}")
            return False
    
    def _fill_form_action_chains(self, driver, form_fields: Dict, wait: WebDriverWait) -> bool:
        """Action chains method for more human-like interaction"""
        try:
            actions = ActionChains(driver)
            
            # Country selection with action chains
            country_dropdown = wait.until(EC.element_to_be_clickable((By.NAME, "country")))
            actions.move_to_element(country_dropdown).click().perform()
            time.sleep(1)
            
            # Type to search for country
            actions.send_keys(form_fields['country'][:3]).perform()
            time.sleep(1)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(2)
            
            # Similar approach for other fields
            text_fields = [
                ("first_name", form_fields.get('first_name', '')),
                ("last_name", form_fields.get('last_name', '')),
                ("passport_no", form_fields.get('passport_number', ''))
            ]
            
            for field_name, value in text_fields:
                if value:
                    try:
                        element = driver.find_element(By.NAME, field_name)
                        actions.move_to_element(element).click().perform()
                        time.sleep(0.5)
                        
                        # Clear field and type slowly
                        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                        time.sleep(0.2)
                        
                        for char in value:
                            actions.send_keys(char).perform()
                            time.sleep(random.uniform(0.05, 0.15))  # Human-like typing
                            
                    except Exception:
                        continue
            
            return True
            
        except Exception as e:
            self.emit_update(f"Action chains failed: {str(e)}")
            return False
    
    def _fill_form_keyboard(self, driver, form_fields: Dict, wait: WebDriverWait) -> bool:
        """Keyboard simulation method"""
        try:
            # Tab through form and fill fields
            body = driver.find_element(By.TAG_NAME, "body")
            body.click()
            
            # Use tab navigation to reach form fields
            for _ in range(10):  # Tab to first form field
                ActionChains(driver).send_keys(Keys.TAB).perform()
                time.sleep(0.1)
            
            # Fill country field
            ActionChains(driver).send_keys(form_fields['country']).perform()
            time.sleep(1)
            ActionChains(driver).send_keys(Keys.TAB).perform()
            
            # Fill city field  
            ActionChains(driver).send_keys(form_fields['city']).perform()
            time.sleep(1)
            
            # Continue with other fields
            field_values = [
                form_fields.get('country_traveling_to', ''),
                form_fields.get('first_name', ''),
                form_fields.get('last_name', ''),
                form_fields.get('passport_number', '')
            ]
            
            for value in field_values:
                ActionChains(driver).send_keys(Keys.TAB).perform()
                time.sleep(0.5)
                if value:
                    ActionChains(driver).send_keys(value).perform()
                    time.sleep(0.5)
            
            return True
            
        except Exception as e:
            self.emit_update(f"Keyboard simulation failed: {str(e)}")
            return False
    
    def get_next_browser_config(self) -> BrowserConfig:
        """Get the next browser configuration to try"""
        # Sort by success rate (highest first)
        sorted_configs = sorted(self.browser_configs, key=lambda x: x.success_rate, reverse=True)
        
        # Return the best performing config that hasn't been used recently
        for config in sorted_configs:
            return config
        
        # Fallback to first config
        return self.browser_configs[0]
    
    def get_next_form_strategy(self) -> FormFillStrategy:
        """Get the next form filling strategy to try"""
        strategy = self.form_strategies[self.current_strategy_index]
        self.current_strategy_index = (self.current_strategy_index + 1) % len(self.form_strategies)
        return strategy
    
    def update_config_success_rate(self, config: BrowserConfig, success: bool):
        """Update success rate for a browser configuration"""
        # Simple success rate calculation (can be enhanced with more sophisticated tracking)
        if hasattr(config, 'attempts'):
            config.attempts += 1
        else:
            config.attempts = 1
            config.successes = 0
        
        if success:
            config.successes += 1
        
        config.success_rate = (config.successes / config.attempts) * 100
        config.last_used = time.strftime("%H:%M:%S")
    
    def apply_network_resilience(self, driver, config_index: int = 0):
        """Apply network resilience settings"""
        try:
            network_config = self.network_retry_configs[config_index]
            
            driver.set_page_load_timeout(network_config["page_load_timeout"])
            driver.implicitly_wait(network_config["implicit_wait"])
            
            self.emit_update(f"🌐 Applied {network_config['name']} network configuration")
            
        except Exception as e:
            self.emit_update(f"Network resilience setup failed: {str(e)}", "warning")
    
    def detect_and_handle_captcha(self, driver) -> Tuple[bool, str]:
        """Detect CAPTCHA and provide handling guidance"""
        try:
            page_source = driver.page_source.lower()
            captcha_indicators = [
                "captcha", "recaptcha", "hcaptcha", 
                "robot", "verify", "security check",
                "i'm not a robot", "prove you're human"
            ]
            
            for indicator in captcha_indicators:
                if indicator in page_source:
                    self.emit_update("🤖 CAPTCHA detected - Manual intervention required", "warning")
                    
                    # Try to find CAPTCHA iframe or container
                    captcha_elements = driver.find_elements(By.CSS_SELECTOR, 
                        "iframe[src*='captcha'], .captcha, #captcha, [class*='captcha']")
                    
                    if captcha_elements:
                        return True, "CAPTCHA element found on page - manual solving required"
                    else:
                        return True, "CAPTCHA detected in page content"
            
            return False, "No CAPTCHA detected"
            
        except Exception as e:
            return False, f"CAPTCHA detection error: {str(e)}"
    
    def get_backup_summary(self) -> Dict:
        """Get summary of backup configurations and their performance"""
        summary = {
            "browser_configs": [],
            "form_strategies": [strategy.value for strategy in self.form_strategies],
            "network_configs": [config["name"] for config in self.network_retry_configs]
        }
        
        for config in self.browser_configs:
            summary["browser_configs"].append({
                "type": config.browser_type.value,
                "success_rate": f"{config.success_rate:.1f}%",
                "last_used": config.last_used or "Never"
            })
        
        return summary