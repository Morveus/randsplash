# RandSplash - Random Themed Photo Server

A simple Python server that serves random photos from Unsplash based on themes, with built-in caching to optimize API usage.

## Important: Unsplash API Required

This server **exclusively** works with the Unsplash API. To use this application, you must:

1. Create a free account at [Unsplash Developers](https://unsplash.com/developers)
2. Create a new application in your developer dashboard
3. Obtain your Access Key and Secret Key from the application settings
4. Use these credentials in your `.env` file

Without valid Unsplash API credentials, this server will not function.

## Features

- 🖼️ Fetch random high-quality photos from Unsplash based on themes
- 💾 Built-in caching mechanism to reduce API calls
- 🔍 Support for multiple keyword searches
- 🚀 Simple REST API with Flask
- 🐳 Docker support for easy deployment

## API Endpoints

### `GET /`
Returns usage instructions.

### `GET /random/<theme>`
Returns a random photo matching the specified theme.

**Examples:**
- `/random/nature` - Random nature photo
- `/random/ocean%20sunset` - Random photo with ocean AND sunset
- `/random/city+night` - Random photo with city AND night
- `/random/mountain%20lake%20sunrise` - Random photo with all three keywords

### `GET /health`
Returns server health status and cache duration configuration.

## Quick Start with Docker Hub

The easiest way to run RandSplash is using the pre-built Docker image:

1. **Copy the example environment file:**
```bash
cp .env.example .env
```

2. **Edit `.env` with your Unsplash API credentials:**
```bash
nano .env  # or use your preferred editor
```

3. **Run the container with mounted `.env` file:**
```bash
docker run -d \
  --name randsplash \
  -p 5000:5000 \
  -v $(pwd)/.env:/app/.env:ro \
  morveus/randsplash:latest
```

The server will be available at `http://localhost:5000`

## Setup

### Prerequisites
- Python 3.8+ (for local development)
- Docker (for containerized deployment)
- Unsplash API credentials (Access Key and Secret Key)

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/randsplash.git
cd randsplash
```

2. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Unsplash API credentials
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python server.py
```

The server will start on `http://localhost:5000`

Note: `CACHE_DURATION_SECONDS` has a minimum value of 600 seconds (10 minutes) to respect API rate limits.

### Building from Source with Docker

1. Build the Docker image:
```bash
docker build -t randsplash .
```

2. Run the container:
```bash
docker run -p 5000:5000 -v $(pwd)/.env:/app/.env:ro randsplash
```

## Configuration

| Environment Variable | Description | Default | Minimum |
|---------------------|-------------|---------|---------|
| `UNSPLASH_ACCESS_KEY` | Your Unsplash API access key | Required | - |
| `UNSPLASH_SECRET_KEY` | Your Unsplash API secret key | Required | - |
| `CACHE_DURATION_SECONDS` | How long to cache photos (in seconds) | 600 | 600 |

## How It Works

1. When a request is made to `/random/<theme>`, the server checks its cache
2. If a cached photo exists for that theme and is less than `CACHE_DURATION_SECONDS` old, it's returned immediately
3. Otherwise, a new photo is fetched from Unsplash API
4. The new photo is cached and served to the client
5. Full resolution images are served for the best quality

## Example Usage

```bash
# Get a random nature photo
curl http://localhost:5000/random/nature > nature.jpg

# Get a random photo with multiple keywords
curl http://localhost:5000/random/tropical%20beach > beach.jpg

# Check server health
curl http://localhost:5000/health
```

## Rate Limiting

The caching mechanism helps prevent hitting Unsplash API rate limits by serving cached photos when available. The minimum cache duration of 600 seconds ensures responsible API usage.

## License

This project uses the Unsplash API and must comply with [Unsplash API Guidelines](https://unsplash.com/api-terms).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.