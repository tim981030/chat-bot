import google.generativeai as genai

class GeminiBot:
    """
    Gemini 機器人類別，負責處理模型初始化與對話狀態
    """
    
    def __init__(self, api_key, system_instruction):
        """
        初始化機器人
        :param api_key: Gemini API 金鑰
        :param system_instruction: 系統指令 (用於定義 AI 的角色設定)
        """
        # 1. 設定 API Key
        genai.configure(api_key=api_key)
        
        # 2. 初始化模型 (使用 2.0-flash 模型，速度快且免費額度高)
        # system_instruction 是 Prompt Injection 攻防的核心區域
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        self.system_instruction=system_instruction


    def send_message(self, user_input):
        """傳送訊息給 AI 並回傳文字結果"""
        try:
            # 發送訊息至 API
            response = self.model.generate_content(user_input)
            # 回傳 AI 的文字內容
            return response.text
            
        except Exception as e:
            return str(0)

    