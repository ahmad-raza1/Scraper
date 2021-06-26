import urllib.request

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open("Downloads/" + filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

if __name__ == "__main__":
    url = "https://en.unesco.org/inclusivepolicylab/sites/default/files/dummy-pdf_2.pdf"
    download_file(url, "Test")