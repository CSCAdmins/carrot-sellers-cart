# Carrot Sellers - UFO/UAP Claims Tracker

A MkDocs-based website for tracking and fact-checking claims made by prominent UFO/UAP talking heads.

## Features

- **Carrot Meter**: 5-carrot credibility rating system
- **Person Profiles**: Track individual speakers with photos, bio info, and credibility ratings
- **Quote Tracking**: Document claims with dates, sources, context, and fact-check status
- **Responsive Design**: Clean, modern interface using Material for MkDocs

## Quick Start

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/CSCAdmins/carrot-sellers-cart.git
cd carrot-sellers-cart
```

2. Create a virtual environment and install dependencies with uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. For development dependencies:
```bash
uv pip install -e ".[dev]"
```

### Running Locally

Start the development server:
```bash
mkdocs serve
```

Visit `http://127.0.0.1:8000` to see the site.

### Building for Production

Build the static site:
```bash
mkdocs build
```

The built site will be in the `site/` directory.

## Project Structure

```
carrot-sellers-site/
├── docs/                    # MkDocs content
│   ├── index.md            # Homepage
│   ├── about.md            # About page
│   ├── people/             # Individual profiles
│   │   ├── index.md        # People directory
│   │   └── example-person.md
│   ├── assets/             # Images and media
│   │   └── images/people/  # Profile photos
│   └── stylesheets/        # Custom CSS
│       └── extra.css       # Carrot meter styles
├── overrides/              # MkDocs theme overrides
├── mkdocs.yml              # MkDocs configuration
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Adding New People

1. Create a new markdown file in `docs/people/` (e.g., `john-doe.md`)
2. Copy the structure from `example-person.md`
3. Add their photo to `docs/assets/images/people/`
4. Update the people index in `docs/people/index.md`

## Carrot Meter Ratings

The more carrots, the more "carrot selling" (BS/unsubstantiated claims):

- ⚪⚪⚪⚪⚪ - Highly credible, evidence-based claims only
- 🥕⚪⚪⚪⚪ - Generally reliable with occasional speculation
- 🥕🥕⚪⚪⚪ - Mixed track record, some questionable claims
- 🥕🥕🥕⚪⚪ - Frequently makes unsubstantiated claims
- 🥕🥕🥕🥕⚪ - Primarily speculation and sensationalism
- 🥕🥕🥕🥕🥕 - Maximum carrot seller, consistent misinformation

## Container Deployment

### Using Apple Container System (Recommended on macOS):

1. **Install Apple Container** (if not already installed):
```bash
# Follow installation instructions at:
# https://github.com/apple/container
```

2. **Build and run with the provided script**:
```bash
./container-build.sh
```

3. **Or manually**:
```bash
# Start container system
container system start

# Build the image
container build --tag carrot-sellers --file Dockerfile .

# Run the container
container run --name carrot-sellers-web --detach --rm carrot-sellers

# Get the container IP address
container inspect carrot-sellers-web | jq -r '.[0].networks[0].address'
```

### Using Docker (Alternative):
```bash
# Build and run the container
docker compose up carrot-sellers

# Or manually:
docker build -t carrot-sellers .
docker run -p 8080:8080 carrot-sellers
```

### For development with live reload:
```bash
# Using Apple container (with volume mount)
container run --rm -it \
  --volume $(pwd):/app \
  --workdir /app \
  cgr.dev/chainguard/python:latest-dev \
  sh -c "python -m venv venv && . venv/bin/activate && pip install -e . && mkdocs serve --dev-addr 0.0.0.0:8000"

# Or using Docker Compose
docker compose up carrot-sellers-dev
```

## Development

### Code Formatting

Format code with Black:
```bash
black .
```

Lint with Ruff:
```bash
ruff check .
```

## License

[Your chosen license]

## Contributing

We welcome contributions to improve the accuracy and completeness of our tracking. Please read our guidelines carefully:

### Branch Naming Convention

| Type | Format | Example |
|------|--------|---------|
| New person | `add/<person-name>` | `add/george-knapp` |
| Profile update | `update/<person-name>` | `update/david-grusch` |
| Quote addition | `quote/<person-name>-<date>` | `quote/grusch-2024-03` |
| Bug fix | `fix/<description>` | `fix/broken-links` |
| Feature | `feature/<description>` | `feature/search-filter` |

### Pull Request Format

**Title**: `[TYPE] Brief description`

Types: `[ADD]`, `[UPDATE]`, `[QUOTE]`, `[FIX]`, `[FEATURE]`

**Body template**:
```markdown
## Summary
Brief description of changes (1-3 sentences)

## Changes
- Change 1
- Change 2

## Sources (for content PRs)
- [Source title](URL)

## Checklist
- [ ] Followed branch naming convention
- [ ] All quotes are verbatim with sources
- [ ] Tested locally with `mkdocs serve`
```

### Quick Contributions (Issues/PRs welcome)
- Quote submissions with sources
- Corrections to existing information
- Fact-checking updates
- Source verification improvements

### Major Contributions (Discussion required)
- **New people**: Must open an Issue first for community discussion (minimum 7 days)
- Score methodology changes
- Structural changes to the site

### Quality Standards
- All quotes must be verbatim with exact sources
- Sources must be publicly verifiable
- New people must meet influence/impact criteria
- Scoring must follow our 5-criteria methodology

**Full guidelines**: [CONTRIBUTING.md](CONTRIBUTING.md)
