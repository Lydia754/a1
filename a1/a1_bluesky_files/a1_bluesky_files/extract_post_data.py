"""
Print the number of likes and post text from file containing Bluesky profile source

source should be as rendered after Javascript executes

Live interaction with Bluesky requires having selenium 4 or later and Google Chrome


Author: Lillian Lee (LJL2)
Version: Feb 7, 2025
"""

import a1_second
import os
import bleach
import difflib

# Need for retrieving text from Javascript-displayed webpages
have_selenium = False
try:
    import selenium
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import SessionNotCreatedException
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    options = selenium.webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = selenium.webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    have_selenium = True
except Exception as e:
    print('Error: '+repr(e))
    print('Problem importing selenium; you may need to stick to samples mode.')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^')
    have_selenium = False  # Just making sure

SAMPLE_DIR='bluesky_samples'
SAMPLE_HANDLES = list(os.listdir(SAMPLE_DIR))
POSSIBLE_DEFAULT_HANDLE = 'nytimes.com'
POST_TEXT_INDICATOR = 'data-testid="postText"'
NO_HANDLE = 'Error: handle must be a valid handle'  # Bluesky text produced
DEBUG = False

DEFAULT_HANDLE = POSSIBLE_DEFAULT_HANDLE \
    if POSSIBLE_DEFAULT_HANDLE in SAMPLE_HANDLES \
    else SAMPLE_HANDLES[0]


def print_debug(msg, on=DEBUG):
    """
    Prints a debugging message, prefaced with tag "DEBUG"

    on: a bool as to whether debugging mode should be considered on or off
    """
    if on:
        print('DEBUG: '+msg)


def print_badhandle_message(mode, given, give_hint=True):
    """Prints a message saying we couldn't get that handle's data,
    and suggests typo fixes.

    Preconditions:
        mode: either 's' or 'l' (lower-case ell), for sample or live mode.
        given [str]:
        give_hint [bool]: whether or not to print nearest matches to `given`
            in SAMPLE_HANDLES
    """
    if mode=='l':
        print("Sorry, I couldn't access a page for " + handle + " on Bluesky.\n"
              + "Maybe that handle doesn't exist, or there's an internet issue?\n")
    else:
        assert mode == 's', "print_badhandle_message: bad mode " + str(mode)
        print("Sorry, I don't have a file for that handle in " + SAMPLE_DIR
              + "\n" 
              + "Is folder '"+SAMPLE_DIR+"'' in the current directory?")
        if give_hint:
            closest = difflib.get_close_matches(given, SAMPLE_HANDLES, cutoff=.3)
            if len(closest) > 0:
                print('\n\tOr, maybe you meant one of the following: ' +
                      ', '.join(closest)+'\n')
            else:
                print('I cannot guess what you might have intended.')
                print('Your choices are '+str(SAMPLE_HANDLES) + '\n')


def text_til_next(source_text, indicator, start):
    """Returns: text in `source_text` starting from index `start` and running
    until next occurrence of string `indicator` (or end of source_text if
    there is no next occurrence).

    Preconditions:
        `indicator` [str]: length > 0
        `source_text` [str]:  contains at least one occurrence of `indicator`
        `start` [int]: >= 0, < len(source_text)
    """
    end = source_text.find(indicator, start)
    if end == -1:
        end = len(source_text)
    return source_text[start:end]


def sim_data_fn(handle, driver=None):
    """Return html for handle from local files in folder SAMPLE_DIR.

    Does not error-check.

    Preconditions: There is a relevant file <handle> in SAMPLE_DIR
    handle: a string
    driver: ignored (just need sim_data_fn to take two arguments)
    """
    handle_file = \
        os.path.join(os.path.dirname(__file__), SAMPLE_DIR, handle)
    with open(handle_file, encoding="utf8") as infile:
        data_text = infile.read()
    return data_text


def live_data_fn(handle, driver):
    """Returns Bluesky profile webpage contents for handle.

    Raises ValueError if Bluesky does not recognize the handle, and prints
    a bad-handle error message.
    Raises a TimeoutException on timeout, and prints a message about timeout.
    
    handle is a string meant to represent a Bluesky handle.
    driver is a Selenium webdriver
    """
    try:
        print_debug("Trying to access webpage\n")
        driver.get('https://bsky.app/profile/'+handle)

        # Make sure some actual text is available
        _ = WebDriverWait(driver, timeout=120).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="css-175oi2r"]')))  
        print_debug("Progress: some web text was retrieved\n")

        if NO_HANDLE in driver.page_source:
            raise ValueError()

        _ = WebDriverWait(driver, timeout=100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="postText"]')))
    except TimeoutException:
        print("Timed out")
        raise TimeoutException('Timed out looking for post Text')
    except Exception as e:
        print_debug('Got exception '+repr(e))
        print_badhandle_message('l', handle)
        raise e
    else:
        return driver.page_source


