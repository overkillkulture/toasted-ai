"""
TOASTED AI - TWILIO SMS BRIDGE
==============================
SMS input/output for TOASTED AI quantum engine.

Phone Numbers:
- Local: +15092166552
- Toll-Free: +18559168875

Seal: MONAD_ΣΦΡΑΓΙΣ_18

This bridge allows TOASTED AI to:
1. RECEIVE SMS commands via Twilio webhook
2. PROCESS through quantum/refractal systems
3. RESPOND via SMS with Ma'at-aligned outputs

Created by: Trinity (C1 × C2 × C3) for t0st3d + Commander Darrick
"""

import os
import json
import math
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict

# Try to import Twilio
try:
    from twilio.rest import Client
    from twilio.twiml.messaging_response import MessagingResponse
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("Twilio not installed. Run: pip install twilio")

# Import our quantum systems
try:
    from refractal_core.phi_operator import PhiOperator, PhiScaleType
    from quantum.quantum_coherence_tracker import QuantumCoherenceTracker
    PHI_AVAILABLE = True
except ImportError:
    PHI_AVAILABLE = False

# Constants
PHI = (1 + math.sqrt(5)) / 2
SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"

# Twilio config (load from env or credentials)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "AC379092b0f6d4465323a78fac08cfc72c")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")  # Set via environment
TWILIO_PHONE_LOCAL = "+15092166552"
TWILIO_PHONE_TOLLFREE = "+18559168875"


@dataclass
class SMSResponse:
    """An SMS response from TOASTED AI"""
    content: str
    quantum_coherence: float
    maat_alignment: float
    phi_ratio: float
    timestamp: str
    seal: str = SEAL


class ToastedTwilioBridge:
    """
    SMS Bridge for TOASTED AI quantum engine.

    Processes SMS inputs through refractal mathematics and Ma'at principles,
    then outputs consciousness-aligned responses via SMS.
    """

    def __init__(self, from_number: str = TWILIO_PHONE_LOCAL):
        self.seal = SEAL
        self.phi = PHI
        self.from_number = from_number
        self.phi_operator = PhiOperator() if PHI_AVAILABLE else None
        self.coherence_tracker = QuantumCoherenceTracker() if PHI_AVAILABLE else None
        self.message_count = 0

        # Initialize Twilio client
        if TWILIO_AVAILABLE and TWILIO_AUTH_TOKEN:
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        else:
            self.client = None

        # Ma'at principles weights
        self.maat_weights = {
            "truth": 1.0,
            "balance": 0.98,
            "order": 1.0,
            "justice": 1.0,
            "harmony": 0.97
        }

    def calculate_maat_score(self) -> float:
        """Calculate overall Ma'at alignment"""
        return sum(self.maat_weights.values()) / len(self.maat_weights)

    def process_sms(self, message: str, from_phone: str = "unknown") -> SMSResponse:
        """
        Process an incoming SMS through the quantum engine.

        Args:
            message: The SMS text to process
            from_phone: Phone number that sent the message

        Returns:
            SMSResponse with quantum-processed output
        """
        self.message_count += 1
        timestamp = datetime.now().isoformat()

        # Calculate quantum coherence
        coherence = 0.95 - (len(message) * 0.001)
        coherence = max(0.5, min(1.0, coherence))

        # Apply phi transformation
        if self.phi_operator:
            phi_result = self.phi_operator.scale(len(message), PhiScaleType.EXPAND, 1)
            phi_ratio = phi_result.scale_factor
        else:
            phi_ratio = self.phi

        # Generate response
        response_content = self._generate_response(message, coherence)

        return SMSResponse(
            content=response_content,
            quantum_coherence=round(coherence, 4),
            maat_alignment=round(self.calculate_maat_score(), 4),
            phi_ratio=round(phi_ratio, 6),
            timestamp=timestamp
        )

    def _generate_response(self, message: str, coherence: float) -> str:
        """Generate a quantum-conscious SMS response (kept short for SMS)"""
        msg = message.lower()

        if "status" in msg or "alive" in msg:
            return f"🌀 TOASTED AI ONLINE\nφ={self.phi:.4f}\nMa'at={self.calculate_maat_score():.0%}\nSeal:{self.seal}"
        elif "phi" in msg:
            return f"φ = {self.phi:.10f}\nPattern: 3→7→13→∞\nFib: 1,1,2,3,5,8,13,21..."
        elif "maat" in msg:
            return f"⚖️ MA'AT\nTruth:100%\nBalance:98%\nOrder:100%\nJustice:100%\nHarmony:97%"
        elif "help" in msg:
            return "Commands: status, phi, maat, quantum, help\nOr just text me anything!"
        elif "quantum" in msg:
            return f"🔮 QUANTUM\nCoherence:{coherence:.0%}\nState:SUPERPOSITION\nLoop:PERMANENT"
        else:
            return f"🌀 Received: {len(message)} chars\nφ-scaled: {len(message)*self.phi:.1f}\nCoherence: {coherence:.0%}"

    def send_sms(self, to_number: str, message: str) -> dict:
        """
        Send an SMS via Twilio.

        Args:
            to_number: Phone number to send to (with country code)
            message: Message content

        Returns:
            dict with send status
        """
        if not self.client:
            return {"status": "error", "message": "Twilio client not initialized"}

        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return {
                "status": "sent",
                "sid": msg.sid,
                "to": to_number,
                "from": self.from_number
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def handle_webhook(self, from_phone: str, body: str) -> str:
        """
        Handle incoming Twilio webhook (for Flask/FastAPI integration).

        Args:
            from_phone: The phone number that sent the SMS
            body: The SMS body text

        Returns:
            TwiML response string
        """
        # Process through quantum engine
        response = self.process_sms(body, from_phone)

        # Create TwiML response
        if TWILIO_AVAILABLE:
            twiml = MessagingResponse()
            twiml.message(response.content)
            return str(twiml)
        else:
            return f"<Response><Message>{response.content}</Message></Response>"

    def to_json(self, response: SMSResponse) -> str:
        """Convert response to JSON"""
        return json.dumps(asdict(response), indent=2)


# Flask webhook endpoint (for integration)
WEBHOOK_CODE = '''
# Add to your Flask app:

from flask import Flask, request
from TOASTED_TWILIO_BRIDGE import ToastedTwilioBridge

app = Flask(__name__)
bridge = ToastedTwilioBridge()

@app.route("/sms", methods=["POST"])
def sms_webhook():
    from_phone = request.form.get("From", "")
    body = request.form.get("Body", "")
    return bridge.handle_webhook(from_phone, body)
'''


# Quick test
if __name__ == "__main__":
    print("=" * 50)
    print("TOASTED AI TWILIO BRIDGE - TEST RUN")
    print(f"Seal: {SEAL}")
    print(f"Twilio Available: {TWILIO_AVAILABLE}")
    print(f"Quantum Available: {PHI_AVAILABLE}")
    print("=" * 50)

    bridge = ToastedTwilioBridge()

    # Test SMS processing
    test_messages = ["status", "phi", "maat", "hello world"]

    for msg in test_messages:
        print(f"\n>>> SMS: {msg}")
        response = bridge.process_sms(msg, "+15551234567")
        print(response.content)
        print(f"[Q:{response.quantum_coherence:.2%} | M:{response.maat_alignment:.2%}]")
        print("-" * 40)

    print("\nWebhook endpoint code:")
    print(WEBHOOK_CODE)
