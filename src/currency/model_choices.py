CURR_USD, CURR_EUR = range(1, 3)
CURRENCY_CHOICES = (
    (CURR_USD, 'USD'),
    (CURR_EUR, 'EUR'),
)


SRC_PB, SRC_MB, SRC_VK, SRC_MTB, SRC_ALPHA, SRC_CONCORD = range(1, 7)
SOURCE_CHOICES = (
    (SRC_PB, 'PrivatBank'),
    (SRC_MB, 'MonoBank'),
    (SRC_VK, 'Vkurse'),
    (SRC_MTB, 'MTBbank'),
    (SRC_ALPHA, 'AlphaBank'),
    (SRC_CONCORD, 'ConcordBank'),
)
