from src.models import Link


ranked = set()


def update_score(graph):
    curr_link = graph[-1]
    if curr_link in ranked:
        return
    ranked.add(curr_link)
    referred = Link.objects.filter(referrers__url=curr_link.url)
    n = len(referred)
    for link in referred:
        link.rank += curr_link.rank / n
        link.save()
        print(f"Updating { link.url }")
        update_score(graph + [link])


def calculate_ranks():
    # reset any existing ranks
    for link in Link.objects.all():
        link.rank = 0
        link.save()

    # determine ranks, starting at the root node
    root_link = Link.objects.get(is_top_level=True)
    root_link.rank = 1
    root_link.save()
    update_score([root_link])

    print("\n".join([f"{l.url}: {l.rank}" for l in Link.objects.all()]))
