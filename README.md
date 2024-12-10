# Kanshudo Example Sentence Scraper

I needed a lightweight search option for my Thinkpad x41 for when I'm writing documents in Japanese and need to see a kanjis use case.

## Description
This Python script allows you to search for example sentences containing specific kanji or phrases from the [Kanshudo](https://www.kanshudo.com) website. The script fetches examples in batches of 10, provides navigation through results, and logs searches with formatted output.

## Features
- Fetch example sentences containing specified kanji or phrases.
- Display results in batches of 10 with options to view more or quit.
- Log search queries and their corresponding example sentences for future reference.

## Usage

### Prerequisites
- Python 3.6+
- `requests` library (`pip install requests`)
- `beautifulsoup4` library (`pip install beautifulsoup4`)

## Example Output
```
pko's 例文検索方法~

Enter a kanji or phrase (or press Enter to quit): 学生

Example 1: 私は学生です。
Example 2: 彼女は優秀な学生でした。
...
Press any key to see more examples, Escape to quit, or Enter to search for new sentences.
```

## Search History
Search queries and their corresponding example sentences are logged in `search_history.txt` with each example sentence on a new line.
This is great for taking the text file and generating anki cards via my other script "Kanshudo to Anki Export"

### Example of `search_history.txt`
```
Search Query: 学生
Example 1: 私は学生です。
Example 2: 彼女は優秀な学生でした。
...

Search Query: 花
Example 1: 春には花が咲きます。
Example 2: 彼は公園で花を写真に撮りました。
...
```

### made w/ love, pko - 冬旬2024
