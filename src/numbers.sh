echo "\documentclass[12pt,a4paper]{article}
\usepackage{multido}
\usepackage[hmargin=.8cm,vmargin=1.5cm,nohead,nofoot]{geometry}
\setcounter{page}{$1}
\begin{document}
    \multido{}{$2}{\vphantom{x}\\newpage}
\end{document}"