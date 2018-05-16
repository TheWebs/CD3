import operator


class Cache:

    cache = dict()

    @staticmethod
    def add_to_count(file):
        if file in Cache.cache:
            Cache.cache[file] += 1
        else:
            Cache.cache[file] = 1
        Cache.sort_cache()

    @staticmethod
    def get_top_two():
        if len(Cache.cache) < 1:
            return []
        top_two = []
        iterator = iter(Cache.cache.keys())
        top_two.append(next(iterator))
        if len(Cache.cache) > 1:
            top_two.append(next(iterator))
        return top_two

    @staticmethod
    def sort_cache():
        sorted_cache = sorted(Cache.cache.items(), key=operator.itemgetter(1), reverse=True)
        Cache.cache = dict(sorted_cache)

    @staticmethod
    def cache_prepared():
        return len(Cache.cache) >= 2
