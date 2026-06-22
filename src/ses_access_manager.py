import json
from dataclasses import dataclass
from email.message import EmailMessage
from typing import List
import uuid
import smtplib
from email.utils import parseaddr

@dataclass
class ComplianceArtifact:
    filename: str
    content: str

class SESAccessManager:
    def __init__(self):
        self.workflow_id = None

    def register_aws_account(self, aws_account_id: str, region: str, contact_email: str) -> str:
        if not aws_account_id or not region or not contact_email:
            raise ValueError("Required fields are missing")
        self.workflow_id = str(uuid.uuid4())
        return self.workflow_id

    def upload_compliance_artifacts(self, artifacts: List[ComplianceArtifact]) -> None:
        if len(artifacts) > 5:
            raise ValueError("Too many compliance artifacts")
        for artifact in artifacts:
            if not artifact.filename or not artifact.content:
                raise ValueError("Invalid compliance artifact")

    def send_email_receipt(self, contact_email: str, workflow_id: str) -> None:
        msg = EmailMessage()
        msg.set_content(f"Your workflow ID is: {workflow_id}")
        msg["Subject"] = "SES Access Workflow Receipt"
        msg["From"] = "ses-access-manager@example.com"
        msg["To"] = contact_email
        try:
            with smtplib.SMTP("localhost") as smtp:
                smtp.send_message(msg)
        except OSError as e:
            print(f"Error sending email: {e}")

    def validate_registration_form(self, aws_account_id: str, region: str, contact_email: str) -> bool:
        if not aws_account_id or not region or not contact_email:
            return False
        return True
