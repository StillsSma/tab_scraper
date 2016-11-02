from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup


class IndexView(TemplateView):

    template_name = "index.html"
    def get_context_data(self):

        context = super().get_context_data()
        if self.request.GET:
            search_url = "http://www.bigbasstabs.com/search.html?search={}&type=songs"
            body = requests.get(search_url.format(self.request.GET.get("song")))
            souper = BeautifulSoup(body.text, "html.parser")
            all_a_tags = souper.findAll("a")
            song_link_list = []

            for counter, tag in enumerate(all_a_tags):
                song_link_list.append(tag.get("href"))
            urls = []
            for song_link in song_link_list:
                print(song_link)
                if 'bass_tabs' in song_link:
                    urls.append(song_link)
            context["song_urls"] = urls

        return context





class SongView(TemplateView):
    template_name = "song.html"

    def get_context_data(self, song_url):
        context = super().get_context_data()
        page = requests.get("http://www.bigbasstabs.com/" + song_url)
        souper = BeautifulSoup(page.text, "html.parser")
        context["tabs"] = souper.find_all("pre")
        return context
