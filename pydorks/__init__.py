# billythegoat356

# https://github.com/billythegoat356/pydorks

# Version : 0.1

# <3


import requests as req
from bs4 import BeautifulSoup as bs
from random import choice, randint


# GOOGLE SEARCH CLASS

class GoogleSearch():

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

    def search(query: str = None,
               results_len: int = 1,
               lang: str = "fr",
               encoding: str = "utf-8",
               random: bool = False,
               **kwargs):
        """
        Google Search
        :param query | str: --> The text to be searched | ex: "billythegoat356"
        :param results_len | int: --> Number of results | ex: 4
        :param lang | str: --> The language | ex: "en"
        :param encoding | str: --> The encoding for the research | ex: "utf-8"
        :param random | bool: --> Return a random link

        :google dorks | str: --> Google Dorks keyword arguments. Query has to be None.                                      
        """

        return GoogleSearch._search(query=query, results_len=results_len, lang=lang, encoding=encoding, random=random, **kwargs)

    def _search(query: str = None,
                results_len: int = 1,
                lang: str = "fr",
                encoding: str = "utf-8",
                random: bool = False,
                **kwargs):

        if query is None and kwargs == {} or query is not None and kwargs != {}:
            raise GoogleSearch.QueryError(
                "Either 'query' argument either keyword arguments has to be passed.")

        query = GoogleSearch._dorks(
            **kwargs) if query is None else query.replace(" ", "+")

        results_len_search = randint(
            5, 25) + results_len if random else results_len

        url = f"https://google.com/search?q={query}&num={results_len_search}&hl={lang}&ie={encoding}"
        r = req.get(url, headers=GoogleSearch.headers)

        r.raise_for_status()
        html = r.text

        results = GoogleSearch._parse(html)

        if random:
            random_results = []
            for _ in range(results_len):
                random_result = choice(results)
                random_results.append(random_result)
                results.remove(random_result)
            return random_results

        if results_len != len(results):
            results = results[:results_len]

        return results

    def _dorks(**kwargs):
        return " ".join(k+":"+v for k, v in kwargs.items() if v is not None)

    def _parse(html: str):
        results = []

        soup = bs(html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                results.append(link['href'])

        return results

    class QueryError(Exception): ...


# GOOGLE DORKS CLASS

class Dorks:

    def github_search(text: str, results_len: int = 1, random: bool = False, advanced: bool = False):
        return Dorks.website_search(website="github.com", text=text, results_len=results_len, random=random, advanced=advanced)

    def stackoverflow_search(text: str, results_len: int = 1, random: bool = False, advanced: bool = False):
        return Dorks.website_search(website="stackoverflow.com", text=text, results_len=results_len, random=random, advanced=advanced)

    def youtube_search(text: str, results_len: int = 1, random: bool = False, advanced: bool = False):
        return Dorks.website_search(website="youtube.com", text=text, results_len=results_len, random=random, advanced=advanced)

    def pornhub_search(text: str, results_len: int = 1, random: bool = False, advanced: bool = False):
        return Dorks.website_search(website="pornhub.com", text=text, results_len=results_len, random=random, advanced=advanced)

    def api_search(text: str, results_len: int = 1, random: bool = False, advanced: bool = False):
        text += " api"
        url, title = "api" if advanced else None, "api" if advanced else None
        return GoogleSearch.search(results_len=results_len, random=random, inurl=url, intitle=title, intext=text)

    def website_search(website: str, text: str, results_len: int = 1, random: bool = False, advanced: bool = False):
        title = text if advanced else None
        return GoogleSearch.search(results_len=results_len, random=random, site=website, intitle=title, intext=text)
