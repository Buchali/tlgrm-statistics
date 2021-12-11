import json
from pathlib import Path
from typing import Union

from hazm import Normalizer, word_tokenize
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    """Generates chat statistics from a telegram json file
    """
    def __init__(self, chat_json: Union[str, Path]):
        """
        Args:
            chat_json: path to telegram export json file
        """
        # Load json file
        with open(chat_json) as f:
            self.chat_data = json.load(f)

        # Load and prepare stopwords
        stopwords = open(DATA_DIR / 'stopwords.txt').readlines()
        stopwords = list(map(str.strip, stopwords))
        self.normalizer = Normalizer()
        stopwords = list(map(self.normalizer.normalize, stopwords))

        # Prepare the text
        text_content = ''
        for msg in self.chat_data['messages']:
            if isinstance(msg['text'], str):
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item: item not in stopwords, tokens))
                text_content += f"{' '.join(tokens)}"
        self.text_content = text_content

    def generate_wordcloud(
        self,
        output_dir: Union[str, Path],
        width: int = 1000, height: int = 1000
    ):
        """ generates word cloud from the chat data

        Args:
            output_dir: Path to output directory
        """
        wordcloud = WordCloud(
            width=width, height=height,
            font_path=str(DATA_DIR / 'XBZar.TTF'),
            background_color='white'
            ).generate(self.text_content)
        wordcloud.to_file(str(output_dir / 'wordcloud.png'))


if __name__ == '__main__':
    chat_stat = ChatStatistics(DATA_DIR / 'Python_OG.json')
    chat_stat.generate_wordcloud(DATA_DIR)
    print('Done!')
