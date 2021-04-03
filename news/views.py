import json
import random
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.


class ComingSoonView(View):
    """Return message <Coming soon>"""
    def get(self, request):
        return redirect("/news/")


class MainPageView(View):
    """Return sorted list of json file on page"""
    def get(self, request):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_list = json.load(json_file)
            for news in news_list:
                news["created"] = news["created"][:10]

        q = request.GET.get('q', None)
        if q is not None:
            news_list = [news for news in news_list if q in news["title"]]
            print(news_list)
        else:
            news_list = sorted(news_list, key=lambda x: x["created"], reverse=True)

        groped_list = []
        i = 0
        if len(news_list) > 1:
            while i < len(news_list) - 1:
                if news_list[i]["created"] == news_list[i + 1]["created"]:
                    groped_list.append([news_list[i], news_list[i + 1]])
                    i += 1
                else:
                    groped_list.append(news_list[i])
                i += 1
        else:
            groped_list = news_list[i]

        return render(request, "news/news_list.html", {"news_list": groped_list})


class NewsDetailView(View):
    """Retrieve news post on page"""
    def get(self, request, link):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_data = json.load(json_file)
            for news in news_data:
                if news['link'] == link:
                    return render(request, 'news/detail_news.html', {"news": news})


class CreateNewsView(View):
    """Create news post"""
    def get(self, request):
        return render(request, "news/news_create.html")

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        link = random.randint(10, 10000)
        created = str(datetime.now())[:19]
        new_post = {"title": title, "text": text, "link": link, "created": created}
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            json_data = json.load(json_file)
            json_data.append(new_post)
        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json.dump(json_data, json_file)
        return redirect("/news/")
