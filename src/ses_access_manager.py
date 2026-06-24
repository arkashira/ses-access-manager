import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class Customer:
    id: int
    sign_up_date: datetime
    access_granted_date: datetime = None

class SESAccessManager:
    def __init__(self):
        self.customers = []
        self.analytics_db = []

    def record_access_granted(self, customer_id: int):
        for customer in self.customers:
            if customer.id == customer_id:
                customer.access_granted_date = datetime.now()
                break

    def get_metrics(self):
        total_sign_ups = len(self.customers)
        granted_access = sum(1 for customer in self.customers if customer.access_granted_date)
        within_30_days = sum(1 for customer in self.customers if customer.access_granted_date and (customer.access_granted_date - customer.sign_up_date).days <= 30)
        return {
            'total_sign_ups': total_sign_ups,
            'granted_access': granted_access,
            'within_30_days': within_30_days / total_sign_ups if total_sign_ups > 0 else 0
        }

    def export_to_analytics_db(self):
        self.analytics_db.append({
            'timestamp': datetime.now(),
            'metrics': self.get_metrics()
        })

    def update_admin_dashboard(self):
        metrics = self.get_metrics()
        return {
            'total_sign_ups': metrics['total_sign_ups'],
            'granted_access': metrics['granted_access'],
            'within_30_days': metrics['within_30_days']
        }
