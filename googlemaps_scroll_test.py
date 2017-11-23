from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os


def wheel_element(element, deltaY=120, offsetX=0, offsetY=0):
    error = element._parent.execute_script("""
    var element = arguments[0];
    var deltaY = arguments[1];
    var box = element.getBoundingClientRect();
    var clientX = box.left + (arguments[2] || box.width / 2);
    var clientY = box.top + (arguments[3] || box.height / 2);
    var target = element.ownerDocument.elementFromPoint(clientX, clientY);

    for (var e = target; e; e = e.parentElement) {
      if (e === element) {
        target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
        return;
      }
    }    
    return "Element is not interactable";
    """, element, deltaY, offsetX, offsetY)
    if error:
        raise WebDriverException(error)


options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars --disable-extensions --window-size=1366,768")
driver = webdriver.Chrome(chrome_options=options, executable_path=os.getcwd() + '/WebDriver/chromedriver.exe')
driver.get("https://www.google.com/maps")

# get element
elm = driver.find_element_by_css_selector("div#scene > div.widget-scene > canvas")

# zoom in with mouse wheel
wheel_element(elm, -120, 0, 0)

# zoom out with mouse wheel
wheel_element(elm, 120)
