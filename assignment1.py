import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re

# Google Colab setup (if needed)
try:
    from google.colab import drive
    drive.mount('/content/drive')
    data_dir = '/content/drive/MyDrive/NeurIPS_Data'
    os.makedirs(data_dir, exist_ok=True)
except ImportError:
    data_dir = 'NeurIPSData'  # Local directory
    os.makedirs(data_dir, exist_ok=True)

def scrape_neurips_years(base_url):
    """Scrapes the main NeurIPS page to get the links for each year's proceedings."""
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        years_data = []
        year_links = soup.find_all('a', href=lambda href: href and '/paper_files/paper/' in href)

        for link in year_links:
            year_text = link.text.strip()

            # Attempt to extract year using different patterns
            match = None
            for pattern in [r'\((\d{4})\)', r'(\d{4})$', r'(\d{4})']:  # Patterns to try
                match = re.search(pattern, year_text)
                if match:
                    break

            if match:
                try:
                    year = int(match.group(1))
                    years_data.append({'year': year, 'year_link': "https://papers.nips.cc" + link['href']})
                except ValueError:
                    print(f"Invalid year format: {year_text}")
            else:
                print(f"Could not extract year from: {year_text}")

        return years_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching main page {base_url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing main page {base_url}: {e}")
        return None


def scrape_neurips_page(url, year):
    """Scrapes a single NeurIPS proceedings page for paper details."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        papers = []
        paper_elements = soup.find_all('li', class_='conference')  # Correct selector

        for paper_element in paper_elements:
            title_a = paper_element.find('a')
            if title_a:
                title = title_a.text.strip()
                link = title_a['href']
                if not link.startswith('http'):
                    link = "https://papers.nips.cc" + link

                authors_i = paper_element.find('i')
                authors = authors_i.text.strip().replace('"', '') if authors_i else "N/A"  # Remove quotes

                papers.append({'title': title, 'link': link, 'authors': authors, 'year': year})

        return papers

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
        return None

def scrape_neurips(base_url, years_to_scrape):  # The missing function!
    all_papers = []

    years_data = scrape_neurips_years(base_url)
    if not years_data:
        print("Could not fetch year links.")
        return None  # Return None if no years data is found

    for year_data in years_data:
        year = year_data['year']
        year_link = year_data['year_link']

        if year in years_to_scrape:
            print(f"Scraping {year_link}")
            papers = scrape_neurips_page(year_link, year)
            if papers:
                for paper in papers:
                    paper_details = scrape_paper_details(paper['link'])
                    if paper_details:
                        all_papers.append({**paper, **paper_details, 'year': year})  # Merge dictionaries
                    else:
                        print(f"Could not fetch details for {paper['link']}")
                time.sleep(1)  # Be nice to the server
            else:
                print(f"No papers found for {year}")
    return all_papers  # Return all_papers

def scrape_paper_details(paper_link):
    try:
        response = requests.get(paper_link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h4').text.strip() if soup.find('h4') else "N/A"  # More robust title extraction
        authors_tag = soup.find('p', string='Authors') # Find the <p> tag containing "Authors"
        authors = authors_tag.find('i').text.strip() if authors_tag and authors_tag.find('i') else "N/A"
        abstract_tag = soup.find('h4', string='Abstract')
        abstract = abstract_tag.find_next_sibling('p').text.strip() if abstract_tag and abstract_tag.find_next_sibling('p') else "N/A"

        return {'title': title, 'authors': authors, 'link': paper_link, 'abstract': abstract}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {paper_link}: {e}")
        return {'title': "N/A", 'authors': "N/A", 'link': paper_link, 'abstract': "N/A"}
    except AttributeError as e:
        print(f"Error parsing {paper_link}: {e}")
        return {'title': "N/A", 'authors': "N/A", 'link': paper_link, 'abstract': "N/A"}

  # ... (same as before)

# --- Main execution ---
base_url = "https://papers.nips.cc/"
years_to_scrape = range(2019, 2026)  # Corrected range (up to and including 2025)

all_papers = scrape_neurips(base_url, years_to_scrape)  # Now it's defined!

if all_papers:
    print(f"Total papers scraped: {len(all_papers)}")
    all_years_df = pd.DataFrame(all_papers)
    all_years_csv = os.path.join(data_dir, "neurips_all_years.csv")
    all_years_df.to_csv(all_years_csv, index=False, encoding='utf-8')
    print(f"All years' data saved to {all_years_csv}")
    try:
        from google.colab import files
        files.download(all_years_csv)
    except ImportError:
        print("Not in Google Colab environment, cannot download file.")
else:
    print("No papers were scraped or an error occurred.")
