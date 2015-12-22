import basc_py4chan


class RogueLikeGeneral:
    def __init__(self):
        self.vg = basc_py4chan.Board('vg')
        self.thrd = None
        with open('E:\RLGTicker\lastpost.txt', 'r') as f:
            self.last_post = int(f.read().rstrip())
            f.close()
        self.last_post_saved = self.last_post
        self.rlg_finder()

    def rlg_finder(self):
        """
        Updates the attribute to reflect the current thread.
        :return:
        """
        threads = self.vg.get_all_threads(expand=False)
        for t in threads:
            if 'rlg' in t.semantic_slug or 'roguelike' in t.semantic_slug:
                self.thrd = t
                return
        self.thrd = None

    def get_next_reply(self):
        if self.thrd is None:
            self.rlg_finder()
        else:
            self.thrd.update()
            if self.thrd.closed:
                self.rlg_finder()
            for post in self.thrd.all_posts:
                if post.post_id > self.last_post:
                    self.last_post = post.post_id
<<<<<<< HEAD
                    return post.text_comment.replace('\n', ' ').replace('\r', '')
=======
                    if self.last_post > self.last_post_saved + 1000:
                        f = open('E:\RLGTicker\lastpost.txt', 'w')
                        f.write(str(self.last_post))
                        self.last_post_saved = self.last_post
                    return post.text_comment.replace('\n', ' ')
>>>>>>> rework
            return ""
