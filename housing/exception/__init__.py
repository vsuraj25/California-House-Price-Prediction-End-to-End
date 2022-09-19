import os 
import sys

class HousingException(Exception):
    
    def __init__(self, error_message:Exception, error_detail:sys):
        super().__init__(error_message)

        self.error_message = HousingException.get_detailed_error_message(error_message=error_message,
                                                                         error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_detail:sys)->str:
        """
        error_message: Exception object
        error_details: object of sys module

        """
        _, _, exec_tb = error_detail.exc_info() # TO get traceback information, two '_' are used as exec_info() returns (type,value, traceback) and we don't require type and value details.
        
        line_number = exec_tb.tb_frame.f_lineno # traceback.tb_frame.f_lineno gives the line number which causes the error.
        file_name = exec_tb.tb_frame.f_code.co_filename # traceback.tb_frame.f_code.co_filename gives the filename in which error occured
        
        error_message = f"Error occured in the script : [{file_name}] at line number : [{line_number}] error message: [{error_message}] " 

        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return HousingException.__name__.str()

