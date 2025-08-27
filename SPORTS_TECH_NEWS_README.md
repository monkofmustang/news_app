# Sports & Tech News Processing System

This system fetches news from multiple sports and technology sources and saves them to PostgreSQL database without summarization.

## 🏈⚽ Features

### Sports News
- **Multi-Source Fetching**: Collects news from The Hindu Sports and The Himalayan Times Sports
- **Database Storage**: Saves all sports news with metadata to PostgreSQL
- **Tag-based Organization**: Uses `sports_news` tag for categorization
- **Duplicate Prevention**: Avoids saving duplicate news articles

### Tech News
- **Multi-Source Fetching**: Collects news from Times of India Tech and TechCrunch
- **Database Storage**: Saves all tech news with metadata to PostgreSQL
- **Tag-based Organization**: Uses `tech_news` tag for categorization
- **Duplicate Prevention**: Avoids saving duplicate news articles

## 📋 Prerequisites

1. **PostgreSQL Database**: Set up and running
2. **Environment Variables**: Configured with database URL
3. **Python Dependencies**: All required packages installed

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Copy and configure your environment variables:

```bash
cp env_template.txt .env
```

Edit `.env` with your database configuration:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/news_app
THE_HINDU_SPORTS=https://www.thehindu.com/sport/?service=rss
THE_HIMALAYAN_TIMES_SPORTS=https://thehimalayantimes.com/category/sports/feed/
TOI_TECH=https://timesofindia.indiatimes.com/rssfeedstopstories.cms
TECH_CRUNCH=https://techcrunch.com/feed/
```

### 3. Initialize Database

```bash
# Create tables
python init_db.py

# Or use Alembic for migrations
alembic revision --autogenerate -m "Add news table"
alembic upgrade head
```

### 4. Test the System

```bash
python test_sports_tech_news.py
```

### 5. Start the Application

```bash
uvicorn news_app:app --reload
```

## 📡 API Endpoints

### Sports News

- **POST** `/sports-news/process` - Process sports news in background
- **POST** `/sports-news/process-sync` - Process sports news synchronously
- **GET** `/sports-news/` - Get all sports news
- **GET** `/sports-news/{news_id}` - Get specific sports news item
- **DELETE** `/sports-news/{news_id}` - Delete a sports news item
- **GET** `/sports-news/stats/summary` - Get sports news statistics

### Tech News

- **POST** `/tech-news/process` - Process tech news in background
- **POST** `/tech-news/process-sync` - Process tech news synchronously
- **GET** `/tech-news/` - Get all tech news
- **GET** `/tech-news/{news_id}` - Get specific tech news item
- **DELETE** `/tech-news/{news_id}` - Delete a tech news item
- **GET** `/tech-news/stats/summary` - Get tech news statistics

## 🔧 Usage Examples

### Process Sports News

```bash
# Background processing
curl -X POST "http://localhost:8000/sports-news/process"

# Synchronous processing (waits for completion)
curl -X POST "http://localhost:8000/sports-news/process-sync"
```

### Process Tech News

```bash
# Background processing
curl -X POST "http://localhost:8000/tech-news/process"

# Synchronous processing (waits for completion)
curl -X POST "http://localhost:8000/tech-news/process-sync"
```

### Get News

```bash
# Get all sports news
curl "http://localhost:8000/sports-news/"

# Get all tech news
curl "http://localhost:8000/tech-news/"

