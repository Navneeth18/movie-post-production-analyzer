from app.core.constants import Wd, Wh, Ws, Wp, Wg, Wb, Wt

class HWSService:
    """Simplified HWS calculation service"""
    
    @staticmethod
    def calculate_hws(director, historical, sentiment, pulse, genre, budget, timing):
        """Calculate HWS score based on weighted components"""
        hws = (Wd * director + Wh * historical + Ws * sentiment + 
               Wp * pulse + Wg * genre + Wb * budget + Wt * timing)
        return round(hws, 2)
    
    @staticmethod
    def get_category(hws_score):
        """Categorize movie based on HWS score"""
        if hws_score >= 70:
            return "Big"
        elif hws_score >= 40:
            return "Medium"
        else:
            return "Small"
