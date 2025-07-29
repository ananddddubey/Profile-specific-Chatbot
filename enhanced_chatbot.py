import re
import json
import random
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Enhanced Profile Database ---
PROFILE = {
    "name": "Anand Dubey",
    "role": "Data Analyst",
    "skills": ["Python", "Excel", "SQL", "Power BI", "Tableau"],
    "education": "B.Tech in AIML from Bennett University",
    "experience": "1+ year research internship, 7+ months industry experience",
    "projects": ["EV Sales Analysis", "Credit Risk Prediction", "TSP Genetic Algorithm", "Healthcare Symptom Checker", "Visit Velocity Analysis"],
    "interests": ["Data Analysis", "Data Engineering", "Hackathons", "Resume Projects"],
    "recent": "Working as Data Analyst and shifting focus from AI/ML to core analytics",
    "location": "India",
    "contact": "Available for freelance projects and collaborations",
    "strengths": ["Problem Solving", "Analytical Thinking", "Data Visualization", "Statistical Analysis"],
    "tools": ["Jupyter Notebook", "VS Code", "Git", "Docker", "AWS"],
    "certifications": ["Data Analysis Specialization", "Python for Data Science"],
    "goals": "To become a senior data analyst and eventually lead data science teams",
    "linkedin": "https://linkedin.com/in/anand-dubey",
    "github": "https://github.com/anand-dubey",
    "portfolio": "https://anand-dubey-portfolio.com"
}

