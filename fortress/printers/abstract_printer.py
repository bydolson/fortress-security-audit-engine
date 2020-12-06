import abc

from fortress.utils import output


class IncorrectPrinterInitialization(Exception):
    pass


class AbstractPrinter(metaclass=abc.ABCMeta):
    ARGUMENT = ""  # run the printer with fortress.py --ARGUMENT
    HELP = ""  # help information

    WIKI = ""

    def __init__(self, fortress, logger):
        self.fortress = fortress
        self.contracts = fortress.contracts
        self.filename = fortress.filename
        self.logger = logger

        if not self.HELP:
            raise IncorrectPrinterInitialization(
                "HELP is not initialized {}".format(self.__class__.__name__)
            )

        if not self.ARGUMENT:
            raise IncorrectPrinterInitialization(
                "ARGUMENT is not initialized {}".format(self.__class__.__name__)
            )

        if not self.WIKI:
            raise IncorrectPrinterInitialization(
                "WIKI is not initialized {}".format(self.__class__.__name__)
            )

    def info(self, info):
        if self.logger:
            self.logger.info(info)

    def generate_output(self, info, additional_fields=None):
        if additional_fields is None:
            additional_fields = {}
        printer_output = output.Output(info, additional_fields)
        printer_output.data["printer"] = self.ARGUMENT

        return printer_output

    @abc.abstractmethod
    def output(self, filename):
        """TODO Documentation"""
        return
