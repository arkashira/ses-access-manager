import pytest
from aws_ticket_manager import generate_aws_ticket, preview_ticket, submit_ticket, get_ticket_status

def test_generate_aws_ticket():
    account_id = "123456789"
    checklist_status = "Completed"
    compliance_docs = "doc1, doc2"
    ticket = generate_aws_ticket(account_id, checklist_status, compliance_docs)
    assert ticket["account_id"] == account_id
    assert ticket["checklist_status"] == checklist_status
    assert ticket["compliance_docs"] == compliance_docs

def test_preview_ticket():
    account_id = "123456789"
    checklist_status = "Completed"
    compliance_docs = "doc1, doc2"
    ticket = generate_aws_ticket(account_id, checklist_status, compliance_docs)
    preview = preview_ticket(ticket)
    assert preview.startswith("{")
    assert preview.endswith("}")

def test_submit_ticket():
    account_id = "123456789"
    checklist_status = "Completed"
    compliance_docs = "doc1, doc2"
    ticket = generate_aws_ticket(account_id, checklist_status, compliance_docs)
    ticket_id = submit_ticket(ticket)
    assert ticket_id.startswith("Ticket ID: ")

def test_get_ticket_status():
    ticket_id = "12345"
    status = get_ticket_status(ticket_id)
    assert status == "Open"

def test_generate_aws_ticket_empty_account_id():
    account_id = ""
    checklist_status = "Completed"
    compliance_docs = "doc1, doc2"
    with pytest.raises(ValueError):
        generate_aws_ticket(account_id, checklist_status, compliance_docs)
