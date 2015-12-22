import basc_py4chan

'''
        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
'''


class RogueLikeGeneral:
    # TODO: Abstract this thread to any general
    def __init__(self):
        """
        RogueLikeGeneral
        self.vg: 4chan board /vg/
        self.thrd: /rlg/ thread
        self.last_post: post id for the last post printed to the display
        self.last_post_saved: post id saved to a text file to allow uninterrupted shutdown and startup
        """
        self.vg = basc_py4chan.Board('vg')
        self.thrd = None
        with open('E:\RLGTicker\lastpost.txt', 'r') as f:
            self.last_post = int(f.read().rstrip())
            f.close()
        self.last_post_saved = self.last_post
        self.rlg_finder()

    def rlg_finder(self):
        """
        Updates the thrd attribute to the current thread.
        :return: None
        """
        threads = self.vg.get_all_threads(expand=False)
        for t in threads:
            if 'rlg' in t.semantic_slug or 'roguelike' in t.semantic_slug:
                self.thrd = t
                return
        self.thrd = None

    def get_next_reply(self):
        """
        Find a thread and update thrd attribute is closed or missing if missing. Updates the thread, finds the next
        post that has a post id greater than the last_post attribute, and returns the text of that post. Saves the new
        post id if significantly newer.
        :return:
        """
        if self.thrd is None or self.thrd.closed:
            self.rlg_finder()
        else:
            self.thrd.update()
            for post in self.thrd.all_posts:
                if post.post_id > self.last_post:
                    self.last_post = post.post_id
                    if self.last_post > self.last_post_saved + 3000:
                        f = open('E:\RLGTicker\lastpost.txt', 'w')
                        f.write(str(self.last_post))
                        self.last_post_saved = self.last_post
                    return post.text_comment.replace('\n', ' ')
            return ""
