class StringManipulator:
    def reverse_string(self, text):

        return text[::-1]

    def count_words(self, text):

        return len(text.split())

    def capitalize_words(self, text):

        return text.title()