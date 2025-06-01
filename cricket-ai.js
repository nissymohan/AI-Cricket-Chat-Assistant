// 🏏 Clean Cricket AI - Auto Smart Mode
console.log('🏏 Loading Cricket AI...');

class CleanCricketAI {
    constructor() {
        this.API_URL = 'http://localhost:5000/api';
        this.isTyping = false;
        
        // Wait for page to load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }
    
    init() {
        console.log('✅ Cricket AI starting...');
        
        // Find your elements
        this.chatBox = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatForm = document.getElementById('chat-form');
        
        // Setup chat
        this.setupChat();
        
        // Setup quick action buttons
        this.setupQuickActions();
        
        // Load live data immediately
        this.loadLiveData();
        
        // Auto-refresh every 30 seconds
        setInterval(() => this.loadLiveData(), 30000);
        
        console.log('🚀 Cricket AI ready!');
    }
    
    setupChat() {
        // Remove old event listeners
        if (this.chatForm) {
            const newForm = this.chatForm.cloneNode(true);
            this.chatForm.parentNode.replaceChild(newForm, this.chatForm);
            this.chatForm = newForm;
            this.sendButton = this.chatForm.querySelector('#sendButton');
            this.messageInput = this.chatForm.querySelector('#messageInput');
        }
        
        // Add new event listener
        if (this.chatForm) {
            this.chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }
        
        // Add enhanced welcome message
        this.addMessage('Hello! I\'m your IPL Fantasy Cricket expert! 🏏 Ask me about live matches, player recommendations, or team strategies!', 'ai');
    }
    
    setupQuickActions() {
        const quickActionButtons = document.querySelectorAll('[data-action]');
        
        quickActionButtons.forEach(button => {
            button.addEventListener('click', () => {
                const action = button.getAttribute('data-action');
                this.handleQuickAction(action, button.textContent);
            });
        });
        
        console.log(`✅ Setup ${quickActionButtons.length} quick action buttons`);
    }
    
    async sendMessage() {
        const message = this.messageInput?.value?.trim();
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        
        // Show typing
        this.showTyping();
        
        try {
            const response = await fetch(`${this.API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (data.response) {
                this.addMessage(data.response, 'ai');
            } else {
                this.addMessage('Sorry, I had trouble understanding that. Can you try asking about IPL matches or players?', 'ai');
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessage('❌ Connection error! Make sure your backend is running on http://localhost:5000', 'ai');
        }
        
        this.hideTyping();
    }
    
    async handleQuickAction(action, buttonText) {
        console.log(`🎯 Quick action: ${action}`);
        
        // Visual feedback on button
        const button = document.querySelector(`[data-action="${action}"]`);
        if (button) {
            button.style.backgroundColor = 'rgba(78, 78, 255, 0.3)';
            setTimeout(() => {
                button.style.backgroundColor = '';
            }, 300);
        }
        
        // Show loading message
        this.addMessage(`⏳ Getting ${buttonText.toLowerCase()}...`, 'ai');
        
        try {
            const response = await fetch(`${this.API_URL}/quick-actions/${action}`);
            const data = await response.json();
            
            if (data.data) {
                const formattedResponse = this.formatQuickActionResponse(action, data.data);
                this.addMessage(formattedResponse, 'ai');
            } else {
                this.addMessage(`❌ Sorry, couldn't get ${buttonText.toLowerCase()} right now.`, 'ai');
            }
            
        } catch (error) {
            console.error(`Quick action error:`, error);
            this.addMessage('❌ Connection error! Make sure your backend is running.', 'ai');
        }
    }
    
    formatQuickActionResponse(action, data) {
        switch (action) {
            case 'best-team':
                return this.formatBestTeam(data);
            case 'differential-picks':
                return this.formatDifferentialPicks(data);
            case 'captain-options':
                return this.formatCaptainOptions(data);
            case 'budget-picks':
                return this.formatBudgetPicks(data);
            case 'fantasy-tips':
                return this.formatFantasyTips(data);
            default:
                return '✅ Here\'s your requested information!';
        }
    }
    
    formatBestTeam(players) {
        let response = '🏏 **Best IPL Team for Today:**\n\n';
        players.slice(0, 6).forEach((player, index) => {
            response += `${index + 1}. **${player.name}** (${player.team}) - ${player.role}\n`;
            response += `   💰 Price: ${player.price} | 📈 Form: ${player.form}%\n`;
            response += `   📝 ${player.reason}\n\n`;
        });
        return response;
    }
    
    formatDifferentialPicks(players) {
        let response = '🎯 **IPL Differential Picks:**\n\n';
        players.forEach((player, index) => {
            response += `${index + 1}. **${player.name}** (${player.team}) - ${player.ownership} owned\n`;
            response += `   💰 Price: ${player.price} | ⚡ Potential: ${player.potential}\n`;
            response += `   📝 ${player.reason}\n\n`;
        });
        return response;
    }
    
    formatCaptainOptions(captains) {
        let response = '👑 **IPL Captain Options:**\n\n';
        captains.forEach((captain, index) => {
            response += `${index + 1}. **${captain.name}** (${captain.team})\n`;
            response += `   📊 Captain Score: ${captain.captaincy} | 🎯 Consistency: ${captain.consistency}\n`;
            response += `   📝 ${captain.reason}\n\n`;
        });
        return response;
    }
    
    formatBudgetPicks(players) {
        let response = '💰 **IPL Budget Picks:**\n\n';
        players.forEach((player, index) => {
            response += `${index + 1}. **${player.name}** (${player.team}) - ${player.role}\n`;
            response += `   💰 Price: ${player.price} | 📊 Value: ${player.value_score}\n\n`;
        });
        return response;
    }
    
    formatFantasyTips(data) {
        const tips = data.tips || [];
        let response = '💡 **IPL Fantasy Tips:**\n\n';
        tips.slice(0, 6).forEach((tip, index) => {
            response += `${index + 1}. ${tip}\n\n`;
        });
        return response;
    }
    
    addMessage(message, sender) {
        if (!this.chatBox) {
            console.log(`${sender}: ${message}`);
            return;
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = this.formatMessage(message);
        
        this.chatBox.appendChild(messageDiv);
        this.chatBox.scrollTop = this.chatBox.scrollHeight;
        
        // Add animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        setTimeout(() => {
            messageDiv.style.transition = 'all 0.3s ease';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 10);
    }
    
    formatMessage(message) {
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>')
            .replace(/• /g, '&bull; ');
    }
    
    showTyping() {
        this.isTyping = true;
        if (this.sendButton) {
            this.sendButton.disabled = true;
            this.sendButton.textContent = '⏳';
        }
    }
    
    hideTyping() {
        this.isTyping = false;
        if (this.sendButton) {
            this.sendButton.disabled = false;
            this.sendButton.textContent = '➤';
        }
    }
    
    async loadLiveData() {
        try {
            console.log('📊 Loading live IPL data...');
            
            // Load live statistics
            const statsResponse = await fetch(`${this.API_URL}/live-stats`);
            const statsData = await statsResponse.json();
            
            if (statsData.stats) {
                this.updateLiveStats(statsData.stats);
            }
            
            // Load match analysis
            const analysisResponse = await fetch(`${this.API_URL}/match-analysis`);
            const analysisData = await analysisResponse.json();
            
            if (analysisData.analysis) {
                this.updateMatchAnalysis(analysisData.analysis);
            }
            
            // Load live matches for sidebar
            const matchesResponse = await fetch(`${this.API_URL}/matches`);
            const matchesData = await matchesResponse.json();
            
            if (matchesData.matches) {
                this.updateLiveMatches(matchesData.matches);
            }
            
            console.log('✅ Live IPL data loaded');
            
        } catch (error) {
            console.error('❌ Error loading live data:', error);
        }
    }
    
    updateLiveStats(stats) {
        console.log('📈 Updating live stats:', stats);
        
        // Update the spans in your HTML with realistic numbers
        this.updateElement('.active-users', stats.active_users?.toLocaleString());
        this.updateElement('.teams-created', stats.teams_created?.toLocaleString());
        this.updateElement('.success-rate', `${stats.success_rate}%`);
        this.updateElement('.live-contests', stats.live_contests?.toLocaleString());
    }
    
    updateMatchAnalysis(analysis) {
        console.log('🏏 Updating match analysis:', analysis);
        
        // Update weather data
        if (analysis.weather) {
            this.updateElement('.temperature', analysis.weather.temperature);
            this.updateElement('.wind-speed', analysis.weather.wind_speed);
            this.updateElement('.humidity', analysis.weather.humidity);
        }
        
        // Update pitch analysis
        if (analysis.pitch) {
            this.updateElement('.batting-friendly', `${analysis.pitch.batting_friendly}%`);
            this.updateElement('.pace-support', `${analysis.pitch.pace_support}%`);
            this.updateElement('.spin-support', `${analysis.pitch.spin_support}%`);
        }
    }
    
    updateLiveMatches(matches) {
        console.log('📺 Updating live matches:', matches);
        
        const matchesList = document.querySelector('.matches-list');
        if (matchesList && matches.length > 0) {
            matchesList.innerHTML = matches.map(match => `
                <div class="match-item">
                    <div class="match-name">${match.name}</div>
                    <div class="match-venue">${match.venue}</div>
                    <div class="match-status ${match.status?.toLowerCase()}">${match.status}</div>
                    ${match.score ? `<div class="match-score">${match.score}</div>` : ''}
                </div>
            `).join('');
        }
    }
    
    updateElement(selector, value) {
        const element = document.querySelector(selector);
        if (element && value !== undefined) {
            element.textContent = value;
            element.classList.remove('loading');
            
            // Add update animation
            element.style.color = '#4e4eff';
            setTimeout(() => {
                element.style.color = '';
            }, 1000);
        }
    }
}

// Enhanced helper functions for testing
window.CricketAIHelpers = {
    askQuestion: (question) => {
        if (window.cricketAI && window.cricketAI.messageInput) {
            window.cricketAI.messageInput.value = question;
            window.cricketAI.sendMessage();
        }
    },
    
    // IPL-specific quick questions
    askLiveMatches: () => window.CricketAIHelpers.askQuestion("What IPL matches are live today?"),
    askBestCaptain: () => window.CricketAIHelpers.askQuestion("Who should I pick as captain for today's IPL match?"),
    askMIvsCSK: () => window.CricketAIHelpers.askQuestion("Give me team strategy for MI vs CSK match"),
    askViratOrRohit: () => window.CricketAIHelpers.askQuestion("Should I pick Virat Kohli or Rohit Sharma today?"),
    askWeatherImpact: () => window.CricketAIHelpers.askQuestion("How will today's weather affect the IPL match?"),
    askDifferentials: () => window.CricketAIHelpers.askQuestion("Give me 3 differential picks for today's IPL matches"),
    
    // Test the system
    testIPLQuestions: () => {
        console.log('🧪 Testing IPL questions...');
        setTimeout(() => window.CricketAIHelpers.askLiveMatches(), 1000);
        setTimeout(() => window.CricketAIHelpers.askBestCaptain(), 3000);
        setTimeout(() => window.CricketAIHelpers.askViratOrRohit(), 5000);
    }
};

// Initialize the Clean Cricket AI
window.cricketAI = new CleanCricketAI();

console.log('🚀 Clean Cricket AI loaded!');
console.log('💡 Try: window.CricketAIHelpers.testIPLQuestions()');
console.log('🏏 Ask about: Live IPL matches, player comparisons, team strategies');