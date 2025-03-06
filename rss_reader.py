import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import html

def fetch_rss(url):
    """Fetch RSS content from the given URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS: {e}")
        return None

def parse_rss(xml_content):
    """Parse the XML content and return structured data"""
    try:
        root = ET.fromstring(xml_content)
        
        # Get channel information
        channel = root.find('channel')
        if channel is None:
            print("No channel element found in the RSS feed.")
            return None
        
        feed_title = channel.find('title').text if channel.find('title') is not None else "No title"
        feed_description = channel.find('description').text if channel.find('description') is not None else "No description"
        
        # Get items
        items = channel.findall('item')
        parsed_items = []
        
        for item in items:
            title = item.find('title').text if item.find('title') is not None else "No title"
            link = item.find('link').text if item.find('link') is not None else "No link"
            description = item.find('description').text if item.find('description') is not None else "No description"
            pubDate = item.find('pubDate').text if item.find('pubDate') is not None else "No date"
            
            # Clean up HTML entities in the description
            if description != "No description":
                description = html.unescape(description)
                # Remove HTML tags (simple approach)
                description = description.replace('<p>', '').replace('</p>', '\n')
                description = description.replace('<br>', '\n').replace('<br/>', '\n')
            
            parsed_items.append({
                'title': title,
                'link': link,
                'description': description,
                'pubDate': pubDate
            })
        
        return {
            'feed_title': feed_title,
            'feed_description': feed_description,
            'items': parsed_items
        }
        
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def display_feed(feed_data):
    """Display the parsed feed data in a readable format"""
    if feed_data is None:
        print("No feed data to display.")
        return
    
    print(f"\n==== {feed_data['feed_title']} ====")
    print(f"Description: {feed_data['feed_description']}")
    print(f"Number of items: {len(feed_data['items'])}")
    print("\n--- Items ---")
    
    for i, item in enumerate(feed_data['items'], 1):
        print(f"\n[{i}] {item['title']}")
        print(f"Published: {item['pubDate']}")
        print(f"Link: {item['link']}")
        print("Description Preview: " + (item['description'][:200] + "..." if len(item['description']) > 200 else item['description']))

def main():
    url = "https://rss.app/feeds/pUJ3YqGjHTMSP6jb.xml"
    print(f"Fetching RSS feed from: {url}")
    
    xml_content = fetch_rss(url)
    if xml_content:
        feed_data = parse_rss(xml_content)
        if feed_data:
            display_feed(feed_data)
        else:
            print("Failed to parse the RSS feed.")
    else:
        print("Failed to fetch the RSS feed.")

if __name__ == "__main__":
    main() 