from typing import Dict, Optional

from form_manager.src.services.rules_manager import RulesManager


class CurrencyService:
    def __init__(self, rules_manager: RulesManager) -> None:
        self.data = rules_manager.currency
        self._alias_map = {}
        for code, info in self.data.items():
            for alias in info.get('aliases', []):
                self._alias_map[alias.lower()] = code
                
    def normalize_currency(self, name: str) -> Optional[str]:
        """
        Converts 'Gold Pieces' -> 'gp'

        Args:
            name (str): Coin name.

        Returns:
            Optional[str]: Normalized coin names.
        """
        return self._alias_map.get(name.lower())
    
    def get_value_in_cp(self, currency_node: str) -> int:
        return self.data.get(currency_node, {}).get('value', 0)
    
    def convert_purse_to_cp(self, purse: Dict[str, int]) -> int:
        total = 0
        for currency, amount in purse.items():
            total += amount * self.get_value_in_cp(currency_node=currency)
        return total
    
    def optimize_purse(self, total_cp: int) -> Dict[str, int]:
        sorted_currencies = sorted(self.data.keys(),
                                   key=lambda k: self.data[k]['value'],
                                   reverse=True)
        
        new_purse = {k: 0 for k in self.data}
        remaining = total_cp
        
        for code in sorted_currencies:
            if code == 'ep':
                continue
            
            value = self.data[code]['value']
            if value > 0:
                count = remaining // value
                new_purse[code] = count
                remaining %= value
        
        return new_purse
        