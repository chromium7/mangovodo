from .forms import SearchProductForm


def search(request):
    return {'search_form': SearchProductForm()}
