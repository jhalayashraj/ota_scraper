import random

class ProxyRotator:
    def __init__(self, proxies):
        self.proxies = proxies
        self.current = 0

    def get_proxy(self):
        proxy = self.proxies[self.current]
        self.current = (self.current + 1) % len(self.proxies)
        return proxy

    def get_random_proxy(self):
        return random.choice(self.proxies)
