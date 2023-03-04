import time
 
import pandas as pd
import difflib
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
 
def commonModelReplacements(modelName):
    model = modelName.replace("chevy", "chevrolet")
    model = modelName.replace("vw ", "volkswagen")
    return model

def commonMakeReplacements(make):
    model = make.replace("f-150", "f150")
    model = make.replace("f-250", "f250")
    model = make.replace("f-350", "f350")
    return make

def getVehicleDBMatchNew(make,rawModel,modelList):
    print(f"{make} {rawModel} {modelList}")

def getVehicleDBMatch(make, rawmodel, modelList):
    print("trying to match vehicle...")
    cutoff=0.7
    decay=0.9
    model = commonReplacements(model)
    matches = difflib.get_close_matches(model,modeldf, cutoff=0.7)
    i = 0
    while len(matches) != 1 and cutoff < 1 and cutoff > 0:
        while len(matches) > 1 and cutoff < 1:
            print(i)
            i = i + 1
            cutoff+=0.1 * decay
            decay-=0.01
            if cutoff > 1:
                break
            matches = difflib.get_close_matches(model,modeldf, cutoff=cutoff)
        while len(matches) < 1 and cutoff > 0:
            print( i)
            i = i + 1
            cutoff-=0.1 * decay
            decay-=0.01
            if cutoff < 1:
                break
            matches = difflib.get_close_matches(model,modeldf, cutoff=cutoff)

    print(f"cuttof: {cutoff}")
    print(matches)
    if len(matches) > 0:
        return(matches[0])
    else:
        return("NO_MATCH")
def addVehicleToCSVBackend(parsedVehicle, url):
    vehicledb = pd.read_csv("./cars.csv")
    vehicledf = pd.DataFrame([parsedVehicle])
    vehicledf["url"] = url
    vehicledb = pd.concat([vehicledf,vehicledb])
    vehicledb.to_csv("./cars.csv", index=False)

def parseElements(elements):
    parsed = {}
    parsed["year_make_model"] = elements[0].text
    try:
        parsed["price"] = driver.find_element(By.CLASS_NAME, "price").text[1:].replace(",","")
    except:
        pass
    listy = elements[1].find_elements(By.TAG_NAME, "span")

    for element in listy:
        if element.text[:11] == "condition: ":
            parsed["condition"] = element.text[11:]
        elif element.text[:11] == "cylinders: ":
            parsed["cylinders"] = element.text[11:]
        elif element.text[:5] == "VIN: ":
            parsed["VIN"] = element.text[5:]
        elif element.text[:7] == "drive: ":
            parsed["drive"] = element.text[7:]
        elif element.text[:6] == "fuel: ":
            parsed["fuel"] = element.text[6:]
        elif element.text[:10] == "odometer: ":
            parsed["odometer"] = element.text[10:]
        elif element.text[:13] == "paint color: ":
            parsed["paint color"] = element.text[13:]
        elif element.text[:6] == "size: ":
            parsed["size"] = element.text[6:]
        elif element.text[:14] == "title status: ":
            parsed["title status"] = element.text[14:]
        elif element.text[:14] == "transmission: ":
            parsed["transmission"] = element.text[14:]
        elif element.text[:6] == "type: ":
            parsed["type"] = element.text[6:]
    return parsed
        
def parseVehicleLinks(urllist):
    df = pd.read_csv("./cars.csv")
    savedurls = df["url"].to_list()
    uncrawledURLS = [x for x in urllist if x not in savedurls]
    for url in uncrawledURLS:
        driver.get(url)
        time.sleep(5)
        driver.save_screenshot("car.png")
        elements = driver.find_elements(By.CLASS_NAME, "attrgroup")
        addVehicleToCSVBackend(parseElements(elements), url)
        # year = elements[0].text[:4]

        # if int(year) < 1992:
        #     continue
        # model_list_df = pd.read_csv(f"./us-car-models-data/{year}.csv")
        # makes = model_list_df["make"].unique().tolist()
        # makeandmodel=elements[0].text[5:]
        # make = ""
        # for m in makes:
        #     if m.lower() in makeandmodel.lower():
        #         print(f"make is {m}")
        #         make = m
        #         rawModel = makeandmodel.lower().replace(m.lower(), "")

        # print(f"make: {make} rawModel: {rawModel}")
        # entry = [
        #          {
        #         ""
        #         "year": elements[0].text[:4],
        #         "make and model in": elements[0].text[5:],
        #         "price": price,
        #         "link": url,
        #         "matched_make": make,
        #         "rawModel": rawModel}
        #         ]
        # try:
        #     print(f"year: {year}")

        # except:
        #     continue
        # entry[0]["match"] = getVehicleDBMatchNew(make, rawModel,model_list_df.loc[model_list_df["make"] == make])
        # entry[0]
        # print(year + " " + str(entry[0]["model"]).lower())
        # df = pd.concat([pd.DataFrame(entry), df])
        # df.to_csv("./cars.csv",index=False)
def getCraigslistLinkList(driver):
    # pass the defined options and service objects to initialize the web driver
    url = "https://denver.craigslist.org/search/cta?purveyor=owner#search=1~list~0~0"
    
    driver.get(url)
    time.sleep(3)
    print("done")
    driver.save_screenshot("screen.png")
    result_div = driver.find_element(By.ID, "search-results-page-1")
    results = result_div.find_elements(By.TAG_NAME, "li")
    linklist = []
    for result in results:
        linklist.append(result.find_element(By.CLASS_NAME, "titlestring").get_attribute("href"))

    return linklist
def getFacebookLinkList(driver):
    # pass the defined options and service objects to initialize the web driver
    url = "https://www.facebook.com/marketplace/denver/vehicles?sellerType=individual&exact=false"
    
    driver.get(url)
    time.sleep(3)
    print("done")
    driver.save_screenshot("screen.png")
    result_div = driver.find_elements(By.TAG_NAME, "a")
    new_res = []
    for link_element in result_div:
        if link_element.get_attribute("href")[:42] == "https://www.facebook.com/marketplace/item/":
            new_res.append(link_element)
    for item in new_res:
        print("==========")
        splititem = item.text.split("\n")
        print("price: " + splititem[0])
        if(splititem[1][:1] == "$"):
            del splititem[1]
        print("car name: " + splititem[1])
        print("location: " + splititem[2])
        if len(splititem) > 3:
            print("miles: " + splititem[3])
        # print(item.text)
        print("==========")

    # return linklist
    

if __name__ == "__main__":
        # start by defining the options
    options = webdriver.ChromeOptions()
    options.headless = True # it's more scalable to work in headless mode
    # normally, selenium waits for all resources to download
    # we don't need it as the page also populated with the running javascript code.
    options.page_load_strategy = 'none' 
    # this returns the path web driver downloaded
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    driver = Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(3)
    linklist = getFacebookLinkList(driver)
    # parseVehicleLinks(linklist)
    driver.quit()
