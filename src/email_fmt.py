from enum import StrEnum


class EmailFileExtension(StrEnum):
    MSG = ".msg"
    EML = ".eml"


class EmailFmt():

    def __init__(
            self, 
            body: str, 
            eml_from = "", 
            eml_to = "", 
            eml_cc = "", 
            eml_bcc = "", 
            subject_line = "", 
            eml_attachments = []
    ):
        self.body = body
        self.eml_from = eml_from
        self.eml_to = eml_to
        self.eml_cc = eml_cc
        self.eml_bcc = eml_bcc
        self.subject_line = subject_line
        self.eml_attachments = eml_attachments


    def create_outlook_email(self, file_name: str) -> bool:
        pass


    def get_full_eml_content(self) -> str:
        output = ""

        if self.eml_from != "":
            output += f"From: {self.eml_from}\n"

        if self.eml_to != "":
            output += f"To: {self.eml_to}\n"

        if self.eml_cc != "":
            output += f"Cc: {self.eml_cc}\n"

        if self.eml_bcc != "":
            output += f"Bcc: {self.eml_bcc}\n"

        if self.subject_line != "" or self.subject_line != None:
            output += f"Subject: {self.subject_line}\n"

        output += "MIME-Version: 1.0\n"
        output += "Content-Type: text/plain; charset=UTF-8\n"
        output += "Content-Transfer-Encoding: 7bit\n\n"
        output += self.body + "\n"
        
        return output