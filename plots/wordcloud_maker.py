# from nltk.corpus import stopwords
# from stop_words import get_stop_words
from wordcloud import WordCloud


# def write_stopwords_to_file():
#     languages = stopwords.fileids()
#     sw = set()
#     for language in languages:
#         sw.update(stopwords.words(language))
#     languages = ['arabic',
#                  'bulgarian',
#                  'catalan',
#                  'czech',
#                  'danish',
#                  'dutch',
#                  'english',
#                  'finnish',
#                  'french',
#                  'german',
#                  'hungarian',
#                  'indonesian',
#                  'italian',
#                  'norwegian',
#                  'polish',
#                  'portuguese',
#                  'romanian',
#                  'russian',
#                  'spanish',
#                  'swedish',
#                  'turkish',
#                  'ukrainian']
#     for language in languages:
#         sw.update(get_stop_words(language))
#     sw.add("ft")
#     print(repr(sw))
#     with open("../assets/sw.txt", "w", encoding="utf-8") as f:
#         f.write(repr(sw))


def create_wordcloud(words_to_cloud):
    """
    Ta funkcja wypluwa chmurę słów, to 'words_to_cloud' to ramka danych najprawdopodobniej
    podana przez get_lyrics(get_streaming_history(zipped_data)))
    """

    with open("./assets/sw.txt", "r", encoding = "utf-8") as file:
        sw = eval(file.read())
        return WordCloud(stopwords=sw, background_color="white").generate(words_to_cloud)

# Tak to testowałem, wrzucam żeby na potem było wiadomo co tam dodatkowo trzeba dopisać przy
# printowaniu żeby ładnie wyglądało
# word_cloud = create_wordcloud(
#         get_lyrics(
#             get_streaming_history(
#                 ZipFile("./my_spotify_data.zip"))
#         )
#     )
#     plt.imshow(word_cloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.show()
