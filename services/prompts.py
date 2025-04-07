class TextCorrectionPrompts:
    @staticmethod
    def get_correction_prompt(text: str) -> str:
        return (
            "You are an English teacher. Please provide two sections:\n\n"
            "1. Fix the grammar and spelling of this text:\n"
            f"{text}\n\n"
            "2. Explain the mistakes that were corrected.\n\n"
            "Format your response as follows:\n"
            "CORRECTED: [corrected text]\n"
            "EXPLANATION: [explanation of mistakes]"
        )

    @staticmethod
    def get_system_prompt() -> str:
        return "You are an expert English teacher who provides clear corrections and detailed explanations of grammar and spelling mistakes." 