# Get with pagination
curl "http://localhost:8000/sports-news/?limit=10&offset=0"
curl "http://localhost:8000/tech-news/?limit=10&offset=0"
```

### Get Statistics

```bash
curl "http://localhost:8000/sports-news/stats/summary"
curl "http://localhost:8000/tech-news/stats/summary"
```

## 📊 Database Schema

### News Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `title` | String(500) | News title |
| `description` | Text | News description |
| `content` | Text | Full news content |
| `link` | String(1000) | Original news URL |
| `pub_date` | DateTime | Publication date |
| `category` | String(100) | News category |
| `image` | String(1000) | Image URL |
| `publisher` | String(200) | News source |
| `tag` | String(100) | News tag (`sports_news` or `tech_news`) |
| `summary` | Text | AI-generated summary (null for sports/tech) |
| `is_summarized` | Boolean | Summary status (false for sports/tech) |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

## 🔄 Processing Flow

### Sports News Processing
1. **Fetch** → Calls `the_hindu_sports()` and `the_himalayan_times_sports()`
2. **Deduplicate** → Checks for existing articles
3. **Save** → Stores new articles in PostgreSQL with tag `sports_news`

### Tech News Processing
1. **Fetch** → Calls `toi_tech()` and `tech_crunch()`
2. **Deduplicate** → Checks for existing articles
3. **Save** → Stores new articles in PostgreSQL with tag `tech_news`

## 🛠️ Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `THE_HINDU_SPORTS`: The Hindu Sports RSS feed URL
- `THE_HIMALAYAN_TIMES_SPORTS`: The Himalayan Times Sports RSS feed URL
- `TOI_TECH`: Times of India Tech RSS feed URL
- `TECH_CRUNCH`: TechCrunch RSS feed URL

### RSS Feed Sources

#### Sports News Sources
1. **The Hindu Sports**: Sports news from The Hindu
2. **The Himalayan Times Sports**: Sports news from Nepal

#### Tech News Sources
1. **Times of India Tech**: Technology news from TOI
2. **TechCrunch**: Technology startup and industry news

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Verify database permissions

2. **RSS Feed Errors**
   - Verify RSS URLs in environment
   - Check network connectivity
   - Some feeds may be temporarily unavailable

3. **No News Fetched**
   - Check RSS feed URLs are correct
   - Verify internet connection
   - Check if feeds are accessible

### Debug Mode

Enable detailed logging by setting environment variable:

```bash
export DEBUG=true
```

## 📈 Performance

- **Processing Time**: ~1-3 minutes for 20-50 articles per category
- **Database Storage**: ~1KB per article
- **API Response Time**: <500ms for queries
- **Concurrent Processing**: Supports background tasks

## 🔒 Security

- **Input Validation**: All inputs are validated
- **SQL Injection Protection**: Uses SQLAlchemy ORM
- **Error Handling**: Comprehensive error management
- **Rate Limiting**: Built-in API rate limiting

## 📝 Development

### Adding New News Sources

#### For Sports News
1. Add RSS feed URL to environment variables
2. Create fetch function in `international_sports_news.py`
3. Add function call to `fetch_all_sports_news()` in `sports_news_service.py`
4. Update documentation

#### For Tech News
1. Add RSS feed URL to environment variables
2. Create fetch function in `international_tech_news.py`
3. Add function call to `fetch_all_tech_news()` in `tech_news_service.py`
4. Update documentation

### Service Structure

```
service/
├── sports_news_service.py      # Sports news processing
├── tech_news_service.py        # Tech news processing
└── international_news_service.py # International news (with summarization)

controller/
├── sports_news_controller.py   # Sports news API endpoints
├── tech_news_controller.py     # Tech news API endpoints
└── international_news_controller.py # International news API endpoints
```

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check application logs
4. Verify environment configuration

## 🎯 Key Differences from International News

| Feature | International News | Sports News | Tech News |
|---------|-------------------|-------------|-----------|
| Summarization | ✅ AI-powered summaries | ❌ No summarization | ❌ No summarization |
| Tag | `international_news` | `sports_news` | `tech_news` |
| Processing | Fetch → Save → Summarize | Fetch → Save | Fetch → Save |
| Sources | 4 sources | 2 sources | 2 sources |

## 🎉 Future Enhancements

- [ ] Add more sports news sources
- [ ] Add more tech news sources
- [ ] Implement news categorization
- [ ] Add sentiment analysis
- [ ] Create news alerts system
- [ ] Add multilingual support
- [ ] Implement news trending analysis
- [ ] Add optional summarization for sports/tech news
