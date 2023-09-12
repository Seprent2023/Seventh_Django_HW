from django import template


register = template.Library()


bad_words = ('poop',
             'ass')


@register.filter()
def censor(txt):
    for word in bad_words:
        word.find(txt)
        if word:
            stars = '*' * len(word)
            txt = txt.replace(word, stars)
    return txt
