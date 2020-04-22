import urllib3
import certifi
import re
import sys, os

class PrometeyDownloader:

    def __init__(self):
        UA_CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        self.http = urllib3.PoolManager(10, headers={'User-Agent': UA_CHROME},
                               cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def save_video(self, url, directory, name):
        page = self.http.urlopen("GET", url)
        parser = re.compile("contentUrl\":\"(.*?)\"")
        data = str(page.data)
        links = parser.findall(data)
        if len(links) > 0:
            video = self.http.urlopen("GET", links[0]).data
        self.__prepare_directory(directory)
        with open(os.path.join(directory, name), 'wb') as f:
            f.write(video)

    def download_video(self, url):
        page = self.http.urlopen("GET", url)
        parser = re.compile("contentUrl\":\"(.*?)\"")
        data = str(page.data)
        links = parser.findall(data)
        if len(links) > 0:
            return self.http.urlopen("GET", links[0]).data




    def __prepare_directory(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)



if __name__ == "__main__":
    print(sys.version_info)
    downloader = PrometeyDownloader()
    downloader.save_video("https://vm.tiktok.com/GLMJ8a/", 'temp', '2.mp4')