# --- Advanced Intent Rules with Confidence Scoring ---
INTENT_RULES = {
    "greet": {
        "patterns": [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bstart\b", r"\bgood morning\b", r"\bgood evening\b"],
        "weight": 1.0,
        "entities": []
    },
    "name": {
        "patterns": [r"your name", r"who are you", r"introduce yourself", r"about yourself", r"tell me about you"],
        "weight": 0.9,
        "entities": ["name", "identity"]
    },
    "role": {
        "patterns": [r"what do you do", r"your job", r"your position", r"work as", r"profession", r"occupation"],
        "weight": 0.8,
        "entities": ["job", "role", "position"]
    },
    "skills": {
        "patterns": [r"your skills", r"what can you do", r"technologies", r"programming", r"technical skills", r"expertise"],
        "weight": 0.9,
        "entities": ["skills", "technology", "programming"]
    },
    "education": {
        "patterns": [r"education", r"college", r"university", r"degree", r"study", r"qualification", r"academic"],
        "weight": 0.8,
        "entities": ["education", "degree", "university"]
    },
    "experience": {
        "patterns": [r"experience", r"worked", r"background", r"career", r"professional", r"work history"],
        "weight": 0.9,
        "entities": ["experience", "work", "career"]
    },
    "projects": {
        "patterns": [r"projects", r"portfolio", r"built", r"created", r"developed", r"work samples"],
        "weight": 0.9,
        "entities": ["projects", "portfolio", "work"]
    },
    "interests": {
        "patterns": [r"interests", r"hobbies", r"passion", r"like", r"enjoy", r"personal interests"],
        "weight": 0.7,
        "entities": ["interests", "hobbies", "passion"]
    },
    "recent": {
        "patterns": [r"currently", r"now", r"latest", r"recent", r"working on", r"current work"],
        "weight": 0.8,
        "entities": ["current", "recent", "now"]
    },
    "contact": {
        "patterns": [r"contact", r"reach", r"hire", r"collaborate", r"freelance", r"get in touch"],
        "weight": 0.8,
        "entities": ["contact", "hire", "collaborate"]
    },
    "goals": {
        "patterns": [r"goals", r"future", r"ambition", r"plan", r"aspire", r"aim", r"career goals"],
        "weight": 0.7,
        "entities": ["goals", "future", "ambition"]
    },
    "tools": {
        "patterns": [r"tools", r"software", r"applications", r"use", r"work with", r"technologies"],
        "weight": 0.7,
        "entities": ["tools", "software", "applications"]
    },
    "location": {
        "patterns": [r"where", r"location", r"based", r"from", r"live", r"country"],
        "weight": 0.6,
        "entities": ["location", "place", "where"]
    },
    "certifications": {
        "patterns": [r"certifications", r"certificates", r"certified", r"credentials", r"qualifications"],
        "weight": 0.7,
        "entities": ["certifications", "credentials"]
    },
    "social": {
        "patterns": [r"linkedin", r"github", r"portfolio", r"social", r"profile", r"website"],
        "weight": 0.8,
        "entities": ["social", "profile", "portfolio"]
    },
    "bye": {
        "patterns": [r"\bbye\b", r"goodbye", r"see you", r"talk later", r"exit", r"quit"],
        "weight": 1.0,
        "entities": []
    }
}

# --- Context Memory with Enhanced Tracking ---
class ConversationContext:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.last_intent = None
        self.intent_history = []
        self.entity_memory = {}
        self.conversation_count = 0
        self.user_preferences = {}
        self.session_start = datetime.now()
        self.topics_discussed = set()
    
    def update(self, intent, entities, user_input):
        self.last_intent = intent
        self.intent_history.append({
            "intent": intent,
            "timestamp": datetime.now(),
            "input": user_input
        })
        self.conversation_count += 1
        self.topics_discussed.add(intent)
        
        # Update entity memory
        for entity in entities:
            if entity not in self.entity_memory:
                self.entity_memory[entity] = []
            self.entity_memory[entity].append({
                "value": entity,
                "timestamp": datetime.now(),
                "context": intent
            })

# Global context instance
context = ConversationContext()

# --- Enhanced Chatbot Class ---
class EnhancedChatBot:
    def __init__(self, profile):
        self.profile = profile
        self.responses = self._initialize_responses()
    
    def _initialize_responses(self):
        return {
            "greet": [
                f"Hello! I'm {self.profile['name']}'s AI assistant. How can I help you learn more about him today?",
                f"Hi there! I'm here to tell you all about {self.profile['name']}. What would you like to know?",
                f"Welcome! I'm {self.profile['name']}'s digital assistant. Ask me anything about his background and expertise!",
                f"Greetings! I represent {self.profile['name']}, a passionate {self.profile['role']}. How may I assist you?"
            ],
            "name": [
                f"His name is {self.profile['name']}. He's a passionate {self.profile['role']} with expertise in data analytics and machine learning.",
                f"I represent {self.profile['name']}, a skilled {self.profile['role']} from {self.profile['location']}.",
                f"{self.profile['name']} is a dedicated professional who has transitioned from AI/ML to focus more on data analytics."
            ],
            "role": [
                f"{self.profile['name']} works as a {self.profile['role']}. He specializes in transforming raw data into actionable insights for business decisions.",
                f"He's currently working as a {self.profile['role']}, focusing on {self.profile['recent']}.",
                f"As a {self.profile['role']}, he combines technical expertise with business acumen to solve complex data problems."
            ],
            "skills": [
                f"{self.profile['name']} has strong technical skills in: {', '.join(self.profile['skills'])}. He's particularly skilled in {', '.join(self.profile['strengths'])}.",
                f"His technical toolkit includes {', '.join(self.profile['skills'])}, with additional expertise in {', '.join(self.profile['tools'])}.",
                f"He excels in {', '.join(self.profile['skills'][:3])} and has proven abilities in {', '.join(self.profile['strengths'])}."
            ],
            "education": [
                f"He completed his {self.profile['education']}. His academic background in AI/ML provides a strong foundation for his current analytics work.",
                f"{self.profile['name']} holds a {self.profile['education']}, which gives him deep technical knowledge in artificial intelligence and machine learning."
            ],
            "experience": [
                f"{self.profile['name']} has {self.profile['experience']}. His background combines both research and industry experience, giving him a unique perspective on data problems.",
                f"With {self.profile['experience']}, he has worked on various challenging projects spanning different domains.",
                f"His professional journey includes {self.profile['experience']}, providing him with both theoretical knowledge and practical skills."
            ],
            "projects": [
                f"Some of his notable projects include: {', '.join(self.profile['projects'])}. Each project demonstrates his ability to solve real-world problems using data analysis.",
                f"His project portfolio showcases diverse applications: {', '.join(self.profile['projects'][:3])}, and more. Would you like to know details about any specific project?",
                f"He has worked on impactful projects like {', '.join(self.profile['projects'][:2])}, showcasing his versatility in data science applications."
            ],
            "interests": [
                f"He's passionate about {', '.join(self.profile['interests'])}. These interests drive him to continuously learn and improve his analytical skills.",
                f"{self.profile['name']} enjoys {', '.join(self.profile['interests'])}, which keeps him updated with the latest trends in data science."
            ],
            "recent": [
                f"Currently, {self.profile['recent']}. This shift allows him to focus more on business impact and strategic decision-making.",
                f"His recent focus is on {self.profile['recent']}, which aligns with industry demand for strong analytical skills."
            ],
            "contact": [
                f"{self.profile['name']} is {self.profile['contact']}. He's always interested in challenging data problems and innovative analytics solutions.",
                f"You can reach out to him for collaborations - he's {self.profile['contact']}."
            ],
            "goals": [
                f"His career goal is {self.profile['goals']}. He's constantly working on improving his skills and taking on more leadership responsibilities.",
                f"{self.profile['name']} aims {self.profile['goals']}, focusing on both technical excellence and leadership development."
            ],
            "tools": [
                f"He regularly works with {', '.join(self.profile['tools'])} for development and data analysis tasks.",
                f"His preferred development environment includes {', '.join(self.profile['tools'])}, ensuring efficient and productive workflows."
            ],
            "location": [
                f"He's based in {self.profile['location']} and is open to both local and remote opportunities.",
                f"{self.profile['name']} is located in {self.profile['location']} but works with clients globally."
            ],
            "certifications": [
                f"He has earned certifications in {', '.join(self.profile['certifications'])}, validating his expertise in data analysis.",
                f"His professional credentials include {', '.join(self.profile['certifications'])}, demonstrating his commitment to continuous learning."
            ],
            "social": [
                f"You can find his professional profile on LinkedIn: {self.profile.get('linkedin', 'Available upon request')}",
                f"Check out his work on GitHub: {self.profile.get('github', 'Available upon request')} and his portfolio: {self.profile.get('portfolio', 'Available upon request')}"
            ],
            "bye": [
                "Thank you for your interest in Anand's profile! Feel free to come back anytime to learn more.",
                "Goodbye! Don't hesitate to reach out if you want to know more about Anand's work and expertise.",
                "It was great chatting with you! Come back anytime to learn more about Anand's professional journey."
            ],
            "fallback": [
                "I'd be happy to tell you more about Anand. You can ask about his skills, projects, experience, or current work.",
                "That's an interesting question! While I might not have specific details on that, I can tell you about Anand's background, skills, or recent projects.",
                "Let me help you learn more about Anand. Try asking about his technical skills, work experience, or recent projects.",
                "I'm here to share information about Anand's professional profile. What specific aspect would you like to know about?"
            ]
        }
    
    def detect_intent(self, message):
        """Advanced intent detection with confidence scoring and entity extraction"""
        chain_of_thought = []
        chain_of_thought.append("🔍 Analyzing user input for intent patterns...")
        
        normalized_message = message.lower().strip()
        best_intent = "fallback"
        max_score = 0
        matched_patterns = []
        extracted_entities = []
        
        # Intent detection
        for intent, config in INTENT_RULES.items():
            score = 0
            intent_matches = []
            
            for pattern in config["patterns"]:
                if re.search(pattern, normalized_message, re.IGNORECASE):
                    score += config["weight"]
                    intent_matches.append(pattern)
            
            if score > max_score:
                max_score = score
                best_intent = intent
                matched_patterns = intent_matches
                extracted_entities = config["entities"]
        
        # Calculate confidence
        confidence = min(max_score * 0.8, 0.95) if max_score > 0 else 0.3
        
        chain_of_thought.append(f"🎯 Best match: '{best_intent}' (confidence: {confidence:.0%})")
        
        if matched_patterns:
            chain_of_thought.append(f"📝 Matched {len(matched_patterns)} pattern(s)")
        
        if extracted_entities:
            chain_of_thought.append(f"🏷️ Extracted entities: {', '.join(extracted_entities)}")
        
        return {
            "intent": best_intent,
            "confidence": confidence,
            "entities": extracted_entities,
            "matched_patterns": matched_patterns,
            "chain_of_thought": chain_of_thought
        }
    
    def generate_contextual_response(self, intent, message):
        """Generate contextually aware responses"""
        chain_of_thought = []
        chain_of_thought.append("🧠 Analyzing conversation context...")
        
        # Get base responses for the intent
        responses = self.responses.get(intent, self.responses["fallback"])
        
        # Context-aware response selection
        if context.conversation_count > 0:
            # Avoid repeating recent responses
            recent_intents = [h["intent"] for h in context.intent_history[-3:]]
            if intent in recent_intents and len(responses) > 1:
                chain_of_thought.append("🔄 Selecting varied response to avoid repetition")
        
        # Select response
        selected_response = random.choice(responses)
        
        # Add contextual enhancements
        enhanced_response = selected_response
        
        # Add follow-up suggestions based on context
        if context.conversation_count > 2 and intent not in ["bye", "greet"]:
            follow_ups = self._get_follow_up_suggestions(intent)
            if follow_ups:
                enhanced_response += f"\n\n{random.choice(follow_ups)}"
        
        chain_of_thought.append("✨ Applied contextual enhancements")
        chain_of_thought.append("✅ Response generated successfully!")
        
        return enhanced_response, chain_of_thought
    
    def _get_follow_up_suggestions(self, current_intent):
        """Get contextual follow-up suggestions"""
        suggestions = {
            "skills": ["Would you like to know about his specific projects using these skills?", "Interested in learning about his work experience?"],
            "projects": ["Would you like to know more about his technical skills?", "Curious about his educational background?"],
            "experience": ["Want to hear about his notable projects?", "Interested in his future career goals?"],
            "education": ["Would you like to know about his professional experience?", "Curious about his current projects?"],
            "recent": ["Want to know about his previous projects?", "Interested in his long-term career goals?"]
        }
        return suggestions.get(current_intent, [])
    
    def process_message(self, message):
        """Main method to process user message and generate response"""
        start_time = time.time()
        
        # Detect intent and extract information
        detection_result = self.detect_intent(message)
        intent = detection_result["intent"]
        confidence = detection_result["confidence"]
        entities = detection_result["entities"]
        chain_of_thought = detection_result["chain_of_thought"]
        
        # Generate contextual response
        chain_of_thought.append("💡 Generating contextual response...")
        response, additional_thoughts = self.generate_contextual_response(intent, message)
        chain_of_thought.extend(additional_thoughts)
        
        # Update context
        context.update(intent, entities, message)
        
        processing_time = time.time() - start_time
        chain_of_thought.append(f"⚡ Processing completed in {processing_time:.3f}s")
        
        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "chain_of_thought": chain_of_thought,
            "processing_time": processing_time,
            "conversation_count": context.conversation_count
        }

