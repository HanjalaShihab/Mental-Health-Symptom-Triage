from telegram.ext import Application, CommandHandler, MessageHandler, filters
from rules import determine_severity
from messages import QUESTIONS, ADVICE, DISCLAIMER, SYMPTOM_ORDER, SELF_HARM_FOLLOWUP
from ml_model import MentalHealthMLPredictor
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables. Please set it in .env file.")

# Initialize ML predictor
ml_predictor = MentalHealthMLPredictor()
ml_enabled = ml_predictor.load_model()  # Try to load trained model

user_state = {}

YES_WORDS = ["yes", "y", "yeah", "yep"]
NO_WORDS = ["no", "n", "nope"]
RESTART_WORDS = ["restart", "start over", "test again", "reset", "/start"]

def generate_prediction_message(severity, ml_confidence=None, prediction_method="rules"):
    """Generate mental health assessment message"""
    
    classification = {
        "NoConcerns": {
            "name": "No Significant Concerns",
            "icon": "✅",
            "advice": "Maintain healthy routines and reach out if things change."
        },
        "Mild": {
            "name": "Mild Concerns",
            "icon": "🟢",
            "advice": "Practice self-care and monitor symptoms. Consider talking to someone."
        },
        "Moderate": {
            "name": "Moderate Concerns",
            "icon": "🟡",
            "advice": "Consider speaking with a mental health professional."
        },
        "Severe": {
            "name": "Severe Concerns",
            "icon": "🔴",
            "advice": "Please seek professional help as soon as possible."
        },
        "Crisis": {
            "name": "IMMEDIATE CRISIS",
            "icon": "🚨",
            "advice": "Call emergency services (999/112) or go to nearest hospital NOW."
        }
    }
    
    cat = classification.get(severity, classification["NoConcerns"])
    
    text = f"{cat['icon']} **Assessment:** {cat['name']}\n\n"
    
    text += cat['advice']
    
    return text

async def start_conversation(update):
    user_id = update.message.from_user.id
    user_state[user_id] = {
        "index": -1,
        "answers": {},
        "user_name": None,
        "start_time": datetime.now(),
        "awaiting_self_harm_followup": False
    }
    
    welcome_msg = f"""
🧠 Welcome to Mental Health Triage Bot!
{'🤖 AI-Powered ' if ml_enabled else ''}Well-being Check

What is your name? (Enter your name)
    """
    
    await update.message.reply_text(welcome_msg)

async def start(update, context):
    await start_conversation(update)

async def handle_message(update, context):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower()

    # Check for restart commands
    if text in RESTART_WORDS:
        await start_conversation(update)
        return

    # New user - start fresh
    if user_id not in user_state:
        await start_conversation(update)
        return

    state = user_state[user_id]

    # Name input
    if state["user_name"] is None:
        if text.strip():
            state["user_name"] = text.strip()
            
            name_msg = f"Thank you, {state['user_name']}! Let's check in on your well-being. Answer honestly.\n\n"
            await update.message.reply_text(name_msg)
            
            state["index"] = 0
            await ask_next_question(update, state)
        else:
            await update.message.reply_text("Please enter your name.")
        return

    # Handle self-harm follow-up
    if state.get("awaiting_self_harm_followup", False):
        state["awaiting_self_harm_followup"] = False
        if text in YES_WORDS:
            state["answers"]["SelfHarmPlan"] = 1
            # Crisis - complete assessment immediately
            await complete_assessment(update, state)
            return
        else:
            state["answers"]["SelfHarmPlan"] = 0
            # Continue with next question
            state["index"] += 1
            if state["index"] < len(SYMPTOM_ORDER):
                await ask_next_question(update, state)
            else:
                await complete_assessment(update, state)
            return

    # Normal symptom question
    if state["index"] >= len(SYMPTOM_ORDER):
        await complete_assessment(update, state)
        return
        
    symptom = SYMPTOM_ORDER[state["index"]]
    
    if text in YES_WORDS:
        value = 1
    elif text in NO_WORDS:
        value = 0
    else:
        await update.message.reply_text("Please reply with yes or no")
        return

    state["answers"][symptom] = value
    
    # Special handling for self-harm
    if symptom == "SelfHarm" and value == 1:
        # Ask follow-up question
        await update.message.reply_text(SELF_HARM_FOLLOWUP)
        state["awaiting_self_harm_followup"] = True
        return
    
    state["index"] += 1
    
    if state["index"] < len(SYMPTOM_ORDER):
        await ask_next_question(update, state)
    else:
        await complete_assessment(update, state)

