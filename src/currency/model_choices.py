CURR_USD, CURR_EUR = range(1, 3)
CURRENCY_CHOICES = (
    (CURR_USD, 'USD'),
    (CURR_EUR, 'EUR'),
)


SRC_PB, SRC_MB, SRC_VK = range(1, 4)
SOURCE_CHOICES = (
    (SRC_PB, 'PrivatBank'),
    (SRC_MB, 'MonoBank'),
    (SRC_VK, 'vkurse.dp.ua'),
)