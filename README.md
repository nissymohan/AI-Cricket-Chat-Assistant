# 🏏 Cricket AI Fantasy Assistant

An intelligent IPL Fantasy Cricket assistant powered by AI that provides real-time match insights, player recommendations, and strategic advice for fantasy cricket enthusiasts.

![Cricket AI Banner](https://img.shields.io/badge/Cricket-AI%20Assistant-4e4eff?style=for-the-badge&logo=cricket&logoColor=white)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=flat-square&logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

## ✨ Features

### 🤖 AI-Powered Chat Assistant
- **Smart Cricket Analysis**: Get intelligent insights about IPL matches, players, and strategies
- **Multi-AI Support**: Compatible with OpenAI GPT and Anthropic Claude APIs
- **Natural Language Processing**: Ask questions in plain English about cricket strategies

### 📊 Real-Time Data & Analytics
- **Live Match Updates**: Real-time IPL match scores and status
- **Player Performance Analysis**: Form analysis, recent scores, and statistical insights
- **Weather & Pitch Reports**: Condition-based recommendations for team selection

### ⚡ Quick Action Features
- **Best Team Suggestions**: Get optimized team combinations for current matches
- **Captain Recommendations**: Data-driven captain and vice-captain picks
- **Differential Picks**: Low-ownership players with high potential
- **Budget-Friendly Options**: Value picks to maximize your fantasy budget

### 🎯 Interactive Dashboard
- **Live Statistics**: Active users, teams created, success rates
- **Match Insights**: Weather conditions, pitch analysis, team strategies
- **Beautiful UI**: Glassmorphism design with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js (for development)
- API keys for OpenAI and/or Anthropic (optional but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cricket-ai-assistant.git
   cd cricket-ai-assistant
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (Optional)
   ```bash
   # Windows
   set OPENAI_API_KEY=your-openai-api-key
   set ANTHROPIC_API_KEY=your-anthropic-api-key
   
   # Linux/macOS
   export OPENAI_API_KEY=your-openai-api-key
   export ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

4. **Run the application**
   ```bash
   python server.py
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🏗️ Project Structure

```
cricket-ai-assistant/
├── 📄 index.html          # Main frontend interface
├── 🎨 style.css           # Glassmorphism styling
├── ⚡ cricket-ai.js       # Frontend JavaScript logic
├── 🐍 server.py           # Flask backend server
├── 📋 requirements.txt    # Python dependencies
└── 📖 README.md          # Project documentation
```

## 🎮 Usage Guide

### Basic Chat Interaction
```
🏏 Ask me anything about IPL cricket:
• "Who should I pick as captain today?"
• "Compare Virat Kohli vs Rohit Sharma"
• "What's the best team for MI vs CSK?"
• "Give me differential picks for tonight's match"
```

### Quick Actions
- **👥 Best Team Today**: Get optimized 11-player team
- **🎯 Differentials**: Low-ownership, high-potential picks
- **👑 Captain Picks**: Top captaincy options with analysis
- **💰 Budget Picks**: Value-for-money player recommendations
- **💡 Fantasy Tips**: Strategic advice for team building

### Advanced Features
```javascript
// Test the AI with preset questions
window.CricketAIHelpers.testIPLQuestions()

// Ask specific questions programmatically
window.CricketAIHelpers.askBestCaptain()
window.CricketAIHelpers.askMIvsCSK()
```

## 🛠️ Configuration

### AI Model Setup
The application supports multiple AI providers:

**OpenAI Configuration:**
```python
# Requires OPENAI_API_KEY environment variable
# Uses GPT-3.5-turbo model for cricket analysis
```

**Anthropic Configuration:**
```python
# Requires ANTHROPIC_API_KEY environment variable  
# Uses Claude-3-sonnet for detailed cricket insights
```

**Fallback Mode:**
If no API keys are provided, the system uses intelligent rule-based responses.

### Customization
- **Player Database**: Modify `player_db` in `server.py` to update player stats
- **UI Themes**: Customize colors and styles in `style.css`
- **API Endpoints**: Add new endpoints in `server.py` for additional features

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/chat` | POST | Main chat interface for AI responses |
| `/api/quick-actions/<action>` | GET | Quick action buttons (best-team, differentials, etc.) |
| `/api/live-stats` | GET | Real-time user and contest statistics |
| `/api/match-analysis` | GET | Weather, pitch, and match condition data |
| `/api/matches` | GET | Live IPL match information |
| `/api/health` | GET | System health check and AI status |

## 🧪 Testing

### Manual Testing
```bash
# Test the backend
curl http://localhost:5000/api/health

# Test chat functionality
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Who should I pick as captain?"}'
```

### Frontend Testing
```javascript
// Open browser console and run:
window.CricketAIHelpers.askLiveMatches()
window.CricketAIHelpers.askBestCaptain()
```

## 🔧 Troubleshooting

### Common Issues

**Backend Not Starting:**
```bash
# Check if port 5000 is available
netstat -an | findstr :5000  # Windows
lsof -i :5000                # Linux/macOS
```

**CORS Errors:**
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check that the frontend is accessing the correct backend URL

**AI Responses Not Working:**
- Verify API keys are set correctly
- Check console for error messages
- System will fall back to rule-based responses if AI APIs fail

**Frontend Not Loading:**
- Ensure all files are in the same directory
- Check browser console for JavaScript errors
- Verify `cricket-ai.js` is loaded properly

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Add new features or fix bugs
4. **Test thoroughly**: Ensure all functionality works
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**: Describe your changes and their benefits

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Use meaningful variable names and comments
- Test both AI and fallback modes
- Ensure responsive design for mobile devices

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IPL Teams**: Mumbai Indians, Chennai Super Kings, Royal Challengers Bangalore, and all IPL franchises
- **AI Providers**: OpenAI and Anthropic for powerful language models
- **Cricket APIs**: Various cricket data providers for live match information
- **Design Inspiration**: Modern glassmorphism and cricket-themed UI elements

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cricket-ai-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cricket-ai-assistant/discussions)
- **Email**: your.email@example.com

## 🚀 Future Roadmap

- [ ] **Mobile App**: React Native version for iOS and Android
- [ ] **Historical Analysis**: Season-long performance tracking
- [ ] **Social Features**: Share teams and compete with friends
- [ ] **Advanced Analytics**: Machine learning models for predictions
- [ ] **Multi-League Support**: Support for other cricket leagues beyond IPL
- [ ] **Voice Interface**: Voice commands for hands-free interaction

---

<div align="center">

**Made with ❤️ for Cricket Fans**

*Transform your fantasy cricket experience with AI-powered insights*

[⭐ Star this repo](https://github.com/yourusername/cricket-ai-assistant) • [🐛 Report Bug](https://github.com/yourusername/cricket-ai-assistant/issues) • [💡 Request Feature](https://github.com/yourusername/cricket-ai-assistant/issues)

</div>
