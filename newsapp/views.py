from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Article


# ---------------------------------------------------------
# ARTICLE LIST PAGE (HTML)
# Readers, Journalists, Editors see approved articles
# ---------------------------------------------------------
@login_required
def article_list(request):
    """
    Display a list of all approved articles.

    Parameters
    ----------
    request : HttpRequest
        The incoming HTTP request.

    Returns
    -------
    HttpResponse
        A rendered HTML page showing all approved articles.
    """
    articles = Article.objects.filter(approved=True)
    return render(request, "newsapp/article_list.html", {"articles": articles})


# ---------------------------------------------------------
# ARTICLE DETAIL PAGE (HTML)
# Shows the article + approval button for editors
# ---------------------------------------------------------
@login_required
def article_detail(request, article_id):
    """
    Display the details of a single article.

    Parameters
    ----------
    request : HttpRequest
        The incoming HTTP request.
    article_id : int
        The ID of the article to retrieve.

    Returns
    -------
    HttpResponse
        A rendered HTML page showing the article details.
    """
    article = get_object_or_404(Article, id=article_id)
    return render(request, "newsapp/article_detail.html", {"article": article})


# ---------------------------------------------------------
# APPROVE ARTICLE (HTML)
# Editors only — triggers signals when approved
# ---------------------------------------------------------
@permission_required("newsapp.change_article")
def approve_article(request, article_id):
    """
    Approve an article and trigger the approval signal.

    Parameters
    ----------
    request : HttpRequest
        The incoming HTTP request.
    article_id : int
        The ID of the article to approve.

    Returns
    -------
    HttpResponseRedirect
        Redirects back to the article detail page after approval.
    """
    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()  # This triggers your signal
    return redirect("article_detail", article_id=article.id)