if __name__ == '__main__':
    print()  # leave blank line before starting interaction

    # default to samples mode; override later if needed.
    get_data_fn = sim_data_fn  # overridden later if in live mode
    driver = None  
    in_mode = 's'


    # Does user want to use sample or live data?
    got_in_mode = False  # Whether we know for sure which mode to use
    if not have_selenium:
        got_in_mode = True  # have to use samples mode.

    while not got_in_mode:
        in_prompt = ('Enter "S" or "L" (without the quotes. Hitting return is the same as "S").\n' +
                     '"S": use sample files on your computer.\n' +
                     '\t(Avoids hundreds of people bothering the real'+
                     ' webserver frequently/simultaneously.\n\t' +
                     'Also useful in case of Internet access problems.)\n' +
                     '"L": use the live Bluesky site.\n'+
                     'Your choice? ')
        in_mode = input(in_prompt).strip().lower()
        in_mode = in_mode.replace('"', '').replace("'", '')
        if in_mode not in ["l", "s", ""]:
            print("Sorry, I couldn't process your response.\n")
        else:
            got_in_mode=True
            if in_mode == "l":
                try:
                    driver = selenium.webdriver.Chrome(options=options) #@
                    driver.implicitly_wait(0)
                    get_data_fn = live_data_fn
                except SessionNotCreatedException:
                    print("Couldn't set driver.\n  !!! SWITCHING TO SAMPLES MODE!!! ")
                    in_mode = 's'
                    get_data_fn = sim_data_fn  # Redundant, but safe
                    driver = None
            else:
                in_mode = 's'
                assert driver is None
                assert get_data_fn is sim_data_fn 

    print()
    handle_prompt = ('Enter a Bluesky handle. ' 
                     + 'Or, just hit return for ' + DEFAULT_HANDLE + '.\n'
                     + 'Or, type "q" to quit: ')
    handle = None  # dummy initialization
    while handle != "q":

        success = False  # could we get any data?
        while not success:
            try:
                handle = input(handle_prompt).strip()
                print()

                if in_mode != "l":
                    while handle not in SAMPLE_HANDLES + ['', 'q']:
                        print_badhandle_message(in_mode, handle)
                        handle = input(handle_prompt).strip()

                if handle == "":
                    handle = DEFAULT_HANDLE
                elif handle == 'q':
                    print('Bye for now! Blue skies ahead!\n')
                    exit()

                # Set up data_text, checking input along the way
                pre_postText = \
                    '<div dir="auto" data-word-wrap="1" class="css-146c3p1" '

                data_text = get_data_fn(handle, driver)
                success = True
            except FileNotFoundError:
                print_badhandle_message(in_mode, handle, give_hint=False)
            except SessionNotCreatedException as e:  #@ SessionNotCreatedException not defined??
                print('Problem with web driver;.\n  !!! SWITCHING TO SAMPLES MODE!!! ')
                print_debug('DEBUG: Error was '+repr(e))
                in_mode = 's'
                get_data_fn = sim_data_fn
                print('\n')
                continue
            except ValueError: # Here because post text not found
                continue
            except TimeoutException:  # Timeout message already printed
                continue

        tired = False
        while not tired and POST_TEXT_INDICATOR in data_text:
            # Assertion: there's another post to report on

            section_start = data_text.index(POST_TEXT_INDICATOR)
            section_text = POST_TEXT_INDICATOR + \
                text_til_next(data_text,
                              POST_TEXT_INDICATOR,
                              section_start + len(POST_TEXT_INDICATOR))
            orig_post_text = a1_second.post_info(section_text)
            cleaned_post_text = bleach.clean(orig_post_text, tags=[], strip=True)
            print(cleaned_post_text+'\n'+'.'*10+'\n')

            # Advance to next section, if any
            data_text = data_text[section_start + len(section_text):]

            prompt = 'Hit return for next post, or "q" to stop for this handle: '
            response = input(prompt).strip()
            while response not in ['q', 'Q', '']:
                print("You need to quit this handle before switching to another.")
                response = input(prompt).strip()
            tired = (response in ['q', 'Q'])
            print()

        handle_prompt = ('......\n\nEnter another handle, ' +
                         'or press return for ' + DEFAULT_HANDLE + ', or "q" to quit: ')
