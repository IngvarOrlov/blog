from .models import Post
from django.utils.text import slugify


def transl(s: str, sep="-") -> str:
    t = {'ё': 'yo', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh',
         'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
         'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh',
         'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
    res = ""
    s = s.strip()
    for i in s.lower():

        if i == " ":
            res += sep
            continue
        elif i in t:
            res += t[i]
            continue
        else:
            res += i
    while '--' in res:
        res = res.replace('--', '-')
    print('res', res)
    res = slugify(res)
    print('res', res)
    return res


def make_unique_slug(title):
    title = transl(title)
    slug = "-".join(title.split())
    # if slug exists
    if Post.objects.filter(slug=slug).order_by("created_at").count() > 0:
        slugs = Post.objects.filter(slug__startswith=slug)
        slugs = slugs.filter(slug__regex=r'^{0}(-\d*)?$'.format(slug))

        print('in search for', slug, 'we find')
        for s in slugs:
            print(s.slug)

        if slugs.count() == 1:
            # if slug already exists, make slug-0
            result = slug + "-0"

        else:
            # increment slug adds
            last_slug = str(slugs.first().slug)
            print(f"last slug is {last_slug}")
            last_slug_list = last_slug.split(sep='-')
            print('last_slug_list ', last_slug_list)
            num = int(last_slug_list.pop()) + 1
            last_slug_list.append(str(num))

            result = "-".join(last_slug_list)

    else:
        result = slug
    return result
