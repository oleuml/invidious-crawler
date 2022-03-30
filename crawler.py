import argparse
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Invidious Channel Video Crawler')
  parser.add_argument('-c', '--channel-path', dest='channel', type=str, help='The channel path from where to be crawled.', required=True)
  parser.add_argument('-r', '--indious-url', dest='url', type=str, help='Output folder.', required=True)
  args = parser.parse_args()

  url = args.url + args.channel
  while True:
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a'):
      if a["href"].startswith("/watch?v") and len(a.find_all("p")) == 2:
        a["href"] = args.url + a["href"]
        a.find("img")["src"] = args.url + a.find("img")["src"] 
        print(f"- [ ] [{a.find_all('p')[1].text} -- {a.find_all('p')[0].text}]({a['href']})")
    if len(list(filter(lambda a: a["href"].startswith(args.channel + "?page=") and "Next page" in a.text, soup.find_all('a')))) == 0:
      break
    else:
      url = args.url + list(filter(lambda a: a["href"].startswith(args.channel + "?page=") and "Next page" in a.text, soup.find_all('a')))[0]["href"]
