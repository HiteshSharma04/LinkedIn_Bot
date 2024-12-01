from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

EMAIL = "email@ur.com"
PASSWORD = "pass"
ADD = "https://www.linkedin.com/jobs/search?keywords=Python%20Developer&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

def abort_application():
    try:
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Dismiss']"))
        )
        dismiss_button.click()
    except Exception as e:
        print("Abort button not found:", e)

try:
    driver.get(ADD)
    wait = WebDriverWait(driver, 10)

    # Dismiss the sign-in modal if present
    try:
        dismiss_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".contextual-sign-in-modal__modal-dismiss-icon"))
        )
        dismiss_button.click()
        print("Sign-in modal dismissed.")
    except Exception as e:
        print("Sign-in modal not present or already dismissed.")

    # Click the sign-in button
    try:
        sign_in_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".job-alert-redirect-section__cta"))
        )
        sign_in_button.click()
        print("Sign-in button clicked.")
    except Exception as e:
        print("Sign-in button not found or not clickable.")

    # Click the sign-in form button
    try:
        sign_in_form_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sign-in-form__sign-in-cta"))
        )
        sign_in_form_button.click()
        print("Sign-in form button clicked.")
    except Exception as e:
        print("Sign-in form button not found or not clickable.")

    # Enter credentials
    time.sleep(5)
    name = driver.find_element(By.NAME, "session_key")
    name.send_keys(EMAIL)
    passwd = driver.find_element(By.NAME, "session_password")
    passwd.send_keys(PASSWORD, Keys.ENTER)

    # Click filter button
    try:
        filter_b = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-reusables__filter-binary-toggle"))
        )
        filter_b.click()
        print("Filter click successful.")
    except Exception as e:
        print("Filter button not working.")

    # Process each job listing
    all_listings = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable"))
    )
    for listing in all_listings:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", listing)
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(listing)).click()
            print("Opening Listing")
            time.sleep(2)
            try:
                # Click Apply Button
                apply_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button"))
                )
                apply_button.click()
                print("Job applied!")
            except Exception as e:
                print("Apply button not clickable: ", e)

            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")
                if submit_button.get_attribute("data-control-name") == "continue_unify":
                    abort_application()
                    print("Complex application, skipped.")
                    continue
                else:
                    # Click Submit Button
                    print("Submitting job application")
                    submit_button.click()
                    cross_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".artdeco-modal__dismiss"))
                    )
                    cross_button.click()
                    print("dismissed.")
            except Exception as e:
                print("Unable to submit application:", e)
                
        except Exception as e:
            print("Listing click failed, retrying:", e)
            # Refresh list of job listings and retry
            all_listings = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable"))
            )
            for retry_listing in all_listings:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", retry_listing)
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(retry_listing)).click()
                    print("Retrying Listing Click")
                    time.sleep(2)
                    try:
                        # Click Apply Button
                        apply_button = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button"))
                        )
                        apply_button.click()
                        print("Job applied!")
                    except Exception as e:
                        print("Apply button not clickable: ", e)
                except Exception as retry_exception:
                    print("Retry failed:", retry_exception)

finally:
    # Optional: Close the browser after operations
    pass