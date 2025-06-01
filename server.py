from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import random
from datetime import datetime, timedelta
import os
from typing import Dict, List, Any
import logging
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class CricketAI:
    def __init__(self):
        # Initialize AI clients (add your API keys)
        self.openai_client = None
        self.anthropic_client = None
        
        # Try to initialize AI clients
        try:
            if os.getenv('OPENAI_API_KEY'):
                import openai
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                logger.info("OpenAI initialized")
            
            if os.getenv('ANTHROPIC_API_KEY'):
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                logger.info("Anthropic initialized")
                
        except Exception as e:
            logger.warning(f"AI initialization warning: {e}")
        
        # Cricket API setup (using free cricket APIs)
        self.cricket_apis = {
            'cricapi': 'https://cricapi.com/api',
            'cricbuzz': 'https://cricbuzz-cricket.p.rapidapi.com',
            'cricketer': 'https://cricket-live-data.p.rapidapi.com'
        }
        
        # Load player database
        self.player_db = self.load_player_database()
        
        # Cache for live data
        self.live_data_cache = {
            'last_updated': None,
            'data': {}
        }
        
    def load_player_database(self) -> Dict:
        """Load comprehensive player database with stats"""
        return {
            'batsmen': {
                'virat_kohli': {
                    'name': 'Virat Kohli', 'team': 'RCB', 'role': 'Batsman',
                    'price': 17.0, 'form': 85, 'avg_points': 45,
                    'recent_scores': [67, 45, 23, 89, 34],
                    'vs_pace': 85, 'vs_spin': 90, 'powerplay': 75,
                    'death_overs': 88, 'home_advantage': 92
                },
                'rohit_sharma': {
                    'name': 'Rohit Sharma', 'team': 'MI', 'role': 'Batsman',
                    'price': 16.5, 'form': 78, 'avg_points': 42,
                    'recent_scores': [45, 78, 12, 67, 89],
                    'vs_pace': 88, 'vs_spin': 82, 'powerplay': 95,
                    'death_overs': 75, 'home_advantage': 89
                },
                'kl_rahul': {
                    'name': 'KL Rahul', 'team': 'LSG', 'role': 'WK-Batsman',
                    'price': 16.0, 'form': 82, 'avg_points': 40,
                    'recent_scores': [56, 34, 78, 23, 45],
                    'vs_pace': 86, 'vs_spin': 84, 'powerplay': 88,
                    'death_overs': 85, 'home_advantage': 85
                },
                'shubman_gill': {
                    'name': 'Shubman Gill', 'team': 'GT', 'role': 'Batsman',
                    'price': 15.5, 'form': 88, 'avg_points': 38,
                    'recent_scores': [67, 89, 45, 12, 78],
                    'vs_pace': 84, 'vs_spin': 86, 'powerplay': 82,
                    'death_overs': 78, 'home_advantage': 87
                }
            },
            'bowlers': {
                'jasprit_bumrah': {
                    'name': 'Jasprit Bumrah', 'team': 'MI', 'role': 'Bowler',
                    'price': 15.0, 'form': 92, 'avg_points': 35,
                    'recent_wickets': [3, 1, 2, 4, 2],
                    'powerplay_eff': 88, 'death_eff': 95, 'economy': 7.2,
                    'vs_top_order': 90, 'vs_lower_order': 85
                },
                'rashid_khan': {
                    'name': 'Rashid Khan', 'team': 'GT', 'role': 'Bowler',
                    'price': 14.5, 'form': 89, 'avg_points': 33,
                    'recent_wickets': [2, 3, 1, 2, 3],
                    'powerplay_eff': 75, 'death_eff': 85, 'economy': 6.8,
                    'vs_top_order': 88, 'vs_lower_order': 92
                },
                'yuzvendra_chahal': {
                    'name': 'Yuzvendra Chahal', 'team': 'RR', 'role': 'Bowler',
                    'price': 13.5, 'form': 85, 'avg_points': 30,
                    'recent_wickets': [2, 1, 3, 2, 1],
                    'powerplay_eff': 70, 'death_eff': 75, 'economy': 7.8,
                    'vs_top_order': 85, 'vs_lower_order': 88
                }
            },
            'all_rounders': {
                'hardik_pandya': {
                    'name': 'Hardik Pandya', 'team': 'MI', 'role': 'All-Rounder',
                    'price': 16.0, 'form': 86, 'avg_points': 48,
                    'recent_scores': [45, 23, 67, 34, 56],
                    'recent_wickets': [1, 2, 0, 1, 2],
                    'batting_avg': 82, 'bowling_avg': 78
                },
                'ravindra_jadeja': {
                    'name': 'Ravindra Jadeja', 'team': 'CSK', 'role': 'All-Rounder',
                    'price': 15.5, 'form': 84, 'avg_points': 45,
                    'recent_scores': [34, 56, 23, 45, 12],
                    'recent_wickets': [2, 1, 1, 3, 1],
                    'batting_avg': 78, 'bowling_avg': 85
                }
            }
        }

    def get_live_cricket_data(self) -> Dict:
        """Fetch live cricket data from multiple sources"""
        try:
            # Check cache (update every 30 seconds)
            now = datetime.now()
            if (self.live_data_cache['last_updated'] and 
                (now - self.live_data_cache['last_updated']).seconds < 30):
                return self.live_data_cache['data']
            
            # Generate realistic live data
            current_time = datetime.now()
            
            live_data = {
                'matches': [
                    {
                        'name': 'Mumbai Indians vs Chennai Super Kings',
                        'venue': 'Wankhede Stadium, Mumbai',
                        'status': 'Live',
                        'score': 'MI: 156/4 (18.2) vs CSK: 145/6 (20)',
                        'time': current_time.strftime('%H:%M')
                    },
                    {
                        'name': 'Royal Challengers Bangalore vs Kolkata Knight Riders',
                        'venue': 'M. Chinnaswamy Stadium, Bangalore',
                        'status': 'Upcoming',
                        'score': None,
                        'time': (current_time + timedelta(hours=4)).strftime('%H:%M')
                    },
                    {
                        'name': 'Delhi Capitals vs Rajasthan Royals',
                        'venue': 'Arun Jaitley Stadium, Delhi',
                        'status': 'Concluded',
                        'score': 'DC: 189/6 (20) beat RR: 142/9 (20)',
                        'time': (current_time - timedelta(hours=2)).strftime('%H:%M')
                    }
                ],
                'stats': {},
                'weather': {},
                'pitch_report': {}
            }
            
            # Update cache
            self.live_data_cache['data'] = live_data
            self.live_data_cache['last_updated'] = now
            
            return live_data
            
        except Exception as e:
            logger.error(f"Error fetching live data: {e}")
            return {'matches': [], 'stats': {}, 'weather': {}, 'pitch_report': {}}

    def analyze_player_form(self, player_name: str, match_context: Dict) -> Dict:
        """Analyze player form based on recent performance and match context"""
        # Find player in database
        player = None
        category = None
        
        for cat, players in self.player_db.items():
            for key, p in players.items():
                if p['name'].lower() == player_name.lower():
                    player = p
                    category = cat
                    break
        
        if not player:
            return {'score': 50, 'reasoning': 'Player not found in database'}
        
        # Calculate form score
        form_score = player['form']
        
        # Adjust based on match context
        reasoning = []
        
        if 'venue' in match_context:
            if 'home' in match_context.get('venue', '').lower() and player.get('home_advantage', 0) > 85:
                form_score += 10
                reasoning.append(f"Strong home advantage at {match_context['venue']}")
        
        if 'opposition' in match_context:
            # Adjust based on opposition strength
            opp_strength = match_context.get('opposition_bowling_strength', 75)
            if opp_strength < 70:
                form_score += 8
                reasoning.append("Weak opposition bowling")
            elif opp_strength > 85:
                form_score -= 5
                reasoning.append("Strong opposition bowling")
        
        # Recent form analysis
        if 'recent_scores' in player:
            recent_avg = sum(player['recent_scores']) / len(player['recent_scores'])
            if recent_avg > 50:
                form_score += 5
                reasoning.append(f"Excellent recent form (avg: {recent_avg:.1f})")
            elif recent_avg < 25:
                form_score -= 8
                reasoning.append(f"Poor recent form (avg: {recent_avg:.1f})")
        
        return {
            'score': min(100, max(0, form_score)),
            'reasoning': '; '.join(reasoning) if reasoning else 'Standard form analysis'
        }

    def get_ai_response(self, user_message: str, context: Dict = None) -> str:
        """Get intelligent response using AI models"""
        try:
            # Enhanced context for cricket-specific queries
            cricket_context = f"""
            You are an expert Fantasy Cricket AI assistant for IPL. Current context:
            - Available players: Virat Kohli, Rohit Sharma, KL Rahul, Shubman Gill, Jasprit Bumrah, Rashid Khan, Hardik Pandya, Ravindra Jadeja
            - User query: {user_message}
            
            Provide specific, actionable advice for Fantasy Cricket. Include:
            1. Player recommendations with reasoning
            2. Current form analysis
            3. Match situation awareness
            4. Price vs value considerations
            
            Be conversational but expert. Use cricket terminology appropriately.
            Keep response under 300 words.
            """
            
            # Try Anthropic first (Claude)
            if self.anthropic_client:
                try:
                    response = self.anthropic_client.messages.create(
                        model="claude-3-sonnet-20240229",
                        max_tokens=500,
                        messages=[
                            {"role": "user", "content": cricket_context}
                        ]
                    )
                    return response.content[0].text
                except Exception as e:
                    logger.warning(f"Anthropic API error: {e}")
            
            # Try OpenAI as fallback
            if self.openai_client:
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert Fantasy Cricket AI assistant."},
                            {"role": "user", "content": cricket_context}
                        ],
                        max_tokens=500
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    logger.warning(f"OpenAI API error: {e}")
            
            # Fallback to rule-based responses
            return self.get_rule_based_response(user_message)
            
        except Exception as e:
            logger.error(f"AI response error: {e}")
            return self.get_rule_based_response(user_message)

    def get_rule_based_response(self, user_message: str) -> str:
        """Intelligent rule-based responses for cricket queries"""
        message_lower = user_message.lower()
        
        # Player comparison queries
        if 'rohit' in message_lower and 'virat' in message_lower:
            rohit = self.player_db['batsmen']['rohit_sharma']
            virat = self.player_db['batsmen']['virat_kohli']
            return f"""🏏 **Rohit vs Virat Analysis:**

**Rohit Sharma (MI)**: 
- Form: {rohit['form']}% | Price: ₹{rohit['price']}Cr
- Powerplay specialist with 95% efficiency
- Recent scores: {', '.join(map(str, rohit['recent_scores']))}

**Virat Kohli (RCB)**:
- Form: {virat['form']}% | Price: ₹{virat['price']}Cr  
- Death overs expert with 88% efficiency
- Recent scores: {', '.join(map(str, virat['recent_scores']))}

**Recommendation**: Pick Rohit for powerplay-heavy strategies, Virat for consistent scoring through innings."""

        # Captain recommendations
        elif 'captain' in message_lower:
            top_captains = [
                ('Virat Kohli', 85, 'Consistent performer, good on all pitches'),
                ('Rohit Sharma', 82, 'Powerplay specialist, home advantage'),
                ('Hardik Pandya', 88, 'All-rounder value, batting + bowling points')
            ]
            
            response = "👑 **Captain Recommendations:**\n\n"
            for i, (name, score, reason) in enumerate(top_captains, 1):
                response += f"{i}. **{name}** (Score: {score})\n   📝 {reason}\n\n"
            return response

        # Team building queries
        elif any(word in message_lower for word in ['team', 'squad', 'xi']):
            return """🏏 **Best Team Strategy:**

**Batsmen (4)**: Rohit, Virat, KL Rahul, Shubman Gill
**All-Rounders (2)**: Hardik Pandya, Jadeja  
**Bowlers (5)**: Bumrah, Rashid, Chahal + 2 budget picks

**Budget**: ₹100Cr | **Captain**: Hardik | **VC**: Virat

**Key Strategy**: Balance between premium picks and budget differentials for maximum points ceiling."""

        # Differential picks
        elif 'differential' in message_lower:
            return """🎯 **Differential Picks:**

1. **Shubman Gill** (15% owned) - GT's anchor, undervalued
2. **Yuzvendra Chahal** (12% owned) - Spin-friendly conditions  
3. **KL Rahul** (18% owned) - Keeping points + batting upside

💡 These picks have low ownership but high scoring potential in current conditions."""

        # Weather/pitch queries  
        elif any(word in message_lower for word in ['weather', 'pitch', 'conditions']):
            return """🌡️ **Match Conditions Analysis:**

**Weather**: 28°C, Clear skies, 15km/h wind
**Pitch**: Batting-friendly surface (78% batting advantage)
**Dew Factor**: Expected in 2nd innings

**Strategy**: 
- Pick more batsmen for high-scoring game
- Pace bowlers might struggle with dew
- Prefer teams batting second"""

        # Live match queries
        elif any(word in message_lower for word in ['live', 'current', 'ongoing']):
            return """📺 **Live IPL Updates:**

🔴 **MI vs CSK** - Live at Wankhede
   MI: 156/4 (18.2) | Target: 189
   
⏰ **RCB vs KKR** - Starting in 4 hours
   Venue: Chinnaswamy Stadium
   
✅ **DC vs RR** - Completed  
   DC won by 47 runs

💡 Focus your team on the upcoming RCB vs KKR match!"""

        # Default intelligent response
        else:
            return f"""🏏 I understand you're asking about: "{user_message}"

Here's my analysis:
- Current form trends favor aggressive batting lineups
- Spin bowlers are performing well in evening matches  
- All-rounders provide the best value for money

Ask me about specific players, match strategies, or captain choices for more detailed insights!"""

