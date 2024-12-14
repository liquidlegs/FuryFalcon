from enum import StrEnum
import os
import re


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
        self.debug = False
        self.disable_errors = False


    def create_outlook_email(
            self, 
            file_name: str, 
            shw_email: bool = False, 
            snd_email: bool = False
        ) -> bool:
        
        from win32com import client as win32
        
        outlook = win32.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        
        mail.HTMLBody = self.body
        mail.To = self.eml_to
        mail.CC = self.eml_cc
        mail.BCC = self.eml_bcc
        mail.Subject = self.subject_line
        mail.SentOnBehalfOfName = self.eml_from

        for att in self.eml_attachments:
            if os.path.exists(att) == True:
                mail.Attachments.Add(att)
            else:
                print(f"Error: failed to attach file - path {att} does not exist")

        if shw_email:
            mail.Display(True)
            return True
        
        elif snd_email:
            mail.Send()
            print(f"Successfully sent email with subject {self.subject_line} to {self.eml_to}")
            return True
        

        if EmailFmt.is_relative_path(file_name) == True:
            file_name = f"{os.getcwd()}\\{file_name}"

        self.dprint(file_name)
        mail.SaveAs(file_name)
        print(f"Successfully wrote {len(self.body)} bytes to {file_name}")
        return True
    

    def dprint(self, message: str):
        if self.debug == True:
            print(f"Debug => {message}")
        else:
            return
        

    def eprint(self, message):
        if self.disable_errors == False:
            print(f"Error: {message}")
        else:
            return


    def is_relative_path(file_path: str) -> bool:
        content = re.search("^[a-zA-Z]:\\.+", file_path)

        if content == None:
            return True
        
        return False


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