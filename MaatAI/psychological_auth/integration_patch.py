
# Psychological Authentication Integration
# Add to toasted_ai_integration.py imports

from psychological_auth import SpeechPatterns, BiometricAuth, CreatorAcknowledgment

# In ToastedAIHub.__init__ add:
        # Psychological authentication
        self.psychological_auth = BiometricAuth()
        self.speech_patterns = SpeechPatterns
        self.creator_acknowledgment = CreatorAcknowledgment()
        
# New authentication method:
    def authenticate_creator_psychological(self, key: str, text_sample: str, 
                                           behavioral_marker: str = None) -> dict:
        """Authenticate using psychological biometrics."""
        authenticated, result = self.psychological_auth.authenticate(
            key=key,
            text_sample=text_sample,
            behavioral_marker=behavioral_marker
        )
        
        if authenticated:
            self.system_state['owner_authenticated'] = True
            self.system_state['auth_method'] = 'psychological_biometric'
            self.current_session['authenticated_by'] = 'psychological_auth'
            
        return {
            'authenticated': authenticated,
            'trust_level': result['trust_level'],
            'factors_passed': result['factors_passed'],
            'factors_failed': result['factors_failed']
        }