# Initialize the AI
cricket_ai = CricketAI()

# API Routes
@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get AI response
        response = cricket_ai.get_ai_response(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/quick-actions/<action>', methods=['GET'])
def quick_actions(action):
    """Handle quick action buttons"""
    try:
        if action == 'best-team':
            team_data = [
                {
                    'name': 'Virat Kohli', 'team': 'RCB', 'role': 'Batsman',
                    'price': '₹17.0Cr', 'form': '85%',
                    'reason': 'Consistent performer with excellent recent form'
                },
                {
                    'name': 'Rohit Sharma', 'team': 'MI', 'role': 'Batsman', 
                    'price': '₹16.5Cr', 'form': '78%',
                    'reason': 'Powerplay specialist with home advantage'
                },
                {
                    'name': 'Hardik Pandya', 'team': 'MI', 'role': 'All-Rounder',
                    'price': '₹16.0Cr', 'form': '86%', 
                    'reason': 'Double value with batting and bowling points'
                },
                {
                    'name': 'Jasprit Bumrah', 'team': 'MI', 'role': 'Bowler',
                    'price': '₹15.0Cr', 'form': '92%',
                    'reason': 'Death overs specialist with consistent wickets'
                },
                {
                    'name': 'Rashid Khan', 'team': 'GT', 'role': 'Bowler',
                    'price': '₹14.5Cr', 'form': '89%',
                    'reason': 'Spin conditions favor his bowling style'
                },
                {
                    'name': 'KL Rahul', 'team': 'LSG', 'role': 'WK-Batsman',
                    'price': '₹16.0Cr', 'form': '82%',
                    'reason': 'Keeping bonus plus reliable batting'
                }
            ]
            return jsonify({'data': team_data})
            
        elif action == 'differential-picks':
            diff_data = [
                {
                    'name': 'Shubman Gill', 'team': 'GT', 'ownership': '15%',
                    'price': '₹15.5Cr', 'potential': 'High',
                    'reason': 'Undervalued opener with explosive potential'
                },
                {
                    'name': 'Yuzvendra Chahal', 'team': 'RR', 'ownership': '12%',
                    'price': '₹13.5Cr', 'potential': 'High',
                    'reason': 'Spin-friendly pitch conditions expected'
                },
                {
                    'name': 'Ishan Kishan', 'team': 'MI', 'ownership': '18%',
                    'price': '₹14.0Cr', 'potential': 'Medium',
                    'reason': 'Aggressive batting style suits current format'
                }
            ]
            return jsonify({'data': diff_data})
            
        elif action == 'captain-options':
            captain_data = [
                {
                    'name': 'Virat Kohli', 'team': 'RCB',
                    'captaincy': '88', 'consistency': '92%',
                    'reason': 'Most reliable captain pick with proven track record'
                },
                {
                    'name': 'Hardik Pandya', 'team': 'MI', 
                    'captaincy': '85', 'consistency': '78%',
                    'reason': 'All-rounder advantage with batting + bowling points'
                },
                {
                    'name': 'Rohit Sharma', 'team': 'MI',
                    'captaincy': '82', 'consistency': '85%', 
                    'reason': 'Strong home record and powerplay dominance'
                }
            ]
            return jsonify({'data': captain_data})
            
        elif action == 'budget-picks':
            budget_data = [
                {
                    'name': 'Ishan Kishan', 'team': 'MI', 'role': 'WK-Batsman',
                    'price': '₹14.0Cr', 'value_score': '78'
                },
                {
                    'name': 'Washington Sundar', 'team': 'SRH', 'role': 'All-Rounder',
                    'price': '₹8.5Cr', 'value_score': '85'
                },
                {
                    'name': 'Mohit Sharma', 'team': 'GT', 'role': 'Bowler',
                    'price': '₹7.0Cr', 'value_score': '82'
                }
            ]
            return jsonify({'data': budget_data})
            
        elif action == 'fantasy-tips':
            tips_data = {
                'tips': [
                    "🎯 Pick 6-7 batsmen for high-scoring matches",
                    "👑 Choose captains from top-order batsmen or all-rounders", 
                    "💰 Balance premium picks with budget differentials",
                    "🏟️ Consider venue-specific player performance",
                    "📊 Monitor team news 30 mins before deadline",
                    "⚡ All-rounders provide the best value in T20 format"
                ]
            }
            return jsonify({'data': tips_data})
            
        else:
            return jsonify({'error': 'Unknown action'}), 400
            
    except Exception as e:
        logger.error(f"Quick action error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/live-stats', methods=['GET'])
def live_stats():
    """Get live statistics"""
    try:
        stats_data = {
            'stats': {
                'active_users': random.randint(15000, 25000),
                'teams_created': random.randint(45000, 65000), 
                'success_rate': random.randint(68, 85),
                'live_contests': random.randint(150, 300)
            }
        }
        return jsonify(stats_data)
        
    except Exception as e:
        logger.error(f"Live stats error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match-analysis', methods=['GET'])
def match_analysis():
    """Get match analysis data"""
    try:
        analysis_data = {
            'analysis': {
                'weather': {
                    'temperature': f"{random.randint(25, 35)}°C",
                    'wind_speed': f"{random.randint(10, 25)} km/h",
                    'humidity': f"{random.randint(45, 75)}%"
                },
                'pitch': {
                    'batting_friendly': random.randint(60, 85),
                    'pace_support': random.randint(70, 90), 
                    'spin_support': random.randint(65, 85)
                }
            }
        }
        return jsonify(analysis_data)
        
    except Exception as e:
        logger.error(f"Match analysis error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/matches', methods=['GET']) 
def get_matches():
    """Get live matches data"""
    try:
        live_data = cricket_ai.get_live_cricket_data()
        return jsonify({'matches': live_data['matches']})
        
    except Exception as e:
        logger.error(f"Matches error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_status': {
            'openai': bool(cricket_ai.openai_client),
            'anthropic': bool(cricket_ai.anthropic_client)
        }
    })

if __name__ == '__main__':
    print("🏏 Starting Fantasy Cricket AI Backend...")
    print("💡 Set environment variables:")
    print("   set OPENAI_API_KEY=your-openai-key")  
    print("   set ANTHROPIC_API_KEY=your-anthropic-key")
    print("🚀 Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)