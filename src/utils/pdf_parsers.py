from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
import string
from typing import List
import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

nltk.download("punkt")
class PreProcessing:
    """
    PreProcessor class includes preprocssing functions for text
    """
    def __init__(self):
        pass
    
    def clean_empty_lines(self,text: str) -> str:
        """
        Remove Empty lines from the text
        Args:
            text (str): input text

        Returns:
            str: returns cleaned text
        """
        lines = text.split("\n")
        cleaned_lines = [line for line in lines if line.strip()]
        cleaned_text = "\n".join(cleaned_lines)
        return cleaned_text
    
    def clean_whitespace(self,text: str) -> str:
        """
        Clear whitespaces from text
        Args:
            text (str): input text

        Returns:
            str: returns cleaned text
        """
        cleaned_text = ' '.join(text.split())
        return cleaned_text
    
    def make_sentences(self,text: str) -> List[str]:
        """
        Make sentences of input text
        Args:
            text (str): input text

        Returns:
            List[str]: returns list of sentences
        """
       
        sentences = sent_tokenize(text)
        return sentences
    
    def lowercase_text(self,text: str) -> str:
        """
        Lower case the text
        Args:
            text (str): input text

        Returns:
            str: returns lowercase text
        """
       
        lowercase_text = text.lower()
        return lowercase_text
    
    def remove_punctuation(self,text: str) -> str:
        """
        Remove punctuations from the text
        Args:
            text (str): input text

        Returns:
            str: returns text with removed puntuations
        """
       
        cleaned_text = text.translate(str.maketrans("", "", string.punctuation))
        return cleaned_text
    
    
class PdfParser(PreProcessing):
    
    """
    A class for parsing PDF documents and performing preprocessing on the extracted text.

    This class inherits from the PreProcessing class and extends its functionality
    by adding PDF-specific parsing capabilities.

    Attributes:
        _path (str): The path to the PDF file.
        _skip_page (int): The number of pages to skip from the
                          beginning and end of the PDF.

    Methods:
        parse(): Parses the PDF document, 
                 extracts text from each page, and performs preprocessing.
    """
    def __init__(self,_path,_skip_page=3,para_count=170,overlap=50):
        super().__init__()
        self.reader = PdfReader(_path)
        self.meta_data = {'chapter':[],"page_num":[]}
        self.chapter_count = 1
        self.paragraphs = []
        self.para_count = para_count
        self.overlap = overlap
        self._skip_page = _skip_page
        
        
        
    def parse(self) ->List[str]:
        """
        Parses the PDF document, extracts text from each page, 
        and performs preprocessing.
        
        This method iterates over the pages of the PDF document, extracts the text from each page,
        and applies preprocessing steps inherited from the PreProcessing class, such as removing
        punctuation, cleaning empty lines, and lowercasing the text. It also divides the text into
        paragraphs based on a specified word count.

        Returns:
            List[str]: Returns List of Paragraphs
        """
        
        # Define regular expression for chapter headings
        page_count = 0
        para = []
        p_count = 0
        pages = self.reader.pages[self._skip_page:-self._skip_page]
        for page in pages:
            page_count+=1
            content = page.extract_text()
            # Search for chapter headings using regular expression
                
            for sent in self.make_sentences(content):
                
                sent = self.remove_punctuation(sent)
                sent = self.clean_empty_lines(sent)
                sent = self.clean_whitespace(sent)
                sent = self.lowercase_text(sent)
            
                if len(sent.split())+p_count < self.para_count:
                    para.append(sent)
                    p_count += len(sent.strip().split())
                    
                else:
                    
                    # Preserve previous 50 words from paragraphs
                    if self.paragraphs:
                        prev_words = ' '.join(self.paragraphs[-1].split()[-self.overlap:])
                        para.insert(0, prev_words)

                    self.paragraphs.append(' '.join(para))
                    para = []
                    para.append(sent)
                    p_count = len(sent.strip().split())

                # Add the last paragraph with preserved context
        if self.paragraphs:
            prev_words = ' '.join(self.paragraphs[-1].split()[-self.overlap:])
            para.insert(0, prev_words)

        self.paragraphs.append(' '.join(para))

        
        return self.paragraphs
