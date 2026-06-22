<div align="center">
  <a href="https://proxidize.com/mobile-proxy-pricing/" target="_blank" rel="noopener noreferrer">
    <img src="https://imagedelivery.net/r4caA8hJ3Ww3j8uyC_NNCA/95a9137a-43fd-48d4-7243-983f3f4a3d00/public" alt="Proxidize Logo" width="100%"/>
  </a>
</div>

# X-Scraper

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)
![License](https://img.shields.io/badge/license-Educational-lightgrey.svg)

Twitter/X scraper built with Playwright for browser automation and OpenAI for AI-powered tweet analysis.

## Features

### Core Scraping Capabilities
- **Timeline Scraping**: Extract tweets from any user's timeline with full metadata
- **Historical Search**: Scrape tweets from specific date ranges
- **Keyword Search**: Search for tweets by keywords, hashtags, or phrases
- **Mixed Strategy**: Combine timeline + historical search for comprehensive coverage

### Advanced Features
- **AI Analysis**: Automatic sentiment analysis, topic extraction, and summaries using ChatGPT
- **Checkpoint/Resume**: Resume interrupted scrapes from where they stopped
- **Progress Tracking**: Real-time progress bars and detailed logging
- **Proxy Support**: Built-in support for residential/mobile proxies
- **Session Persistence**: Cookie-based authentication for reliable long-term scraping
- **Rate Limit Handling**: Intelligent retry mechanisms with exponential backoff
- **Deduplication**: Automatic removal of duplicate tweets

### Data Quality
- **Rich Metadata**: Captures tweets, user info, engagement metrics, media, hashtags, URLs
- **Structured Output**: Clean JSON format with proper typing and validation

## Prerequisites

- Python 3.11+
- Chrome/Chromium browser (installed automatically by Playwright)
- Twitter/X account credentials
- Proxy service for IP rotation
- (Optional) OpenAI API key for AI analysis

## Installation

### Standard Installation

```bash
git clone https://github.com/proxidize/x-scraper

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install uv
uv sync

# Install Playwright browsers
playwright install chromium

# Copy config template
cp config.ini.template config.ini
```

### Docker Installation

```bash
docker build -t x-scraper .
```

## Configuration

Edit `config.ini` with your settings:

```ini
[TWITTER]
username = your_username
email = your_email@example.com
password = your_password

[PROXY]
use_proxy = true
proxy_url = http://your-proxy:port

[AI]
enable_analysis = true
openai_api_key = sk-your-api-key-here
model = gpt-4o-mini
batch_size = 10

[SCRAPING]
output_directory = ./data
max_tweets_per_session = 1000
scroll_delay_min = 2.0
scroll_delay_max = 5.0
```

### Required Fields
- `[TWITTER]`: username, email, password
- `[SCRAPING]`: output_directory, max_tweets_per_session

### Optional Fields
- `[AI]`: All fields (for AI analysis)

## Usage

> **Note:** Throughout these examples, we use `FabrizioRomano` (a popular football transfer news reporter) as our test account. This account was used during development and testing due to its high tweet volume and consistent posting patterns.

### Interactive Mode

```bash
python main.py interactive
```

Launches an interactive menu with guided options for all scraping modes.

### Command Line Interface

#### 1. Scrape User Timeline

```bash
python main.py user <username> [OPTIONS]

# Example: Scrape 500 tweets from FabrizioRomano
python main.py user FabrizioRomano --max-tweets 500

# With AI analysis
python main.py user FabrizioRomano --max-tweets 500 --analysis sentiment,topics,summary
```

**Options:**
- `--max-tweets`: Maximum number of tweets to scrape (default: from config)
- `--analysis`: AI analysis types (sentiment, topics, summary, all)

**Performance Note:**
- A typical timeline scraping session takes approximately **30-40 minutes**
- Produces roughly **800-1000 tweets**
- For comprehensive coverage beyond this limit, use **historical search by date** (see below)

#### 2. Keyword Search

```bash
python main.py search <query> [OPTIONS]

# Example: Search for "Here we go" tweets
python main.py search "Here we go" --max-tweets 200

# Search with filters
python main.py search "#TransferNews" --max-tweets 500 --analysis all
```

**Options:**
- `--max-tweets`: Maximum number of tweets to scrape
- `--analysis`: AI analysis types

#### 3. Historical Search (Date Range)

```bash
python main.py search-historical <username> --since YYYY-MM-DD --until YYYY-MM-DD [OPTIONS]

# Example: Scrape FabrizioRomano's tweets from December 2021
python main.py search-historical FabrizioRomano \
  --since 2021-12-01 \
  --until 2021-12-31 \
  --max-tweets 500

# With AI analysis
python main.py search-historical FabrizioRomano \
  --since 2023-07-01 \
  --until 2023-07-31 \
  --analysis sentiment,topics
```

**Options:**
- `--since`: Start date (YYYY-MM-DD)
- `--until`: End date (YYYY-MM-DD)
- `--max-tweets`: Maximum tweets per date chunk
- `--analysis`: AI analysis types

**Note:** Historical search automatically chunks large date ranges into weekly intervals for better coverage.

### Recommended Strategy: Mixed Approach

For comprehensive tweet coverage, combine both methods:

1. **Start with Timeline Scraping**: Get recent tweets (last 800-1000 tweets)
   ```bash
   python main.py user FabrizioRomano --max-tweets 1000
   ```

2. **Use Historical Search for Older Tweets**: Go beyond timeline limitations
   ```bash
   python main.py search-historical FabrizioRomano \
     --since 2023-01-01 \
     --until 2023-12-31 \
     --max-tweets 500
   ```

## Output Structure

### Tweet Data

```json
{
  "username": "FabrizioRomano",
  "tweet_count": 303,
  "unique_tweet_count": 303,
  "tweets": [
    {
      "id": "1468352445113942019",
      "text": "Tweet content here...",
      "created_at": "Tue Dec 07 22:51:18 +0000 2021",
      "user": {
        "id": "330262748",
        "followers_count": 26490513,
        "verified": true
      },
      "metrics": {
        "retweet_count": 3,
        "favorite_count": 401,
        "reply_count": 7,
        "quote_count": 1
      },
      "hashtags": ["TransferNews"],
      "media": [],
      "is_retweet": false,
      "is_reply": true
    }
  ],
  "date_range": {
    "since": "2021-12-01",
    "until": "2021-12-31"
  }
}
```

### AI Analysis Output

```json
{
  "total_tweets": 303,
  "analysis": {
    "sentiment": {
      "positive": 156,
      "neutral": 120,
      "negative": 27
    },
    "topics": [
      {"topic": "Transfer News", "count": 89},
      {"topic": "Contract Extensions", "count": 45}
    ],
    "summary": "Analysis of 303 tweets shows..."
  }
}
```

## Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
3. **Add tests for new functionality**
4. **Commit your changes**
5. **Push to the branch**
6. **Submit a pull request**

## License

This project is for **educational and research purposes only**. 

### Important Legal Notes
- Respect Twitter/X's Terms of Service
- Do not use for commercial scraping without proper authorization
- Be mindful of rate limits and API usage

**Disclaimer:** The authors are not responsible for misuse of this tool. Use responsibly and ethically.

## Blog Post

For a detailed walkthrough of how this Twitter/X scraper was built, including challenges faced and solutions implemented, read our comprehensive blog post:

**[Twitter/X Scraper: How to Scrape Twitter for Free](https://proxidize.com/blog/twitter-scraper/)**

The blog post covers:
- Why Python and Playwright were chosen
- How Twitter/X's infinite scroll was handled
- Timeline vs. historical search strategies
- Proxy rotation and error handling
- AI integration with OpenAI

## Support

For issues, questions, or feature requests, please open an issue on GitHub or contact [support@proxidize.com](mailto:support@proxidize.com).

---

**Note**: This tool is designed for ethical data collection and research purposes. Always comply with Twitter/X's Terms of Service and respect rate limits.