async def ask_next_question(update, state):
    """Ask the next symptom question"""
    if state["index"] < 0 or state["index"] >= len(SYMPTOM_ORDER):
        return
    
    next_symptom = SYMPTOM_ORDER[state["index"]]
    await update.message.reply_text(QUESTIONS[next_symptom])

async def complete_assessment(update, state):
    """Complete the assessment and show results"""
    user_name = state["user_name"]
    
    # Get rule-based prediction
    rule_severity = determine_severity(state["answers"])
    
    # Get ML prediction if available
    ml_severity = None
    ml_confidence = 0.0
    if ml_enabled:
        try:
            ml_result = ml_predictor.predict(state["answers"])
            if ml_result[0] is not None:
                ml_severity, ml_confidence, _ = ml_result
        except Exception as e:
            print(f"ML prediction error: {e}")
    
    # Decide which prediction to use
    if ml_enabled and ml_severity and ml_confidence > 0.7:
        final_severity = ml_severity
        prediction_method = "ml"
    else:
        final_severity = rule_severity
        prediction_method = "rules"
    
    # Show summary (symptoms reported)
    present_symptoms = [s for s in SYMPTOM_ORDER if state["answers"].get(s) == 1]
    
    if present_symptoms:
        summary = f"📝 **Symptoms reported for {user_name}:**\n\n"
        for s in present_symptoms[:10]:  # Show first 10 to avoid too long
            summary += f"• {s}\n"
        if len(present_symptoms) > 10:
            summary += f"• ... and {len(present_symptoms)-10} more\n"
    else:
        summary = f"📝 **{user_name}, you reported no significant symptoms.**\n"
    
    await update.message.reply_text(summary)
    
    # Show assessment
    await update.message.reply_text("=" * 40)
    assessment_message = generate_prediction_message(
        final_severity, 
        ml_confidence if prediction_method == "ml" else None,
        prediction_method
    )
    await update.message.reply_text(assessment_message)
    
    # Send advice
    advice_key = final_severity if final_severity in ADVICE else "Mild"
    advice_text = f"💡 **Recommendations for {user_name}:**\n\n" + ADVICE[advice_key] + "\n\n" + DISCLAIMER
    await update.message.reply_text(advice_text)
    
    # Clear user state
    if user_id in user_state:
        del user_state[user_id]

# ===== COMMAND HANDLERS =====

async def help_command(update, context):
    """Show help information"""
    help_text = """
🧠 **Mental Health Triage Bot Commands:**

/start - Start well-being check
/help - Show this help message

📱 **How to use:**
1. Type /start
2. Enter your name
3. Answer questions honestly with yes/no
4. Get educational assessment

🚨 **If you're in crisis:**
Contact emergency services immediately (999/112)
You are not alone - help is available
    """
    await update.message.reply_text(help_text)

async def train_command(update, context):
    """Train ML model (admin only)"""
    if not os.path.exists('MentalHealthSurvey.csv'):
        await update.message.reply_text("❌ Training data not found.")
        return
    
    try:
        await update.message.reply_text("🔄 Training AI model... Please wait (may take a minute).")
        
        predictor = MentalHealthMLPredictor()
        accuracy = predictor.train_model(dataset_path='MentalHealthSurvey.csv', cv_folds=5)
        
        if accuracy:
            ml_predictor.load_model()  # Reload the model
            global ml_enabled
            ml_enabled = True
            
            await update.message.reply_text(
                f"✅ AI model trained successfully!\n"
                f"📊 Training Accuracy: {accuracy*100:.1f}%\n"
                f"🤖 AI analysis is now active!"
            )
        else:
            await update.message.reply_text("❌ Model training failed.")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Training error: {e}")

async def error_handler(update, context):
    """Handle errors"""
    print(f"Error occurred: {context.error}")
    try:
        await update.effective_message.reply_text(
            "❌ An error occurred. Please try again with /start"
        )
    except:
        pass

def main():
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("train", train_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("=" * 60)
    print("🧠 MENTAL HEALTH TRIAGE CHATBOT")
    print("=" * 60)
    print(f"📊 ML Model: {'✅ ACTIVE' if ml_enabled else '❌ NOT FOUND (using rules)'}")
    print("=" * 60)
    print("✅ Bot is running...")
    print("📱 Commands: /start, /help, /train")
    print("=" * 60)
    
    # Run the bot
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()