class base_score():
    driver = None

    def __init__(self, url):
        self.url = url

    def get_par(self):
        raise NotImplementedError("")

    def get_scores(self):
        raise NotImplementedError("")

    def get_basic_info(self):
        raise NotImplementedError("")

    def after_filter(self, scores):
        played_scores = list(
            filter(lambda x: len(x["score"]) == 18, scores["scores"]))
        scores["scores"] = played_scores
        return scores
