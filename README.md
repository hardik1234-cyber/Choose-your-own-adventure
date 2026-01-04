# Choose Your Own Adventure Game

An interactive Gen-AI-powered story generator that creates personalized choose-your-own-adventure experiences. Users can input a theme, and the system generates a complete branching narrative with multiple paths and endings using Google's Gemini AI.

## 🚀 Features

- **AI-Powered Story Generation**: Leverages Google Gemini 2.5 Flash model to create engaging, dynamic stories
- **Interactive Storytelling**: Branching narratives with multiple choice options and endings
- **Asynchronous Processing**: Background job system for story generation to handle AI API calls efficiently
- **Session Management**: Cookie-based sessions for seamless user experience
- **Responsive Web Interface**: Modern React frontend with clean, intuitive design
- **RESTful API**: Well-documented FastAPI backend with automatic OpenAPI documentation
- **Database Persistence**: SQLite database with SQLAlchemy ORM for story storage

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI for high-performance async API
- **AI Integration**: LangChain with Google Gemini AI for story generation
- **Database**: SQLAlchemy ORM with SQLite
- **Job Processing**: Background tasks for asynchronous story creation
- **CORS Support**: Configurable cross-origin resource sharing

### Frontend (React/Vite)
- **Framework**: React 19 with modern hooks
- **Routing**: React Router for navigation
- **HTTP Client**: Axios for API communication
- **Build Tool**: Vite for fast development and optimized production builds

### Data Flow
1. User inputs a story theme on the frontend
2. Frontend sends request to create a background job
3. Backend processes job asynchronously, calling Gemini AI to generate story
4. AI creates a tree-structured story with nodes, options, and endings
5. Story is saved to database with proper relationships
6. Frontend polls job status and redirects to interactive story player
7. User makes choices that navigate through the story tree

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Database ORM
- **LangChain** - AI framework integration
- **Google Generative AI** - Gemini model access
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **ESLint** - Code linting

### Database
- **SQLite** - Lightweight relational database
- **SQLAlchemy** - ORM and migrations

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Google Gemini API key


## 🎮 Usage

1. **Access the application** at `http://localhost:5173`
2. **Enter a story theme** (e.g., "space adventure", "medieval fantasy", "detective mystery")
3. **Wait for AI generation** - the system will show loading status
4. **Play the story** - make choices by clicking on options
5. **Experience multiple endings** - different paths lead to different outcomes
6. **Restart or create new stories** anytime

## 📚 API Documentation

When the backend is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Key Endpoints

- `POST stories/create` - Create a new story generation job
- `GET  jobs/{job_id}` - Check job status
- `GET stories/{story_id}/complete` - Get complete story data

## 🗄️ Database Schema

### Stories Table
- `id`: Primary key
- `title`: Story title
- `session_id`: User session identifier
- `created_at`: Timestamp

### Story Nodes Table
- `id`: Primary key
- `story_id`: Foreign key to stories
- `content`: Node content text
- `is_root`: Boolean for root node
- `is_ending`: Boolean for ending nodes
- `is_winning_ending`: Boolean for winning endings
- `options`: JSON array of choice options

### Jobs Table
- `job_id`: UUID primary key
- `session_id`: User session
- `theme`: Story theme
- `status`: Job status (pending/processing/completed/failed)
- `story_id`: Generated story ID
- `error`: Error message if failed

## 🤖 AI Story Generation

The system uses a sophisticated prompt engineering approach:

1. **Structured Output**: Pydantic models ensure consistent JSON responses from AI
2. **Tree Structure**: Stories are generated as hierarchical node trees
3. **Multiple Endings**: Guaranteed winning and losing paths
4. **Dynamic Depth**: Stories vary in length and complexity
5. **Theme Integration**: User themes are incorporated into narrative generation


## 🚀 Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=sqlite:///./database.db
   DEBUG=True
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the backend:**
   ```bash
   python main.py
   ```
   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`


## 🔧 Development

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend can be deployed with uvicorn or gunicorn
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering the story generation
- FastAPI community for the excellent framework
- React ecosystem for the frontend tools
- LangChain for AI integration utilities

---

