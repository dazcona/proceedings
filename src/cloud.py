import os
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from utils import get_paper_titles

# Paper titles
text = ' '.join(get_paper_titles())

# Wordcloud
x, y = np.ogrid[:600, :600]
mask = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
mask = 255 * mask.astype(int)
wordcloud = WordCloud(background_color="white", repeat=True, mask=mask)
wordcloud = WordCloud(
    max_font_size=44, 
    width=4000, 
    height=4000, 
    background_color="white", 
    repeat=True, 
    mask=mask).generate(text)

# Graph
plt.switch_backend('Agg')
plt.figure( figsize=(10,10) )
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
filename = os.path.join('data', 'figures', 'wordcloud.png')
plt.savefig(filename)