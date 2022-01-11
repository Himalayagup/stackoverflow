# from django.db.models import Q
#
# # Create your views here.
# q = request.GET['q'].split()  # I am assuming space separator in URL like "random stuff"
#
# query = Q()
# for word in q:
#     query = query | Q(title__icontains=word) | Q(tags__name__icontains=word)
# results = Post.objects.filter(query)
