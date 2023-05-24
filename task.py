from RPA.Robocorp.WorkItems import WorkItems
from news import FreshNews
from config import Config


if __name__ == "__main__":
    """
    Main script to run the process.
    """
    run_config = Config()
    run = run_config.get_run_detail()
    if run == 'PROD':
        print('Running with workitems.')
        wi = WorkItems()
        wi.get_input_work_item()
        payload = wi.get_work_item_payload()
        search_phrase = payload.get('search_phrase')
        sections = payload.get('sections')
        months = payload.get('months')
    else:
        print('Running with local configration.')
        search_phrase = run_config.search_phrase
        sections = run_config.sections
        months = run_config.months

    newses = FreshNews(search_phrase=search_phrase, sections=sections, months=months)
    try:
        newses.start()
    except Exception as e:
        print(f'Run failed due to error {str(e)}, closing the run.')
    finally:
        newses.end()
