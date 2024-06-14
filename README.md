# NewsAggregator

This project is a Python-based news aggregator that fetches and parses news articles from multiple Indian news websites. The aggregator uses requests for HTTP requests, BeautifulSoup for HTML parsing, and ThreadPoolExecutor for concurrent fetching and processing of news articles.

# Features

- Fetches and parses news articles from multiple Indian news websites.
- Concurrently processes multiple news URLs to improve efficiency.
- Extracts and sanitizes the title and content of news articles.

# Supported News Channels
The aggregator currently supports the following news channels:

- Times Now
- ABP News
- India Today
- Aaj Tak
- News18

# Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/news-aggregator.git
```
2. Navigate to the project directory:
```
cd news-aggregator
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

# Usage
To run the news aggregator, execute the following command:
```
python news_aggregator.py
```

# Code Explanation
## NewsAggregator Class
The NewsAggregator class contains methods to fetch and parse news articles from different news websites.

## Initialization
- self.news_hrefs: A list to store news article URLs.
- self.news_channels: A dictionary containing the base URLs and relevant HTML classes/IDs for different news websites.

## Methods
- get_soup(url): Fetches the HTML content of the provided URL and returns a BeautifulSoup object.
- timesnow_news(news_soup): Parses news articles from Times Now.
- abpnews_news(news_soup): Parses news articles from ABP News.
- indiatoday_news(news_soup): Parses news articles from India Today.
- aajtak_news(news_soup): Parses news articles from Aaj Tak.
- news18_news(news_soup): Parses news articles from News18.
- parse_news(href): Identifies the source of the news article and parses it accordingly.
- main(): Main method to fetch, parse, and aggregate news articles from all supported news channels.

## main()
The main() function initializes the NewsAggregator class, fetches the news articles, and prints the results.

# Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.
