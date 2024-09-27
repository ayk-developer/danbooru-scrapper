import requests
from bs4 import BeautifulSoup as soup
import shutil

def download_image(url, filename):
  """Downloads an image from the specified URL and saves it with the given filename."""
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    with open(filename, "wb") as f:
      shutil.copyfileobj(response.raw, f)
      print(f"Downloaded image: {filename}")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading image: {url} ({e})")

def main():
  """Main function for scraping images from Danbooru."""
  tag = input("Type in the tag to scrap: ")
  page_no = int(input("Type in the amount of pages to scrap: "))

  for page in range(1, page_no + 1):
    url = f"https://danbooru.donmai.us/posts?page={page}&tags={tag}"
    print(f"Scraping Page Number {page}")

    try:
      response = requests.get(url)
      response.raise_for_status()

      soup_object = soup(response.content, 'html.parser')
      images = soup_object.find_all("article")

      for i, image in enumerate(images):
        try:
          image_url = image.find("img", {"class": "has-cropped-false"})["src"]
          download_image(image_url, image_url.split("/")[-1])
        except (KeyError, TypeError):
          try:
            image_url = image.find("img", {"class": "has-cropped-true"})["src"]
            download_image(image_url, image_url.split("/")[-1])
          except (KeyError, TypeError):
            print(f"Failed to find image URL on picture number {i}")

    except requests.exceptions.RequestException as e:
      print(f"Error scraping page {page}: {e}")

if __name__ == "__main__":
  main()
