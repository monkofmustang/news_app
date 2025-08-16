# International News Processing System

This system fetches news from multiple international sources, saves them to PostgreSQL database, and generates AI-powered summaries using LLM.

## 🌍 Features

- **Multi-Source News Fetching**: Collects news from UN News, Times of India, The Hindu International, and NYT World
- **Database Storage**: Saves all news with metadata to PostgreSQL
- **AI Summarization**: Uses LLM to generate compelling 60-word summaries
- **Duplicate Prevention**: Avoids saving duplicate news articles
- **Background Processing**: Supports both synchronous and asynchronous processing
- **RESTful API**: Complete CRUD operations for news management

## 📋 Prerequisites

1. **PostgreSQL Database**: Set up and running
2. **Environment Variables**: Configured with database URL and API keys
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
HF_TOKEN=your_huggingface_token
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
python test_international_news.py
```

### 5. Start the Application

```bash
uvicorn news_app:app --reload
```

## 📡 API Endpoints

### International News Processing

- **POST** `/international-news/process` - Process news in background
- **POST** `/international-news/process-sync` - Process news synchronously

### News Retrieval

- **GET** `/international-news/` - Get all international news
- **GET** `/international-news/summarized` - Get only summarized news
- **GET** `/international-news/{news_id}` - Get specific news item
- **GET** `/international-news/stats/summary` - Get processing statistics

### News Management

- **POST** `/international-news/summarize/{news_id}` - Manually summarize a news item
- **DELETE** `/international-news/{news_id}` - Delete a news item

## 🔧 Usage Examples

### Process International News

```bash
# Background processing
curl -X POST "http://localhost:8000/international-news/process"

# Synchronous processing (waits for completion)
curl -X POST "http://localhost:8000/international-news/process-sync"
```

### Get News

```bash
# Get all international news
curl "http://localhost:8000/international-news/"

# Get only summarized news
curl "http://localhost:8000/international-news/summarized"

# Get with pagination
curl "http://localhost:8000/international-news/?limit=10&offset=0"
```

### Get Statistics

```bash
curl "http://localhost:8000/international-news/stats/summary"
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
| `tag` | String(100) | News tag (e.g., "international_news") |
| `summary` | Text | AI-generated summary |
| `is_summarized` | Boolean | Summary status |
| `created_at` | DateTime | Record creation time |
| `updated_at` | DateTime | Last update time |

## 🤖 AI Summarization

The system uses the `summarize_news` function from `llm_service.py` to generate compelling 60-word summaries that:

- **Hook the reader** with compelling openings
- **Reveal core story** with key details
- **Create urgency** with emotional triggers
- **End with cliffhangers** to encourage reading full story
- **Maintain journalistic integrity**

### Example Summary

```
BREAKING: UN Security Council passes unprecedented resolution calling for immediate ceasefire in Gaza conflict. The 15-member council voted 14-1, with only the US abstaining, marking a historic shift in international diplomacy. The resolution demands humanitarian aid access and prisoner exchanges within 48 hours. But here's what happens next that will shock everyone...
```

## 🔄 Processing Flow

1. **Fetch News**: Calls all news source methods (`un_news`, `toi_news`, etc.)
2. **Deduplication**: Checks for existing news based on title and link
3. **Database Storage**: Saves new articles with metadata
4. **AI Summarization**: Generates summaries for each article
5. **Status Update**: Marks articles as summarized

## 🛠️ Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `HF_TOKEN`: Hugging Face API token for LLM access
- `UN_NEWS`: UN News RSS feed URL
- `TOI_NEWS`: Times of India RSS feed URL
- `THE_HINDU_INTERNATIONAL`: The Hindu International RSS feed URL
- `NYT_WORLD`: NYT World RSS feed URL

### RSS Feed Sources

The system fetches from these sources:

1. **UN News**: United Nations official news
2. **Times of India**: Indian news and international coverage
3. **The Hindu International**: International news from The Hindu
4. **NYT World**: World news from The New York Times

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Verify database permissions

2. **LLM API Error**
   - Check `HF_TOKEN` configuration
   - Verify internet connection
   - Check API rate limits

3. **RSS Feed Errors**
   - Verify RSS URLs in environment
   - Check network connectivity
   - Some feeds may be temporarily unavailable

### Debug Mode

Enable detailed logging by setting environment variable:

```bash
export DEBUG=true
```

## 📈 Performance

- **Processing Time**: ~2-5 minutes for 50-100 articles
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

1. Add RSS feed URL to environment variables
2. Create fetch function in `international_news.py`
3. Add function call to `fetch_all_international_news()`
4. Update documentation

### Customizing Summarization

Modify the system prompt in `llm_service.py`:

```python
system_prompt = """Your custom summarization instructions here..."""
```

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check application logs
4. Verify environment configuration

## 🎯 Future Enhancements

- [ ] Add more news sources
- [ ] Implement news categorization
- [ ] Add sentiment analysis
- [ ] Create news alerts system
- [ ] Add multilingual support
- [ ] Implement news trending analysis
