import pytest
from playwright.sync_api import Page

@pytest.mark.parametrize("latitude, longitude", [
    (40.7128, -74.0060),
    (48.8566, 2.3522),
    (35.6895, 139.6917),
    (52.2298, 21.0122)
])
def test_real_geolocation(page: Page, latitude, longitude):
    context = page.context
    context.grant_permissions(["geolocation"])
    context.set_geolocation({"latitude":latitude, "longitude":longitude})

    page.goto("https://my-location.org")
    page.evaluate("document.querySelector('#iplocation').innerText='ip hidden'")

    try:
        page.get_by_role("button", name="Consent").click()
        print("Cookies accepted")
    except:
        print("No cookies button found")

    page.wait_for_timeout(5000)

    try:
        detect_location = page.locator("#address").all_text_contents()
        print(f"Detected location: {detect_location}")
    except:
        print("Unable to retrieve the location name")
