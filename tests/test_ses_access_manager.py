from datetime import datetime, timedelta
from ses_access_manager import SESAccessManager, Customer

def test_record_access_granted():
    manager = SESAccessManager()
    customer = Customer(1, datetime.now())
    manager.customers.append(customer)
    manager.record_access_granted(1)
    assert customer.access_granted_date is not None

def test_get_metrics():
    manager = SESAccessManager()
    customer1 = Customer(1, datetime.now())
    customer2 = Customer(2, datetime.now() - timedelta(days=31))
    customer2.access_granted_date = datetime.now()
    manager.customers = [customer1, customer2]
    metrics = manager.get_metrics()
    assert metrics['total_sign_ups'] == 2
    assert metrics['granted_access'] == 1
    assert metrics['within_30_days'] == 0

def test_export_to_analytics_db():
    manager = SESAccessManager()
    customer = Customer(1, datetime.now())
    manager.customers.append(customer)
    manager.export_to_analytics_db()
    assert len(manager.analytics_db) == 1

def test_update_admin_dashboard():
    manager = SESAccessManager()
    customer1 = Customer(1, datetime.now())
    customer2 = Customer(2, datetime.now() - timedelta(days=31))
    customer2.access_granted_date = datetime.now()
    manager.customers = [customer1, customer2]
    dashboard = manager.update_admin_dashboard()
    assert dashboard['total_sign_ups'] == 2
    assert dashboard['granted_access'] == 1
    assert dashboard['within_30_days'] == 0
