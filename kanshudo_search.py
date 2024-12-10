import requests
from bs4 import BeautifulSoup
import os
import sys

def get_kanshudo_examples(kanji):
    # Encode the kanji for URL
    encoded_kanji = requests.utils.quote(kanji)
    
    # Construct the base URL for the search query
    base_url = "https://www.kanshudo.com/searcht"
    page_number = 1
    
    all_examples = []
    
    while True:
        # Construct the full URL with the current page number
        url = f"{base_url}?page={page_number}&q={encoded_kanji}"
        
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Send a GET request to the website
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            break
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove all furigana elements
        for furigana in soup.find_all(['span', 'div'], class_=lambda x: x and 'furigana' in x):
            furigana.decompose()
        
        # Find all example sentences with class "tatoeba"
        examples = soup.find_all('div', class_='tatoeba')
        
        # If no examples are found, break the loop
        if not examples:
            print(f"No more examples found on page {page_number}.")
            break
        
        # Add the examples to the all_examples list
        for example in examples:
            # Extract text from the example sentence
            example_text = ""
            for child in example.children:
                if isinstance(child, str) and child.strip():
                    example_text += child.strip()
                elif child.name:  # Check if it's a tag element
                    if not any('furigana' in c for c in child.get('class', [])):
                        example_text += child.get_text(strip=True)
            
            # Remove unwanted parts like "Copy" or "(click the icon for English translation)"
            cleaned_example = example_text.split('Copy')[0].strip()
            final_example = cleaned_example.replace("(click the icon for English translation)", "").strip()
            all_examples.append(final_example)
        
        # Check for pagination
        pagination = soup.find('div', {'role': 'navigation', 'aria-label': 'Pagination'})
        if not pagination:
            break
        
        # Find the next page link
        next_page_link = pagination.find('a', {'rel': 'next'})
        
        # If no next page link or it is disabled, break the loop
        if not next_page_link or 'disabled' in next_page_link.get('class', []):
            break
        
        print(f"Page {page_number}")
        
        # Increment page number
        page_number += 1
    
    return all_examples

def clear_screen():
    # Clear screen for different operating systems
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/Mac
        os.system('clear')

def read_char():
    # Read a single character from the terminal
    if os.name == 'nt':
        import msvcrt
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\x1b':  # Escape key
                    return 'ESC'
                elif key == b'\r':  # Enter key
                    return 'ENTER'
                else:
                    return 'KEY'
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)  # Read a single byte for normal keys
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        if ch == '\x1b':  # Check for escape sequence
            return 'ESC'
        elif ch == '\n':  # Enter key
            return 'ENTER'
        else:
            return 'KEY'

def display_examples(examples):
    index = 0
    while index < len(examples):
        clear_screen()
        print("pko's 例文検索方法~\n")
        end_index = min(index + 10, len(examples))
        for i in range(index, end_index):
            print(f"Example {i+1}: {examples[i]}")
        
        if end_index >= len(examples):
            break
        
        print("\nPress any key to see more examples, Escape to quit, or Enter to search for new sentences.")
        char = read_char()
        
        # Handle the key press
        if char == 'ESC':
            clear_screen()  # Clear screen when Escape is pressed
            return  # Exit the function and return to main menu
        elif char == 'ENTER':
            clear_screen()
            main()  # Restart the main function to allow a new search
        else:
            index += 10

def log_search(kanji, examples):
    history_file = 'search_history.txt'
    
    # Read existing searches
    existing_searches = set()
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as file:
            for line in file:
                existing_kanji, *existing_examples = line.strip().split('|')
                existing_searches.add(existing_kanji)
    
    # Check if the current search has been done before
    if kanji in existing_searches:
        print("This search has already been logged.")
        return
    
    # Log the new search query and its examples with line breaks for better readability
    with open(history_file, 'a', encoding='utf-8') as file:
        file.write(f"Search Query: {kanji}\n")
        for i, example in enumerate(examples):
            file.write(f"Example {i+1}: {example}\n")
        file.write("\n")  # Add a line break after each search entry

def main():
    clear_screen()  # Clear screen upon launch
    while True:
        print("pko's 例文検索方法~\n")
        
        # Get user input
        kanji = input("Enter a kanji or phrase (or press Enter to quit): ")
        
        if not kanji.strip():
            clear_screen()  # Clear screen when Enter is hit to quit
            print("Exiting.")
            break
        
        # Fetch examples from Kanshudo
        all_examples = get_kanshudo_examples(kanji)
        
        if not all_examples:
            print("No example sentences found. Press any key to search again or Enter to quit.")
            char = read_char()
            if char == 'ENTER':
                clear_screen()
                continue
            else:
                break
        
        display_examples(all_examples)
        
        # Log the search query and its examples
        log_search(kanji, all_examples)

if __name__ == "__main__":
    main()