# --- Flask Web Application ---
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize chatbot
chatbot = EnhancedChatBot(PROFILE)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Message is required",
                "status": "error"
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                "error": "Empty message",
                "status": "error"
            }), 400
        
        # Process message with chatbot
        result = chatbot.process_message(user_message)
        
        return jsonify({
            "status": "success",
            "bot_response": result["response"],
            "intent": result["intent"],
            "confidence": result["confidence"],
            "entities": result["entities"],
            "chain_of_thought": result["chain_of_thought"],
            "processing_time": result["processing_time"],
            "conversation_count": result["conversation_count"],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/profile', methods=['GET'])
def get_profile():
    """Get profile information"""
    return jsonify({
        "status": "success",
        "profile": PROFILE,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/context', methods=['GET'])
def get_context():
    """Get current conversation context"""
    return jsonify({
        "status": "success",
        "context": {
            "conversation_count": context.conversation_count,
            "topics_discussed": list(context.topics_discussed),
            "last_intent": context.last_intent,
            "session_duration": str(datetime.now() - context.session_start)
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/reset', methods=['POST'])
def reset_context():
    """Reset conversation context"""
    context.reset()
    return jsonify({
        "status": "success",
        "message": "Context reset successfully",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Enhanced Chatbot API",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    })

# --- Command Line Interface ---
def console_chat():
    """Console-based chat interface"""
    print("🤖 Enhanced Anand Dubey Chatbot")
    print("=" * 50)
    print(f"Hello! I can tell you all about {PROFILE['name']}.")
    print("Type 'bye' to exit, 'reset' to clear context, or 'help' for commands.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("- 'bye' or 'exit': End the conversation")
                print("- 'reset': Clear conversation context")
                print("- 'context': Show current conversation context")
                print("- Ask anything about Anand's profile!\n")
                continue
                
            if user_input.lower() in ['bye', 'exit', 'quit']:
                result = chatbot.process_message(user_input)
                print(f"Bot: {result['response']}")
                break
                
            if user_input.lower() == 'reset':
                context.reset()
                print("Bot: Conversation context has been reset!\n")
                continue
                
            if user_input.lower() == 'context':
                print(f"\nConversation Context:")
                print(f"- Messages exchanged: {context.conversation_count}")
                print(f"- Topics discussed: {', '.join(context.topics_discussed) if context.topics_discussed else 'None'}")
                print(f"- Last intent: {context.last_intent}")
                print(f"- Session duration: {datetime.now() - context.session_start}\n")
                continue
            
            # Process message
            result = chatbot.process_message(user_input)
            
            # Display chain of thought (optional - comment out for cleaner output)
            print("\n--- Chain of Thought ---")
            for i, thought in enumerate(result['chain_of_thought'], 1):
                print(f"{i}. {thought}")
            print(f"Confidence: {result['confidence']:.0%}")
            print("------------------------")
            
            print(f"Bot: {result['response']}\n")
            
        except KeyboardInterrupt:
            print("\n\nBot: Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'console':
        # Run console version
        console_chat()
    else:
        # Run Flask web server
        print("🚀 Starting Enhanced Chatbot API Server...")
        print(f"Profile: {PROFILE['name']} - {PROFILE['role']}")
        print("=" * 50)
        app.run(debug=True, host='0.0.0.0', port=5000)