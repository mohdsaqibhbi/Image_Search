import json
import logging
import os
import sys
import time
import traceback
import warnings
from typing import Any, Callable, Dict, Union

# from opencensus.ext.azure.log_exporter import AzureLogHandler

LOGGING_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class APILogging:
    def __init__(
        self,
        logger_name: str = "",
        logging_level: str = "WARNING",
        custom_dimensions: Dict[str, Union[str, int, float]] = {},
    ) -> None:
        """APILogging Class to log info, warnings and errors.

        Args:
            logger_name (str, optional): Name of the logger. Defaults to "".
            logging_level (str, optional): Logging Level. Defaults to "INFO".
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        if logging_level not in LOGGING_LEVELS.keys():
            warnings.warn(
                f"Logging level '{logging_level}' not found. Setting logging level "
                f"to 'INFO'. Valid logging levels are {list(LOGGING_LEVELS.keys())}"
            )
            logging_level = "INFO"
        if not logger_name:
            logger_name = __name__
        self.custom_dimensions = custom_dimensions
        self.logging_level = LOGGING_LEVELS[logging_level]
        logger = logging.getLogger(logger_name)
        logger.setLevel(self.logging_level)
        # logger.addHandler(
        #     AzureLogHandler(
        #         connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
        #     )
        # )
        self.logger = logger

    def info(
        self, info_str: str, custom_dimensions: Dict[str, Union[str, int, float]] = {}
    ):
        """Log the Info

        Args:
            info_str (str): Info String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        self.logger.info(info_str, extra={"custom_dimensions": custom_dimensions})

    def info_print(
        self, info_str: str, custom_dimensions: Dict[str, Union[str, int, float]] = {}
    ):
        """Log and prints Info

        Args:
            info_str (str): Info String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        print(info_str)
        self.logger.info(info_str, extra={"custom_dimensions": custom_dimensions})

    def warning(
        self,
        warning_str: str,
        custom_dimensions: Dict[str, Union[str, int, float]] = {},
    ):
        """Log the Warning

        Args:
            warning_str (str): Warning String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        self.logger.warning(warning_str, extra={"custom_dimensions": custom_dimensions})

    def warning_print(
        self,
        warning_str: str,
        custom_dimensions: Dict[str, Union[str, int, float]] = {},
    ):
        """Log and prints Warning

        Args:
            warning_str (str): Warning String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        print(warning_str)
        self.logger.warning(warning_str, extra={"custom_dimensions": custom_dimensions})

    def error(
        self, err_str: str, custom_dimensions: Dict[str, Union[str, int, float]] = {}
    ):
        """Log the Error

        Args:
            err_str (str): Error String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        self.logger.error(err_str, extra={"custom_dimensions": custom_dimensions})

    def error_print(
        self, err_str: str, custom_dimensions: Dict[str, Union[str, int, float]] = {}
    ):
        """Log and prints Error

        Args:
            err_str (str): Error String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        print(err_str)
        self.logger.error(err_str, extra={"custom_dimensions": custom_dimensions})

    def error_tb(
        self, err_str: str, custom_dimensions: Dict[str, Union[str, int, float]] = {}
    ):
        """Log the Error with Traceback

        Args:
            err_str (str): Error String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        tb = traceback.format_exc()
        self.logger.error(
            f"{err_str}, Traceback: {tb}",
            extra={"custom_dimensions": custom_dimensions},
        )

    def error_print_tb(
        self, err_str: str, custom_dimensions: Dict[str, Union[str, int, float]] = {}
    ):
        """Log and prints Error with Traceback

        Args:
            err_str (str): Error String, that needs to be logged.
            custom_dimensions (Dict[str, Union[str, int, float]], optional): Any custom
            dimensions to add to the Azure App Insights logs, to filter the logs in the
            query. Defaults to {}.
        """
        custom_dimensions.update(self.custom_dimensions)
        tb = traceback.format_exc()
        print(f"{err_str}, Traceback: \n{tb}")
        self.logger.error(
            f"{err_str}, Traceback: {tb}",
            extra={"custom_dimensions": custom_dimensions},
        )


def create_logger(
    application: str, custom_dimensions: Dict[str, str] = {}
) -> APILogging:
    """Create a logger object to log info and errors.

    Args:
        application (str): Name of the application.
        custom_dimensions (Dict[str, str], optional): Any custom dimensions to be added
        to the logger, so that they are logged with every log. Helps in filtering the
        logs.

    Returns:
        APILogging: APILogging Object to log info and errors.
    """
    logging_level = os.environ.get("LOGGING_LEVEL", "WARNING")
    log = APILogging(
        logging_level=logging_level,
        custom_dimensions={
            "application": application,
            "hostName": os.environ.get("HOST_NAME", os.uname().nodename),
            "runner": os.environ.get("RUNNER", "K8s"),
            **custom_dimensions,
        },
    )
    return log


def load_config(config_path: str, log: APILogging) -> Dict[str, Any]:
    """Load the json configurations from given file path.

    Args:
        config_path (str): Path to the Json config file.

    Returns:
        Dict[str, Any]: A Dictionary containing the configurations.
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        tb = traceback.format_exc()
        log.info_print(
            (
                f"Could not find a Config file at specified path: {config_path}! "
                f"Error Traceback: {tb}"
            )
        )
        raise Exception(e)
    return config


def error_handling() -> str:
    """Get the error details.

    Returns:
        str: Error details.
    """
    tb = sys.exc_info()[2]
    line_no = tb.tb_lineno
    module = tb.tb_frame.f_code.co_filename
    return (
        f"Error : {sys.exc_info()[0]}. {sys.exc_info()[1]}, in {module} line: {line_no}"
    )


def timer(info: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to time the execution of a function.

    Args:
        info (str): Information string to be printed before the function name.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]: A decorator that can be used
        to time a function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Time taken by {info}: {round(end_time - start_time, 4)} seconds.")
            return result

        return wrapper

    return decorator
