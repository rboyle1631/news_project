from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Article


# ---------------------------------------------------------
# ARTICLE LIST PAGE (HTML)
# Readers, Journalists, Editors see approved articles
# ---------------------------------------------------------
@login_required
def article_list(request):
    articles = Article.objects.filter(approved=True)
    return render(request, "newsapp/article_list.html", {"articles": articles})


# ---------------------------------------------------------
# ARTICLE DETAIL PAGE (HTML)
# Shows the article + approval button for editors
# ---------------------------------------------------------
@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, "newsapp/article_detail.html", {"article": article})


# ---------------------------------------------------------
# APPROVE ARTICLE (HTML)
# Editors only — triggers signals when approved
# ---------------------------------------------------------
@permission_required("newsapp.change_article")
def approve_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()  # This triggers your signal
    return redirect("article_detail", article_id=article.id)
