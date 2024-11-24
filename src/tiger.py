import os 
import re
import json
from src.email_fmt import EmailFmt
from src.email_fmt import EmailFileExtension
from functools import wraps


RGX_TEMPLATE_VARS = r"{\S+}"
BANNER = '''
▗▄▄▄▖▗▄▄▄▖ ▗▄▄▖▗▄▄▄▖▗▄▄▖     ▗▄▄▄▖▗▄▖  ▗▄▄▖ ▗▄▖  ▗▄▄▖
  █    █  ▐▌   ▐▌   ▐▌ ▐▌      █ ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌   
  █    █  ▐▌▝▜▌▐▛▀▀▘▐▛▀▚▖      █ ▐▛▀▜▌▐▌   ▐▌ ▐▌ ▝▀▚▖
  █  ▗▄█▄▖▝▚▄▞▘▐▙▄▄▖▐▌ ▐▌      █ ▐▌ ▐▌▝▚▄▄▖▝▚▄▞▘▗▄▄▞▘
'''

class Taco(EmailFmt):

    def __init__(self, args: any):
        self.args = args
        self.debug = args.debug
        self.disable_errors = args.err


    def handle_exceptions(err_message="..."):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    self.eprint(f"({__name__}) failed with error - {e}")
                    return None
            return wrapper
        return decorator


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


    @handle_exceptions(err_message="failed to get data from dictonary")
    def check_json_error(self, data: dict[str], key: str) -> str:
        return data[key]


    def parse_input(self):
        template_file = self.args.template
        logic_file = self.args.logic
        output_file = self.args.output
        config_path = self.args.config_file
        customer_name = self.args.customer_name
        
        data_input = {
            "config_path": config_path,
            "customer_name": customer_name
        }

        templ_buffer = None
        logic_buffer = None
        data_output = None

        if template_file != None:
            if os.path.exists(template_file) == False:
                self.eprint(f"template file located at {template_file} does not exist")
                return

            templ_buffer = Taco.read_file(template_file)
            data_output = self.generate_output_struct(templ_buffer)
        
        if logic_file != None:
            if os.path.exists(logic_file) == False:
                self.eprint(f"logic file located at {logic_file} does not exist")
                return
            
            logic_buffer = Taco.read_file(logic_file)

        if config_path != None:
            if os.path.exists(config_path) == False:
                self.eprint(f"customer contacts file located at {config_path} does not exist")
                return
            
        
        # Callbacks.
        _dprint = self.dprint
        _eprint = self.eprint
        _read_file = Taco.read_file
        _load_json = self.load_json
        _check_json_error = self.check_json_error

        if logic_buffer != None:
            exec(logic_buffer, locals())

        if self.debug == True:
            for i in data_output:
                print(f"{i} -> '{self.check_json_error(data_output, i)}'")

        for i in data_output:
            key = "{" + i + "}"
            data = self.check_json_error(data_output, i)

            if data != None:
                templ_buffer = templ_buffer.replace(key, data)

        if output_file == None:
            print(templ_buffer)
        else:
            self.write_file(output_file, data_output, templ_buffer)


    @handle_exceptions(err_message="failed to write file to disk")
    def write_file(self, output: str, data_output: dict[str], body: str) -> None:
        if output.endswith(EmailFileExtension.MSG):
            return
        
        elif output.endswith(EmailFileExtension.EML):
            email = EmailFmt(
                body,
                eml_to = data_output["to"],
                eml_cc = data_output["cc"],
                eml_bcc = data_output["bcc"],
                subject_line = data_output["subject"]
            )

            email_content = email.get_full_eml_content()
        
        else:
            email_content = body

        with open(output, "w") as f:
            bytes_written = f.write(email_content)
            
            if bytes_written > 0:
                print(f"Successfully wrote {bytes_written} bytes to {output}")
                return



    @handle_exceptions(err_message=f"unable to convert from str to json object")
    def load_json(self, data: str) -> dict[str]:
        return json.loads(data)


    def generate_output_struct(self, file_content) -> dict[str]:
        vars = re.findall(RGX_TEMPLATE_VARS, file_content)
        list_to_dict = []

        for i in vars:
            key = i[1:len(i)-1]
            list_to_dict.append([key, ""])

        list_to_dict.append(["from", ""])
        list_to_dict.append(["to", ""])
        list_to_dict.append(["cc", ""])
        list_to_dict.append(["bcc", ""])
        list_to_dict.append(["subject", ""])

        out_dict = dict(list_to_dict)
        return out_dict


    @handle_exceptions(err_message="failed to read file into a string")
    def read_file(file_path: str) -> str:
        full_path = os.getcwd()

        if Taco.is_relative_path(file_path) == True:
            full_path = "".join([os.getcwd(), file_path])
        else:
            full_path = file_path

        buffer = ""
        with open(full_path, "r") as f:
            buffer = f.read()

        return buffer


    @handle_exceptions(err_message="failed to check if path was relative or not")
    def is_relative_path(file_path: str) -> bool:                
        if os.path.abspath(file_path) == True:
            return True
        else:
            return False