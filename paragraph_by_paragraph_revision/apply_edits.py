t=open('main.tex').read()
R=[
("and used about 37 times more traced memory.","and whole-pipeline traced memory was about 37 times higher."),
("is one of the most used. In the MachineLearningCVE","is widely used. In the MachineLearningCVE"),
("row-order splits (a proxy for chronology) and smaller training sets?","and row-order splits (a proxy for chronology)?"),
("repeated class-aware validation, nested selection, tuning, and row-order","repeated class-aware validation, nested selection, tuning and row-order"),
("; we use this to place CIC-IDS2017 among available flow datasets.","; we cite it for the criteria by which flow datasets are judged."),
("These four papers concern how far scores can be trusted, not dimensionality reduction.","Together these four papers bear on how far CIC-IDS2017 scores can be trusted; none studies dimensionality reduction."),
(" Our reading was not exhaustive, so this is not a claim about a gap in the literature. IEEE Xplore was not accessible during our search; we used publisher records, proceedings, repositories and preprints. The review is not exhaustive."," Our reading was not exhaustive, so this is not a claim about a gap in the literature. IEEE Xplore was not accessible during our search; we used publisher records, proceedings, repositories and preprints."),
("ran the main grid (2{,}850 fits, about 28 min)","ran the main grid (2{,}850 classifier fits: 190 configurations $\\times$ 15 folds, including the majority-class baseline; about 28 min)"),
("They assume that row order follows capture time and score only a subset of classes, so they support the ranking but give no precise penalty.","Both checks assume that row order follows capture time and score only a subset of classes, so they support the ranking but give no precise penalty."),
("orderings were stable across repeated folds, training sizes, nested selection, tuning and the scorable row-order splits.","orderings were stable across repeated folds, nested selection, tuning and the scorable row-order splits."),
("tuning, smaller training sets and the two row-order checks","tuning and the two row-order checks"),
("Datasets, sampling, splits and metrics differ; the figure is not a performance ranking.","Datasets, sample designs, splits and metrics differ, so the bars are not a like-for-like ranking."),
]
for a,b in R:
    n=t.count(a)
    if n!=1: print("MISS",n,a[:60]); continue
    t=t.replace(a,b)
open('main.tex','w').write(t)
