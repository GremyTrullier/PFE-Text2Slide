# -*- coding: utf-8 -*-
"""
@author: MARTIN Tancrède tancrede.martin@efrei.net

Il faut avoir téléchargé par avance le chromedriver de votre 
version de Chrome et l'avoir placé dans le "path" indiqué.
"""
from time import sleep, gmtime, strftime
init_t = strftime("%Y%m%d-%H%M%S", gmtime())
#print('Initiated at ' + init_t + ' ....')
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import requests
import os

""" Préparation """
# Préparer le chromedriver
path = "C:\\Users\\sdael\\Documents\\Cours\\M2\\PFE\\"
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome(path+'chromedriver.exe', chrome_options=options)
driver.set_window_position(10000, 0) # Pour cacher la fenêtre (on la voit quand même quelques secondes)

# Préparer le répertoire d'enregistrement des images.
save_directory = 'Images\\'
if not os.path.isdir( save_directory ): os.mkdir( save_directory )

""" Recherche """
extensions = ['.jpg', '.png']
keywords = [ 'soccer' ]
for key in keywords:
    url = 'https://pixabay.com/images/search/%s'%key
    driver.get(url)
    sleep(1)
    
    # Retrouver la liste des images
    elem = driver.find_element_by_tag_name("body") 
    key1 = '//*[@id="content"]'
    page = elem.find_elements_by_xpath(key1)[0]
    key2 = '//*[@class="item"]'
    imgs = page.find_elements_by_xpath( key2 )
    print(len(imgs))
    # Pour chaque image...
    for imgIdx in range(5): # Nous ne prenons que les 5 premières images après les 12 premières (qui sont payantes donc innacessibles)
        img = imgs[imgIdx+12]
        html_src = img.get_attribute('innerHTML')
        save_fname = save_directory+'[%s]-%03d'%(key,imgIdx) # Nom de l'image sauvegardée
        
        # Pour chacune des extensions demandées (.png et .jpg)
        for form in extensions:
            if html_src.find(form) > 0: # L'image est soit png soit jpg. On évite d'aller plus loin si on cherche la mauvaise extension.
                
                url = html_src.split(form)[-2].split('="')[-1]+form
                if url[0] =='/': url= 'https:'+url # Visiblement il est arrivé que certains url n'ont pas le https, donc je prends une précaution.
                
                # Ecriture du fichiers
                try:
                    r = requests.get(url, stream = True)
                    with open(save_fname+form, "wb") as file:
                        for block in r.iter_content(chunk_size=1024):
                            if block: file.write(block)
                except:
                    print('failed! [%s]'%url)

driver.close()