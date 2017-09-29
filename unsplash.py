from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import os,re
import time
from selenium import webdriver
import threading


class Unsplash(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.links = []
        self.url = "https://unsplash.com"
        self.driver = webdriver.Chrome()

    # def load_page(self):
    #     #all_page_url = []
    #     self.driver.get(self.url)
    #     time.sleep(10)
    #     print('正在下拉%s次！')
    #     self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    #     print('等待%s次网页加载！')
    #     time.sleep(10)
    #     print('下拉完成，正在获取链接')
    #     all_html = self.driver.page_source
    #     bsObj = BeautifulSoup(all_html, 'html.parser')
    #     img_srcs = bsObj.find_all("a",{"class": "_23lr1"})
    #     for img_src in img_srcs:
    #         print(img_src["href"])
        #return img_src
        # # for img_src in all_img_src:
        # #     all_page_url.append(self.url + str(img_src['href']))
        # # print (all_page_url)
        # print (img_src)

    def get_photo_links(self):
        self.driver.get(self.url)
        time.sleep(10)
        print('页面正在下拉！')
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight/2);')
        print('等待网页加载！')
        time.sleep(10)
        print('下拉完成，正在获取链接')
        html = self.driver.page_source
        try:
            bs = BeautifulSoup(html,"html.parser")
            links = bs.find_all("a",{"class": "_23lr1"})
        except:
            self.driver.quit()

        for link in links:
            link = self.url + "/photos/" + link["href"][8:] + "/download"
            if link not in self.links:
                print (link)
                self.links.append(link)
                self.save_to_file(link)
        while len(self.links) <= 100:
            self.get_photo_links()
        print(self.links)
        self.driver.quit()
    def save_to_file(self,url):
        # html = urlopen(url)
        # bs = BeautifulSoup(html, "html.parser")
        # metas = bs.find_all("meta")
        # for meta in metas:
        #     if "name" in meta.attrs:
        #         if meta["name"] == "twitter:image":
        #             img_url = meta["content"]
        path_sata = "d:/"
        root_dir = "image"
        date = time.strftime("%Y_%m_%d",time.localtime())
        try:
            os.chdir(path_sata)
        except OSError:
            return "there is no such path"
        else:
            if root_dir not in os.listdir():
                os.mkdir(root_dir)
            os.chdir(path_sata + "/" + root_dir)

            if date not in os.listdir():
                os.mkdir(date)
            os.chdir(path_sata + "/" + root_dir + "/" + date)
            name = re.split("/",url)[-2]
            f = open(name + ".jpg","wb")
            f.write(requests.get(url).content)
            f.close()


# for i in range(3):
#     t= Unsplash()
#     t.start()
#     t.join(t.get_photo_links())

#unsplash.load_page()

#>>>{"href": re.compile("https://unsplash.com/\?photo=\w+")}"href": re.compile("/photos/\w+ ")
#unsplash.all_url(1)
# os.chdir("d:/image/")
if __name__ == "__main__":
    unsplash = Unsplash()
    unsplash.get_photo_links()

#unsplash.load_page()