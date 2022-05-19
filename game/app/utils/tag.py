def add_tag(msg_builder):
    def decorated(self, *args, **kwargs):
        res = msg_builder(self, *args, **kwargs)
        res = self.game.add_tag_to_msg(res)
        return res
    return decorated
