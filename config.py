import os


class Config:
    """
    Configuration class for the process.
    """

    search_phrase = 'test'
    months = 1
    sections = ['Arts']

    @staticmethod
    def get_run_detail():
        """
        Retrieves the run detail from the environment variable 'RUN' or returns 'local' if not set.

        Returns:
            str: The run detail.
        """
        run = os.getenv('RUN')
        if not run:
            run = 'local'
        return run


OUTPUT = f'{os.getcwd()}/output'
